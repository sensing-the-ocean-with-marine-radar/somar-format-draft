#!/usr/bin/env python3
"""Check the internal links and anchors of the built site.

Run after "jekyll build" (and after scripts/build_pdf.py, which writes the
PDF that every page links to). Every href and src in the built HTML that
points into the site must name an existing file, and its fragment, if any,
must name an id or a named anchor on the target page. Links to other sites
are not checked.

Usage: python3 scripts/check_links.py [SITE_DIR] [--baseurl PATH]

SITE_DIR defaults to _site and the base URL to the baseurl of _config.yml.
"""

import argparse
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Page(HTMLParser):
    """The ids and the links of an HTML page."""

    def __init__(self):
        super().__init__()
        self.ids, self.links = set(), []

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "a" and "name" in attributes:
            self.ids.add(attributes["name"])
        for name in ("href", "src"):
            if attributes.get(name):
                self.links.append(attributes[name])


def baseurl():
    with open(os.path.join(ROOT, "_config.yml"), encoding="utf-8") as f:
        match = re.search(r"^baseurl:\s*\"?([^\"\n]*?)\"?\s*$", f.read(), re.M)
    return match.group(1).rstrip("/") if match else ""


def target(site_dir, page, path, base):
    """Return the site-relative file that a link path points to, or None if it points outside the site."""
    if path == "":
        return page
    if path.startswith("/"):
        if not path.startswith(base + "/") and path != base:
            return None
        path = path[len(base):].lstrip("/")
    else:
        path = os.path.normpath(os.path.join(os.path.dirname(page), path))
    if path in ("", ".") or path.endswith("/") or os.path.isdir(os.path.join(site_dir, path)):
        path = os.path.join(path, "index.html")
    return os.path.normpath(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("site_dir", nargs="?", default="_site")
    parser.add_argument("--baseurl", help="the base URL the site was built with, if not that of _config.yml")
    args = parser.parse_args()

    pages = {}
    for directory, _, files in os.walk(args.site_dir):
        for name in files:
            if name.endswith(".html"):
                path = os.path.join(directory, name)
                page = Page()
                with open(path, encoding="utf-8") as f:
                    page.feed(f.read())
                pages[os.path.relpath(path, args.site_dir)] = page

    base, broken = (args.baseurl.rstrip("/") if args.baseurl is not None else baseurl()), set()
    for name, page in pages.items():
        for link in page.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            path = target(args.site_dir, name, unquote(parts.path), base)
            if path is None:
                broken.add((name, link, "outside the site"))
            elif path not in pages:
                if not os.path.exists(os.path.join(args.site_dir, path)):
                    broken.add((name, link, "no such file"))
            elif parts.fragment and unquote(parts.fragment) not in pages[path].ids:
                broken.add((name, link, "no such anchor"))

    for name, link, reason in sorted(broken):
        print(f"FAIL {name}: {link} ({reason})")
    print(f"{len(pages)} pages checked, {len(broken)} broken links")
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
