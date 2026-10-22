#!/usr/bin/env python3
"""Link the names of attributes and variables to the table rows that define them, and check the links of the text.

Every row of an attribute or variable table has an id (see _plugins/table_rows.rb):
the name of its item where that name heads only one row of the page and is no
heading id there, and otherwise the id of the nearest preceding heading and the
name. Two kinds of mention, written as `name`, link to these rows:

- in the description, the last column, of a row of these tables, the first
  mention of an item whose row is in another table, on the same page or another;
- in the text, the first mention per section (##) of an item defined on another
  page; mentions on the defining page stay plain.

A name that more than one row defines links to the row on its own page,
preferring the row of the current section; on a product page of the annex, to
the row of its category page that applies to the product (see SECTION_SCOPES in
check_examples.py); for comment, source, and references outside the pages of the
global attributes, to the variable attributes, unless "global attribute" goes
with the name; for a variable defined both under Product variables and on a
category page, to Product variables; and otherwise it stays plain. The words
around a mention narrow its meaning: a name after "product type" or inside
quotes is no reference, and "attribute" or "variable" next to it leaves out the
rows of the other kind.

The script also checks the links of the text against the rule of the README:
each convention has one URL, for the version SOMaR pins (CONVENTION_URLS), such
as version 95 of the CF standard name table, which check_examples.py validates
against, and is linked reference-style, as [CF][cf] with the URL at the foot of
the page, except on the References page; a link whose text is a name has the
name alone as its text; and no section (##) links to the same target twice,
apart from citations and tables.

Usage: python3 scripts/link_items.py [--check]

Without --check, the script adds the missing links to the pages; with --check,
it lists them and fails if there are any, as CI runs it. Problems that the
script cannot fix, such as a wrong URL, fail it in either mode.
"""

import argparse
import glob
import os
import posixpath
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from check_examples import SECTION_SCOPES, STANDARD_NAME_TABLE_VERSION, registry  # noqa: E402

DEFINITION_TABLES = ("attribute-table", "variable-table", "mandatory-attribute-table")
HEADING = re.compile(r"^(#{1,6}) (.*)$")
CODE_NAME = re.compile(r"`(\w+)`")
# A Markdown link, whose text may hold code spans.
LINK = re.compile(r"\[((?:[^\[\]`]|`[^`]*`)*)\]\(([^)\s]*)\)")
PRODUCT_VARIABLES = "contents/product_types/product_variables.md"
VARIABLE_ATTRIBUTES = "contents/metadata_attributes/variable_attributes.md"
# The names of both a global and a variable attribute, and the pages on which they mean the global one.
GLOBAL_AND_VARIABLE_ATTRIBUTES = ("comment", "references", "source")
# The words before or after a mention that say what it names: a product type, a global attribute
# (also as the last of a list, "the global attributes `a` and `b`"), or an attribute or variable.
LIST_BEFORE = r"(?: `x`(?:,| and|, and))* $"
PRODUCT_TYPE_BEFORE = re.compile(r"product types?" + LIST_BEFORE)
GLOBAL_ATTRIBUTES_BEFORE = re.compile(r"global attributes?" + LIST_BEFORE)
KIND_WORDS = {
    "attribute": (re.compile(r"\battributes?" + LIST_BEFORE), re.compile(r" (?:global |variable )?attributes?\b")),
    "variable": (re.compile(r"\bvariables?" + LIST_BEFORE), re.compile(r" variables?\b")),
}
# The sentence by which a product page of the annex names its product type and category.
CATEGORY_LINK = re.compile(r"The product type `(\w+)` is one of the \[[^\]]*\]\(\.\./product_types/(\w+)\.md")
GLOBAL_ATTRIBUTE_PAGES = ("contents/metadata_attributes/mandatory_global.md", "contents/metadata_attributes/optional_global.md")
# The conventions SOMaR builds on, by the start of their URLs, and the one URL of each, without
# fragment, for the version SOMaR pins. UDUNITS has no version pinned, so its current documentation applies.
CONVENTION_URLS = {
    "https://cfconventions.org/": (
        "https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html",
        f"https://cfconventions.org/Data/cf-standard-names/{STANDARD_NAME_TABLE_VERSION}/build/cf-standard-name-table.html",
    ),
    "https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery": ("https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3",),
    "https://library.wmo.int/": ("https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes",),
    "https://github.com/NCAR/CfRadial": ("https://github.com/NCAR/CfRadial/tree/master/docs",),
    "https://docs.unidata.ucar.edu/udunits/": ("https://docs.unidata.ucar.edu/udunits/current/",),
}
# The bibliography, which cites the conventions with their URLs written out.
REFERENCES = "contents/references/index.md"
# A reference-style link, [text][label], and the definition of a label, [label]: URL.
REFERENCE_LINK = re.compile(r"(?<!!)\[((?:[^\[\]`]|`[^`]*`)*)\]\[([\w-]*)\]")
REFERENCE_DEFINITION = re.compile(r"^\[([\w-]+)\]: (\S+)")
URL = re.compile(r"https?://[^\s)>\]\"]+")


def slug(heading):
    """The id that kramdown gives a heading."""
    text = re.sub(r"`|\*|\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    return re.sub(r"[^a-z0-9 _-]", "", text.lower()).strip().replace(" ", "-")


def tables(lines):
    """Yield (first line index, last line index, class) for the tables of a page."""
    start = None
    for i, line in enumerate(lines):
        if line.startswith("|"):
            start = i if start is None else start
        elif start is not None:
            match = re.match(r"\{: \.([\w-]+) \}", line.strip())
            yield start, i - 1, match.group(1) if match else ""
            start = None


def page_rows(lines):
    """Return [(row id, name, section id, h2 section id, kind)] for the definition rows of a page, as table_rows.rb assigns the ids.

    The kind is "attribute" or "variable", by the class of the table.
    """
    headings, rows, heading, section = [], [], None, None
    table_class = {}
    for start, end, kind in tables(lines):
        for i in range(start, end + 1):
            table_class[i] = kind
    code = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            code = not code
            continue
        if code:
            continue
        match = HEADING.match(line)
        if match and len(match.group(1)) >= 2:
            heading = slug(match.group(2))
            headings.append(heading)
            if len(match.group(1)) == 2:
                section = heading
            continue
        match = re.match(r"\| `(\w+)`", line)
        if match and table_class.get(i) in DEFINITION_TABLES:
            kind = "variable" if table_class[i] == "variable-table" else "attribute"
            rows.append((match.group(1), heading, section, kind))
    counts = {}
    for name, _, _, _ in rows:
        counts[name] = counts.get(name, 0) + 1
    return [(name if counts[name] == 1 and name not in headings else f"{h}-{name}", name, h, s, k) for name, h, s, k in rows]


def definitions(pages):
    """Return {name: [(page, row id, h2 section id, kind)]} for all definition rows."""
    found = {}
    for page, lines in pages.items():
        for row_id, name, _, section, kind in page_rows(lines):
            found.setdefault(name, []).append((page, row_id, section, kind))
    return found


def target(name, page, section, defs, global_attribute=False, context=None, kind=None):
    """Return (page, row id) that a mention of name links to, or None if it is ambiguous.

    global_attribute is true for a mention followed by "global attribute"; context is
    (product type, category page, {section: product types}) on a product page of the annex,
    where a name that the category page defines in several sections means the row of the
    section that applies to the product. kind, "attribute" or "variable", is the kind
    of item that the words around the mention name, if any; rows of the other kind are
    left out.
    """
    candidates = [c for c in defs.get(name, []) if kind is None or c[3] == kind]
    if not candidates:
        return None
    own = [c for c in candidates if c[0] == page]
    if len(own) == 1:
        return own[0][:2]
    if own:
        here = [c for c in own if c[2] == section]
        return here[0][:2] if len(here) == 1 else None
    if context:
        product, category, scopes = context
        rows = [c for c in candidates if c[0] == category and (scopes.get(c[2]) is None or product in scopes[c[2]])]
        if len(rows) == 1 and len([c for c in candidates if c[0] == category]) > 1:
            return rows[0][:2]
    if name in GLOBAL_AND_VARIABLE_ATTRIBUTES:
        meant = GLOBAL_ATTRIBUTE_PAGES if global_attribute or page in GLOBAL_ATTRIBUTE_PAGES else (VARIABLE_ATTRIBUTES,)
        rows = [c for c in candidates if c[0] in meant]
        if len(rows) == 1:
            return rows[0][:2]
    if len(candidates) == 1:
        return candidates[0][:2]
    variables = [c for c in candidates if c[0] == PRODUCT_VARIABLES]
    if len(variables) == 1 and all(c[0].startswith("contents/product_types/") for c in candidates):
        return variables[0][:2]
    return None


def href(page, destination, row_id):
    if destination == page:
        return f"#{row_id}"
    return posixpath.relpath(destination, posixpath.dirname(page)) + f"#{row_id}"


def unlinked(text):
    """The text with links whose text is code replaced by the code, and code spans by a placeholder name."""
    text = re.sub(r"\[(`\w+`)\]\([^)]*\)", r"\1", text)
    return re.sub(r"`[^`]*`", "`x`", text)


def link_line(text, page, section, defs, seen, context=None, other_pages_only=False):
    """Link the first mentions of items in a text that are not in seen; return (text, [names linked]).

    With other_pages_only, items defined on the page itself stay plain.
    """
    linked_spans = []
    for match in LINK.finditer(text):
        linked_spans.append((match.start(), match.end()))
        seen.update(CODE_NAME.findall(match.group(1)))
    result, added, last = [], [], 0
    for match in CODE_NAME.finditer(text):
        name = match.group(1)
        if any(a <= match.start() < b for a, b in linked_spans) or name in seen:
            continue
        if other_pages_only and any(c[0] == page for c in defs.get(name, [])):
            continue
        before, after = unlinked(text[:match.start()]), text[match.end():]
        if PRODUCT_TYPE_BEFORE.search(before) or before.count('"') % 2:
            # A product type, such as relative_roughness, or a name quoted as text.
            continue
        global_attribute = after.startswith(" global attribute") or bool(GLOBAL_ATTRIBUTES_BEFORE.search(before))
        kind = next((k for k, pattern in KIND_WORDS.items() if pattern[0].search(before) or pattern[1].match(after)), None)
        found = target(name, page, section, defs, global_attribute, context, kind)
        if found is None:
            continue
        seen.add(name)
        result.append(text[last:match.start()])
        result.append(f"[`{name}`]({href(page, found[0], found[1])})")
        last = match.end()
        added.append(name)
    result.append(text[last:])
    return "".join(result), added


def annex_context(lines, products):
    """Return the context of target() for a product page of the annex, or None for other pages."""
    match = CATEGORY_LINK.search("\n".join(lines))
    if not match or match.group(1) not in products:
        return None
    category = f"contents/product_types/{match.group(2)}.md"
    scopes = {}
    for section, scope in SECTION_SCOPES.get(category, {}).items():
        if scope == "level 2":
            scope = {p for p, (page, _, level) in products.items() if page == category and level.startswith("L2")}
        scopes[section] = scope
    return match.group(1), category, scopes


def link_page(page, lines, defs, products):
    """Return the lines of a page with the missing links added, and [(line number, name)] of the links added.

    In the definition tables, the first mention per row of an item of another table is linked;
    in the text, the first mention per section (##) of an item defined on another page.
    """
    out, added = list(lines), []
    sections, section, code = [], None, False
    for line in lines:
        if line.startswith("```"):
            code = not code
        match = HEADING.match(line)
        if match and not code and len(match.group(1)) == 2:
            section = slug(match.group(2))
        sections.append(section)
    for start, end, kind in tables(lines):
        if kind not in DEFINITION_TABLES:
            continue
        own_table = {m.group(1) for m in (re.match(r"\| `(\w+)`", line) for line in lines[start:end + 1]) if m}
        for i in range(start + 2, end + 1):
            cells = lines[i].split("|")
            # The row's own item and the items of its table are not linked, nor names already linked.
            description, names = link_line(cells[-2], page, sections[i], defs, set(own_table))
            cells[-2] = description
            out[i] = "|".join(cells)
            added += [(i + 1, name) for name in names]
    context = annex_context(lines, products)
    seen, code, front = set(), False, lines[:1] == ["---"]
    for i, line in enumerate(out):
        if front:
            front = i == 0 or line != "---"
            continue
        if line.startswith("```"):
            code = not code
            continue
        heading = HEADING.match(line)
        if heading and not code:
            if len(heading.group(1)) <= 2:
                seen = set()
            continue
        if code or line.startswith(("|", "{:", "<")) or REFERENCE_DEFINITION.match(line) or not line.strip():
            continue
        out[i], names = link_line(line, page, sections[i], defs, seen, context, other_pages_only=True)
        added += [(i + 1, name) for name in names]
    return out, added


def convention_problems(page, lines):
    """Return [(line number, message)] for the links to the conventions that are not of the pinned version, or inline outside the References page."""
    problems = []
    for number, line in enumerate(lines, 1):
        for url in URL.findall(line):
            for start, allowed in CONVENTION_URLS.items():
                if url.startswith(start) and url.split("#")[0] not in allowed:
                    problems.append((number, f"{url} is not the URL of the version SOMaR pins ({' or '.join(allowed)})"))
        if page != REFERENCES:
            for match in LINK.finditer(line):
                if match.group(2).startswith(tuple(CONVENTION_URLS)):
                    problems.append((number, f"the link [{match.group(1)}] to a convention is inline; link it reference-style, as [{match.group(1)}][label]"))
    return problems


def text_problems(page, lines):
    """Return [(line number, message)] for the links whose text mixes code and words, such as [`x` attribute]."""
    problems, code = [], False
    for number, line in enumerate(lines, 1):
        if line.startswith("```"):
            code = not code
            continue
        if code:
            continue
        for match in LINK.finditer(line):
            text = match.group(1)
            if "`" in text and not re.fullmatch(r"`[^`]+`", text):
                problems.append((number, f"the link text [{text}] mixes code and words; link each name on its own, as [`name`](...)"))
    return problems


def resolved(page, url):
    """Return the target of a link as (page, fragment), with the path resolved against the page."""
    if re.match(r"https?://", url):
        return tuple(url.split("#", 1)) if "#" in url else (url, "")
    path, _, fragment = url.partition("#")
    destination = posixpath.normpath(posixpath.join(posixpath.dirname(page), path)) if path else page
    if destination.endswith("/") or not posixpath.splitext(destination)[1]:
        destination = posixpath.join(destination, "index.md")
    return destination, fragment


def repeat_problems(page, lines):
    """Return [(line number, message)] for a link in the text to a target that the same section (##) already links to.

    Citations, each a reference of its own, and tables, which follow the rule of the
    definition tables, are left out.
    """
    labels = {m.group(1): m.group(2) for m in map(REFERENCE_DEFINITION.match, lines) if m}
    problems, seen, code = [], {}, False
    for number, line in enumerate(lines, 1):
        if line.startswith("```"):
            code = not code
            continue
        heading = HEADING.match(line)
        if heading and not code and len(heading.group(1)) <= 2:
            seen = {}
            continue
        if code or line.startswith("|") or REFERENCE_DEFINITION.match(line):
            continue
        links = [(m.start(), m.group(1), m.group(2)) for m in LINK.finditer(line)]
        links += [(m.start(), m.group(1), labels.get(m.group(2) or m.group(1), "")) for m in REFERENCE_LINK.finditer(line)]
        for _, text, url in sorted(links):
            if not url or "references/index.md" in url:
                continue
            key = resolved(page, url)
            if key in seen:
                problems.append((number, f"the link [{text}] repeats the link of line {seen[key]} to the same target in this section"))
            else:
                seen[key] = number
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="list the missing links and fail if there are any")
    args = parser.parse_args()
    paths = [os.path.join(ROOT, "index.md")] + sorted(glob.glob(os.path.join(ROOT, "contents/**/*.md"), recursive=True))
    pages = {os.path.relpath(p, ROOT): open(p, encoding="utf-8").read().split("\n") for p in paths}
    defs = definitions(pages)
    products = registry()
    problems = 0
    for page, lines in pages.items():
        out, added = link_page(page, lines, defs, products)
        if args.check:
            found = [(number, f"`{name}` is not linked to its definition") for number, name in added]
        else:
            found = []
            if added:
                with open(os.path.join(ROOT, page), "w", encoding="utf-8") as f:
                    f.write("\n".join(out))
                print(f"{page}: {len(added)} links added")
        # The problems that the script reports but does not fix.
        found += convention_problems(page, out) + text_problems(page, out) + repeat_problems(page, out)
        for number, message in sorted(found):
            print(f"{page}:{number}: {message}")
        problems += len(found)
    print(f"{problems} problems found")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
