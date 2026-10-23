#!/usr/bin/env python3
"""Build a PDF of the SOMaR specification from the built site.

Run after "jekyll build". The pages are taken in the order of the sidebar
navigation of the home page, and the content of each page (its <main>
element, without the anchor icons and the table of contents of the child
pages) is joined into one HTML document:

- Each page becomes a section whose id is derived from its path, and every
  id inside it is prefixed with that section id, since the pages repeat
  heading ids.
- Links between pages, and to headings on them, point into the document;
  other links to the site are made absolute.
- Images of the site, such as figures, are loaded from the files of the
  built site, since the joined document lies elsewhere.

The document uses the site's stylesheet and MathJax configuration, with
Noto Sans and Source Code Pro in place of the system fonts of the site, which
Linux lacks. The fonts are the static ones of Fontsource (from jsDelivr):
Chromium embeds variable fonts, such as those of Google Fonts, as Type 3
fonts, which PDF viewers render without hinting. The page footer cannot load
web fonts and uses an installed Noto Sans (fonts-noto-core) if there is one. It is printed with headless Chromium
(Playwright) once MathJax has typeset the equations and the fonts have
loaded, so it needs network access. The combined HTML is written to a temporary directory only.

The bookmarks of the PDF are Chromium's outline of the headings. Each page
starts with an h1, so the headings of a page take an aria-level offset by
its depth in the navigation, which Chromium uses for the outline without
changing their style. Chromium also drops the spaces at the line breaks of
a wrapped heading, so the titles of the bookmarks are set afterwards to the
text of the headings, in document order.

A table of contents follows the title page. Chromium cannot number its
entries, so the document is printed twice: the first print gives the page of
each section (its named destination, which Chromium writes for every id that
a link points to), and the second fills in those page numbers. The page
numbers take a fixed width, so the second print lays out as the first.

Usage: python3 scripts/build_pdf.py [SITE_DIR] [--output PATH]

SITE_DIR defaults to _site and the output to SITE_DIR/somar-format.pdf.
Requires beautifulsoup4, pypdf, and playwright (with "playwright install
chromium").
"""

import argparse
import datetime
import os
import posixpath
import re
import sys
import tempfile
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_NAME = "somar-format.pdf"
STYLESHEET = "assets/css/just-the-docs-default.css"
FONT_STYLESHEETS = [
    f"https://cdn.jsdelivr.net/npm/@fontsource/{font}/{style}.css"
    for font, styles in (
        ("noto-sans@5.2.10", ("300", "400", "400-italic", "500", "700")),
        ("source-code-pro@5.2.7", ("400", "700")),
    )
    for style in styles
]
FONT_FAMILIES = ("Noto Sans", "Source Code Pro")

PRINT_CSS = """
@page { size: A4; margin: 18mm 16mm 20mm; }
/* The site sets the root font size to 16px at the width of an A4 page; the theme
   sizes everything in rem, so this scales the whole document to 10.5pt text. */
html { font-size: 14px !important; }
html, body { background: #fff; }
body { margin: 0; font-family: "Noto Sans", sans-serif; }
code, pre, kbd, samp { font-family: "Source Code Pro", monospace !important; }
.main-content { max-width: none; margin: 0; padding: 0; }
section.pdf-section { break-before: page; }
.title-page { text-align: center; padding-top: 30vh; }
.title-page h1 { font-size: 2rem !important; line-height: 1.3; }
.title-page p { font-size: 1.1rem !important; }
nav.pdf-toc { break-before: page; }
nav.pdf-toc ol { list-style: none; padding: 0; margin: 0; }
nav.pdf-toc li { margin: 0 !important; padding: 0; }
nav.pdf-toc li::before { content: none !important; }
nav.pdf-toc a { display: flex; align-items: baseline; color: inherit; text-decoration: none; }
nav.pdf-toc .leader { flex: 1; margin: 0 0.4em; border-bottom: 1px dotted #959396; }
nav.pdf-toc .page { width: 2.5em; text-align: right; font-variant-numeric: tabular-nums; }
nav.pdf-toc .depth-0 { font-weight: 500; margin-top: 0.6em !important; }
nav.pdf-toc .depth-1 { padding-left: 1.5em; }
nav.pdf-toc .depth-2 { padding-left: 3em; }
pre, pre code { white-space: pre-wrap !important; overflow-wrap: anywhere; }
/* The site sets the font size on <code> only, so the lines of a code block
   keep the spacing of the body text; give it to <pre> instead. */
pre.highlight { font-size: 0.75em; line-height: 1.4; }
pre.highlight code { font-size: inherit; }
.highlight, .table-wrapper { overflow: visible !important; }
h1, h2, h3, h4, h5, h6 { break-after: avoid; }
tr, pre, .open_issue { break-inside: avoid; }
"""

HEADING = re.compile(r"^h[1-6]$")

FOOTER = (
    '<div style="width: 100%; font-family: \'Noto Sans\', sans-serif; font-size: 8px; color: #5c5962; '
    'padding: 0 16mm; display: flex; justify-content: space-between;">'
    "<span>{title}</span>"
    '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span>'
    "</div>"
)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse(path):
    return BeautifulSoup(read(path), "html.parser")


def nav_pages(index, baseurl):
    """Site path (relative to baseurl), title, and nesting depth of the pages, in sidebar order."""
    pages = []
    for link in index.select("nav#site-nav a.nav-list-link"):
        path = urlsplit(link["href"]).path
        if path.startswith(baseurl):
            path = path[len(baseurl):]
        if path not in (page[0] for page in pages):
            depth = len(link.find_parents("ul", class_="nav-list")) - 1
            pages.append((path, link.get_text(strip=True), depth))
    return pages


def page_file(site_dir, path):
    """Built file of a site path ("" or ".../" is a directory index)."""
    if path == "" or path.endswith("/"):
        path += "index.html"
    return os.path.join(site_dir, path)


def section_id(path):
    """Section id of a site path, e.g. "contents/georeferencing/" -> "georeferencing"."""
    path = path.removesuffix("index.html").removesuffix(".html").strip("/")
    path = path.removeprefix("contents").strip("/")
    return path.replace("/", "-") or "abstract"


def normalize(path):
    """Site path as listed in the navigation, for comparing link targets."""
    if path.endswith("/index.html"):
        return path[: -len("index.html")]
    return "" if path == "index.html" else path


def page_content(soup):
    """Contents of the <main> element of a built page, cleaned up for print."""
    main = soup.select_one("#main-content main")
    for anchor in main.select("a.anchor-heading"):
        anchor.decompose()
    # Table of contents of the child pages, which follow as sections anyway.
    for heading in main.select("h2.text-delta"):
        rule = heading.find_previous_sibling()
        listing = heading.find_next_sibling()
        if rule is not None and rule.name == "hr":
            rule.decompose()
        if listing is not None and listing.name == "ul":
            listing.decompose()
        heading.decompose()
    return main


def rewrite(main, path, sections, baseurl, site_url, site_dir):
    """Prefix the ids of a page, point its links into the document, and its images to the built site."""
    own = sections[path]
    for tag in main.find_all(id=True):
        tag["id"] = f"{own}--{tag['id']}"
    for tag in main.find_all(attrs={"aria-labelledby": True}):
        tag["aria-labelledby"] = f"{own}--{tag['aria-labelledby']}"
    page_url = baseurl + path
    for link in main.find_all("a", href=True):
        href = link["href"]
        parts = urlsplit(urljoin(page_url, href))
        if parts.scheme or parts.netloc or not parts.path.startswith(baseurl):
            continue
        target = normalize(posixpath.normpath(parts.path[len(baseurl):]) + ("/" if parts.path.endswith("/") else ""))
        target = "" if target in (".", "./") else target
        if target in sections:
            fragment = parts.fragment
            link["href"] = f"#{sections[target]}--{fragment}" if fragment else f"#{sections[target]}"
        else:
            link["href"] = urljoin(site_url, parts.path[len(baseurl):]) + (f"#{parts.fragment}" if parts.fragment else "")
    for image in main.find_all("img", src=True):
        parts = urlsplit(urljoin(page_url, image["src"]))
        if not parts.scheme and not parts.netloc and parts.path.startswith(baseurl):
            image["src"] = "file://" + os.path.abspath(os.path.join(site_dir, parts.path[len(baseurl):]))


def table_of_contents(doc, pages, sections, page_numbers):
    """Contents listing every page, with its page in the PDF if known."""
    toc = doc.new_tag("nav", attrs={"class": "pdf-toc"})
    heading = doc.new_tag("h1")
    heading.string = "Contents"
    toc.append(heading)
    listing = doc.new_tag("ol")
    toc.append(listing)
    for path, title, depth in pages:
        item = doc.new_tag("li", attrs={"class": f"depth-{min(depth, 2)}"})
        link = doc.new_tag("a", href=f"#{sections[path]}")
        for cls, text in (("title", title), ("leader", ""), ("page", str(page_numbers.get(sections[path], "")))):
            span = doc.new_tag("span", attrs={"class": cls})
            span.string = text
            link.append(span)
        item.append(link)
        listing.append(item)
    return toc


def build_document(site_dir, page_numbers):
    index = parse(page_file(site_dir, ""))
    canonical = index.find("link", rel="canonical")["href"]
    baseurl = urlsplit(canonical).path
    if not baseurl.endswith("/"):
        baseurl += "/"
    site_url = canonical if canonical.endswith("/") else canonical + "/"

    pages = nav_pages(index, baseurl)
    paths = [path for path, _, _ in pages]
    sections = {path: section_id(path) for path in paths}

    title = index.find("meta", property="og:site_name")
    title = title["content"] if title is not None else index.title.get_text(strip=True)
    description = index.find("meta", attrs={"name": "description"})
    description = description["content"] if description is not None else ""
    status = index.select_one(".status-pill")
    status = status.get_text(" ", strip=True) if status is not None else ""

    doc = BeautifulSoup("<!doctype html><html lang='en'><head></head><body></body></html>", "html.parser")
    doc.head.append(doc.new_tag("meta", charset="utf-8"))
    doc.head.append(doc.new_tag("title"))
    doc.head.title.string = title
    for href in FONT_STYLESHEETS:
        doc.head.append(doc.new_tag("link", rel="stylesheet", href=href))
    style = doc.new_tag("style")
    style.string = read(os.path.join(site_dir, STYLESHEET)) + PRINT_CSS
    doc.head.append(style)
    # MathJax configuration and loader of _includes/head_custom.html.
    for script in index.head.find_all("script"):
        if "MathJax" in (script.string or "") or "mathjax" in script.get("src", ""):
            doc.head.append(BeautifulSoup(str(script), "html.parser"))

    content = doc.new_tag("div", attrs={"class": "main-content"})
    doc.body.append(content)
    cover = BeautifulSoup(
        "<div class='title-page'><h1></h1><p class='description'></p>"
        "<p class='status'></p><p class='date'></p><p class='url'></p></div>",
        "html.parser",
    )
    cover.h1.string = title
    cover.select_one(".description").string = description
    cover.select_one(".status").string = status
    cover.select_one(".date").string = f"Built {datetime.date.today().isoformat()}"
    url = cover.new_tag("a", href=site_url)
    url.string = site_url
    cover.select_one(".url").append(url)
    content.append(cover)
    content.append(table_of_contents(doc, pages, sections, page_numbers))

    for path, _, depth in pages:
        main = page_content(parse(page_file(site_dir, path)))
        rewrite(main, path, sections, baseurl, site_url, site_dir)
        # Nest the headings of a child page below those of its parent in the outline.
        for heading in main.find_all(HEADING):
            heading["aria-level"] = str(int(heading.name[1]) + depth)
        section = doc.new_tag("section", attrs={"class": "pdf-section", "id": sections[path]})
        section.extend(list(main.contents))
        content.append(section)
    headings = [" ".join(heading.get_text(" ").split()) for heading in doc.find_all(HEADING)]
    return str(doc), title, list(sections.values()), headings


def section_pages(pdf, section_ids):
    """Page (counting from 1) on which each section of a printed PDF starts."""
    reader = PdfReader(pdf)
    destinations = reader.named_destinations
    return {
        sid: reader.get_destination_page_number(destinations["/" + sid]) + 1
        for sid in section_ids
        if "/" + sid in destinations
    }


def outline_items(outline):
    """The items of a PDF outline dictionary, in document order."""
    item = outline.get("/First")
    while item is not None:
        item = item.get_object()
        yield item
        yield from outline_items(item)
        item = item.get("/Next")


def set_outline_titles(pdf, titles):
    """Set the titles of the bookmarks of a PDF to the headings, which Chromium gives without the spaces at line breaks."""
    writer = PdfWriter(clone_from=pdf)
    items = list(outline_items(writer._root_object["/Outlines"].get_object()))
    if len(items) != len(titles):
        sys.exit(f"{pdf}: {len(items)} bookmarks for {len(titles)} headings")
    for item, text in zip(items, titles):
        item[NameObject("/Title")] = TextStringObject(text)
    writer.write(pdf)


def print_pdf(html_path, output, title):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{html_path}", wait_until="networkidle")
        page.wait_for_function("window.MathJax && MathJax.startup && MathJax.startup.promise")
        page.evaluate("MathJax.startup.promise")
        loaded = page.evaluate(
            """async (families) => {
                await document.fonts.ready;
                return families.filter((family) => [...document.fonts].some(
                    (face) => face.family.replace(/"/g, "") === family && face.status === "loaded"));
            }""",
            list(FONT_FAMILIES),
        )
        missing = [family for family in FONT_FAMILIES if family not in loaded]
        if missing:
            sys.exit(f"fonts not loaded: {', '.join(missing)}")
        page.pdf(
            path=output,
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            display_header_footer=True,
            header_template="<div></div>",
            footer_template=FOOTER.format(title=title),
            outline=True,
            tagged=True,
        )
        browser.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("site_dir", nargs="?", default=os.path.join(ROOT, "_site"))
    parser.add_argument("--output", help=f"PDF to write (default: SITE_DIR/{PDF_NAME})")
    args = parser.parse_args()

    site_dir = os.path.abspath(args.site_dir)
    if not os.path.isfile(page_file(site_dir, "")):
        sys.exit(f"{site_dir}: no built site found; run 'bundle exec jekyll build' first")
    output = os.path.abspath(args.output or os.path.join(site_dir, PDF_NAME))

    with tempfile.TemporaryDirectory() as tmp:
        html_path = os.path.join(tmp, "somar-format.html")
        draft = os.path.join(tmp, "draft.pdf")
        page_numbers = {}
        for pdf in (draft, output):
            html, title, section_ids, headings = build_document(site_dir, page_numbers)
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)
            print_pdf(html_path, pdf, title)
            if pdf == draft:
                page_numbers = section_pages(draft, section_ids)
                missing = [sid for sid in section_ids if sid not in page_numbers]
                if missing:
                    sys.exit(f"no page found for the sections {', '.join(missing)}")
    set_outline_titles(output, headings)
    if section_pages(output, section_ids) != page_numbers:
        sys.exit(f"{output}: the sections moved between the two prints; the contents give wrong pages")
    print(f"{output}: {len(section_ids)} pages of the site")


if __name__ == "__main__":
    main()
