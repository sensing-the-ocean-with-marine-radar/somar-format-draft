#!/usr/bin/env python3
"""Link the names in the definition tables to the rows of the other tables that define them.

Every row of an attribute or variable table has an id (see _plugins/table_rows.rb):
the name of its item where that name heads only one row of the page and is no
heading id there, and otherwise the id of the nearest preceding heading and the
name. In the description, the last column, of each row of these tables, the
first mention of an item, written as `name`, links to its row if that row is in
another table, on the same page or another; the later mentions in the row, the
items of the row's own table, and the other columns stay plain, and so does the
prose of the pages.

A name that more than one row defines links to the row on its own page,
preferring the row of the current section; for comment, source, and references
outside the pages of the global attributes, to the variable attributes, unless
"global attribute" follows the name; for a
variable defined both under Product variables and on a category page, to
Product variables; and otherwise it stays plain.

Usage: python3 scripts/link_items.py [--check]

Without --check, the script adds the missing links to the pages; with --check,
it lists them and fails if there are any, as CI runs it.
"""

import argparse
import glob
import os
import posixpath
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFINITION_TABLES = ("attribute-table", "variable-table", "mandatory-attribute-table")
HEADING = re.compile(r"^(#{1,6}) (.*)$")
CODE_NAME = re.compile(r"`(\w+)`")
# A Markdown link, whose text may hold code spans.
LINK = re.compile(r"\[((?:[^\[\]]|`[^`]*`)*)\]\(([^)\s]*)\)")
PRODUCT_VARIABLES = "contents/product_types/product_variables.md"
VARIABLE_ATTRIBUTES = "contents/metadata_attributes/variable_attributes.md"
# The names of both a global and a variable attribute, and the pages on which they mean the global one.
GLOBAL_AND_VARIABLE_ATTRIBUTES = ("comment", "references", "source")
GLOBAL_ATTRIBUTE_PAGES = ("contents/metadata_attributes/mandatory_global.md", "contents/metadata_attributes/optional_global.md")


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
    """Return [(row id, name, section id, h2 section id)] for the definition rows of a page, as table_rows.rb assigns the ids."""
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
            rows.append((match.group(1), heading, section))
    counts = {}
    for name, _, _ in rows:
        counts[name] = counts.get(name, 0) + 1
    return [(name if counts[name] == 1 and name not in headings else f"{h}-{name}", name, h, s) for name, h, s in rows]


def definitions(pages):
    """Return {name: [(page, row id, h2 section id)]} for all definition rows."""
    found = {}
    for page, lines in pages.items():
        for row_id, name, _, section in page_rows(lines):
            found.setdefault(name, []).append((page, row_id, section))
    return found


def target(name, page, section, defs, global_attribute=False):
    """Return (page, row id) that a mention of name links to, or None if it is ambiguous.

    global_attribute is true for a mention followed by "global attribute".
    """
    candidates = defs.get(name, [])
    if not candidates:
        return None
    own = [c for c in candidates if c[0] == page]
    if len(own) == 1:
        return own[0][:2]
    if own:
        here = [c for c in own if c[2] == section]
        return here[0][:2] if len(here) == 1 else None
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


def link_line(text, page, section, defs, seen):
    """Link the first mentions of items in a text that are not in seen; return (text, [names linked])."""
    linked_spans = []
    for match in LINK.finditer(text):
        linked_spans.append((match.start(), match.end()))
        seen.update(CODE_NAME.findall(match.group(1)))
    result, added, last = [], [], 0
    for match in CODE_NAME.finditer(text):
        name = match.group(1)
        if any(a <= match.start() < b for a, b in linked_spans) or name in seen:
            continue
        found = target(name, page, section, defs, text[match.end():].startswith(" global attribute"))
        if found is None:
            continue
        seen.add(name)
        result.append(text[last:match.start()])
        result.append(f"[`{name}`]({href(page, found[0], found[1])})")
        last = match.end()
        added.append(name)
    result.append(text[last:])
    return "".join(result), added


def link_page(page, lines, defs):
    """Return the lines of a page with the missing links added, and [(line number, name)] of the links added."""
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
    return out, added


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="list the missing links and fail if there are any")
    args = parser.parse_args()
    paths = sorted(glob.glob(os.path.join(ROOT, "contents/**/*.md"), recursive=True))
    pages = {os.path.relpath(p, ROOT): open(p, encoding="utf-8").read().split("\n") for p in paths}
    defs = definitions(pages)
    missing = 0
    for page, lines in pages.items():
        out, added = link_page(page, lines, defs)
        missing += len(added)
        if args.check:
            for number, name in added:
                print(f"{page}:{number}: `{name}` is not linked to its definition")
        elif added:
            with open(os.path.join(ROOT, page), "w", encoding="utf-8") as f:
                f.write("\n".join(out))
            print(f"{page}: {len(added)} links added")
    if args.check:
        print(f"{missing} mentions without a link")
        sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
