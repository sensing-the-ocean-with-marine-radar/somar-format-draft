#!/usr/bin/env python3
"""Build and check the CDL examples of the SOMaR specification.

Every fenced code block in contents/**/*.md is checked unless its first line
is "// excerpt":

- Blocks starting with "netcdf" are built as they are; blocks starting with
  "dimensions:", "variables:", "group:", or "// global attributes:" are
  wrapped in a "netcdf fragment { ... }" first.
- Placeholders of the form "group: <name> { ... }" are replaced by the
  canonical group of that name, taken from the examples on the Metadata pages.
- Dimension lengths are capped at 3 so that the built files stay small; the
  data sections of the examples must therefore hold scalars only.

Each block is built with "ncgen -k nc4" and its "ncdump" output checked
against the pinned CF standard name table, UDUNITS (through cf-units), CF
scoping rules for references between variables and for the names of a
coordinate reference system, the CF syntax of cell_methods, the dimensions
and units of bounds variables, and the SOMaR rules for global attributes and
file names, among them that a file whose structure is that of a moving
platform sets platform_is_mobile to "true" and that a Level 2 file that sets
it has that structure; the examples must carry the highly recommended global
attributes as well as the mandatory ones, and the variables that the product
variables they carry require (see product_variables.md). The spatial bounds
are checked against the positions the example gives: scalar latitude and
longitude values in the data sections and the projection origins of crs
variables.

A file must also hold the variables that its row in the product-type table
requires, and meet the conditional requirements of the category pages:
averaged_quantity on interpolated or averaged backscatter and on
relative_roughness, fixed_angle exactly in pointing sweeps, a crs on the local
grid of a Level 2 product and in Cartesian images from a fixed platform only,
the platform velocity exactly for platform-fixed analysis windows, and the
coordinates attribute of the data variables of a discrete sampling geometry.
The attribute tables, and the variable tables of the Metadata pages and of
product_variables.md, must be in alphabetical order, and the product types
listed in mandatory_global.md, the product-type tables, the index of the
product types, the file naming page, and the annex must be the same.

The values of an example must agree with each other: the file name with
time_coverage_start, time_coverage_start with the start of the earliest
time_<YYYYMMDDHHMMSS> group, each such group name with its time and
time_iso_8601, time_iso_8601 with the value of time, time_coverage_end with
the start, the flags of a flag variable with its valid_range, and the spatial
bounds with the extent of a geographic grid of analysis windows, from the
dimension lengths as written and analysis_window_spacing.

Items that a file may omit are marked by a trailing comment with their tier
("// highly recommended", "// recommended", or "// optional"). The markers
of global attributes and variables are checked against the tables of the
global attribute pages, the processing parameters, and the page of the
example; for a product, against the tables of its category page and its row
in the product-type table there instead. The markers of variable attributes
are checked against the attribute tables of variable_attributes.md and the
category pages, and those of groups against GROUP_TIERS. Each file example is also checked
in its minimal form, without the marked items; a block whose first line is
"// minimal form" must equal the minimal form of the example with the same
"netcdf" name.

Usage: python3 scripts/check_examples.py [--strict]

Without cf-units installed, the unit checks are skipped with a warning;
--strict makes that an error.
"""

import argparse
import datetime
import glob
import math
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDARD_NAME_TABLE_VERSION = 95
STANDARD_NAME_TABLE_URL = (
    "https://cfconventions.org/Data/cf-standard-names/"
    f"{STANDARD_NAME_TABLE_VERSION}/src/cf-standard-name-table.xml"
)
DIMENSION_CAP = 3
# Units the specification allows but UDUNITS does not define.
EXTRA_UNITS = {"dB"}
# The backscatter variables of the Level 1 products, of which a file holds exactly one.
LEVEL1_DATA_VARIABLES = {"backscatter_amplitude", "backscatter_power"}
GEOSPATIAL_ATTRIBUTES = ("geospatial_lat_min", "geospatial_lat_max", "geospatial_lon_min", "geospatial_lon_max")
FILE_NAME = re.compile(
    r"^(?P<station>[a-z0-9]+)_(?P<date>\d{4}-\d{2}-\d{2})-(?P<hour>\d{2})(?:-(?P<minute>\d{2}))?_"
    r"(?P<product>[a-z0-9_]+)$"
)
FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.M | re.S)
PLACEHOLDER = re.compile(r"^(\s*)group: (\w+) \{ \.\.\. \}.*$", re.M)
# CDL lines, as written in the examples.
DECLARATION = re.compile(r"^\s*(?:char|byte|ubyte|short|ushort|int|uint|int64|uint64|float|double|string) (\w+)(?:\(.*\))? ;")
ATTRIBUTE = re.compile(r"^(\s*(?:string )?(\w*):(\w+) = )(.*?) ;")
GROUP_OPEN = re.compile(r"^\s*group: (\w+) \{")
GROUP_CLOSE = re.compile(r"^\s*\} // group (\w+)")
# The tier with which a trailing comment marks an item that a minimal file may omit.
# "required" marks an item that the tables recommend but the minimal file keeps.
TIER = re.compile(r"(highly recommended|recommended|optional|required)\b")
OMITTED_TIERS = ("highly recommended", "recommended", "optional")
# The pages of the Level 2 categories, whose product-type tables list the Level 2 products.
CATEGORY_PAGES = ("contents/product_types/polar.md", "contents/product_types/gridded.md", "contents/product_types/spatially_averaged.md")
PRODUCT_TYPE = re.compile(r':product_type = "(\w+)"')
# The rules of the product variables: "Carried together with `x`." and "Requires `x`." (see product_variables.md).
VARIABLE_RULE = re.compile(r"(?:Carried together with|Requires) ((?:`\w+`(?:,? and |, )?)+)\.")
# The names of a coordinate reference system, which CF requires all together if any is given (Appendix F).
CRS_NAMES = ("reference_ellipsoid_name", "prime_meridian_name", "horizontal_datum_name", "geographic_crs_name")
# Recommended global attributes that a file must carry under a condition stated in their description,
# such as platform_is_mobile from a moving platform; their tier is not checked.
CONDITIONAL_ATTRIBUTES = ("platform_is_mobile",)
# The methods of cell_methods (CF Appendix E) and one of its entries: names, a method, and qualifiers (CF 7.3).
CELL_METHODS = {"point", "sum", "maximum", "maximum_absolute_value", "median", "mid_range", "minimum",
                "minimum_absolute_value", "mean", "mean_absolute_value", "mean_of_upper_decile", "mode", "range",
                "root_mean_square", "standard_deviation", "sum_of_squares", "variance"}
CELL_METHOD = re.compile(r"((?:\w+:\s*)+)(\w+)((?:\s+(?:where|over|within)\s+\w+)*)(?:\s*\([^)]*\))?")
# Attributes whose references to omitted variables are dropped in the minimal form.
REFERENCE_ATTRIBUTES = ("grid_mapping", "ancillary_variables")
# The tiers of the groups that a file may omit, as stated in the text of their pages
# (polar.md, radar_parameters.md, georeference_correction.md, wave_calibration.md); other groups are required.
GROUP_TIERS = {"georeference": "recommended", "radar_parameters": "optional",
               "georeference_correction": "optional", "wave_calibration": "recommended"}
# The pages whose attribute tables give the tiers of variable attributes.
VARIABLE_ATTRIBUTE_PAGES = ("contents/metadata_attributes/variable_attributes.md",) + CATEGORY_PAGES
# The pages whose variable tables, as well as their attribute tables, are in alphabetical order
# (see metadata_attributes/index.md#reading-the-tables).
ALPHABETICAL_VARIABLE_PAGES = ("contents/metadata_attributes/", "contents/product_types/product_variables.md")
# Meters per degree of latitude, and of longitude at the equator, for the extent of geographic grids.
METERS_PER_DEGREE = 111320.0
# The variables of a discrete sampling geometry that are not data variables.
DSG_COORDINATES = {"time", "time_bounds", "longitude", "latitude", "trajectory", "station"}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def config_value(key):
    match = re.search(rf'^{key}:\s*"?([^"\n]+?)"?\s*$', read(os.path.join(ROOT, "_config.yml")), re.M)
    if not match:
        sys.exit(f"_config.yml has no {key}")
    return match.group(1)


def product_types():
    text = read(os.path.join(ROOT, "contents/metadata_attributes/mandatory_global.md"))
    row = next(line for line in text.splitlines() if line.startswith("| `product_type`"))
    return set(re.findall(r"`([a-z0-9_]+)`", row.split("|")[2]))


def mandatory_attributes():
    text = read(os.path.join(ROOT, "contents/metadata_attributes/mandatory_global.md"))
    return [re.match(r"\| `(\w+)`", line).group(1) for line in text.splitlines() if line.startswith("| `")]


def recommended_global_section(heading):
    text = read(os.path.join(ROOT, "contents/metadata_attributes/optional_global.md"))
    section = text.split(f"\n## {heading}\n", 1)[1].split("\n## ", 1)[0]
    return [re.match(r"\| `(\w+)`", line).group(1) for line in section.splitlines() if line.startswith("| `")]


def highly_recommended_attributes():
    return recommended_global_section("Highly recommended")


def table_tiers(text, strict=True):
    """Return {name: tier} for the table rows whose description starts with a tier.

    With strict, only "Required.", "Recommended.", or "Optional." count; otherwise the
    word alone does, as in "Recommended for map products". Names listed with different
    tiers in different rows are left out.
    """
    tiers, conflicts = {}, set()
    pattern = r"\s*(Required|Recommended|Optional)" + (r"\." if strict else r"\b")
    for line in text.splitlines():
        if not line.startswith("| `"):
            continue
        cells = line.strip().strip("|").split("|")
        match = re.match(pattern, cells[-1])
        if not match:
            continue
        for name in re.findall(r"`(\w+)`", cells[0].split("<br>")[0]):
            if tiers.get(name, match.group(1).lower()) != match.group(1).lower():
                conflicts.add(name)
            tiers[name] = match.group(1).lower()
    return {name: tier for name, tier in tiers.items() if name not in conflicts}


def registry():
    """Return {product_type: (category page, {name: tier}, level)} from the product-type tables of the categories.

    The tiers are those of the "**Required:**", "**Recommended:**", and "**Optional:**" lines of a row,
    and the level, such as "L1a", is given in parentheses after the name of the product.
    """
    products = {}
    for page in CATEGORY_PAGES:
        for line in read(os.path.join(ROOT, page)).splitlines():
            if not (line.startswith("| [") and ":**" in line):
                continue
            cells = line.strip().strip("|").split("|")
            tiers = {}
            for part in cells[2].split("<br>"):
                match = re.match(r"\s*\*\*(Required|Recommended|Optional):\*\*(.*)", part)
                if match:
                    tiers.update((name, match.group(1).lower()) for name in re.findall(r"`(\w+)`", match.group(2)))
            level = re.search(r"\((L\d[a-z])\)\s*$", cells[0]).group(1)
            products[re.search(r"`(\w+)`", cells[1]).group(1)] = (page, tiers, level)
    return products


def table_blocks(text):
    """Yield (line number, class, [names]) for each table of a page, with the class given below it."""
    names, start = [], None
    for number, line in enumerate(text.splitlines() + [""], 1):
        match = re.match(r"\| `(\w+)`", line)
        if match:
            start = start or number
            names.append(match.group(1))
        elif line.startswith("{: .") and names:
            yield start, line.strip()[4:-2].strip(), names
            names, start = [], None
        elif not line.startswith("|"):
            names, start = [], None


def attribute_tiers():
    """Return {attribute: tier} for the variable attributes whose description starts with a tier."""
    tiers = {}
    for page in VARIABLE_ATTRIBUTE_PAGES:
        text = read(os.path.join(ROOT, page))
        rows = [line for line in text.splitlines() if line.startswith("| `")]
        attribute_rows = set()
        for start, kind, names in table_blocks(text):
            if kind == "attribute-table":
                attribute_rows.update(names)
        tiers.update(table_tiers("\n".join(row for row in rows if re.match(r"\| `(\w+)`", row).group(1) in attribute_rows), strict=False))
    return tiers


def product_type_lists():
    """Return {page: set of product types} for the pages that list all product types besides mandatory_global.md."""
    lists = {}
    index = read(os.path.join(ROOT, "contents/product_types/index.md"))
    lists["contents/product_types/index.md"] = {re.findall(r"`(\w+)`", line.split("|")[4])[0] for line in index.splitlines() if line.startswith("| **L")}
    naming = read(os.path.join(ROOT, "contents/file_naming/index.md"))
    lists["contents/file_naming/index.md"] = set(re.findall(r"^\| `\w+?_[0-9-]+_(\w+)\.nc`", naming, re.M))
    lists["contents/annex/*.md"] = {match.group(1) for page in glob.glob(os.path.join(ROOT, "contents/annex/*.md"))
                                    for match in [re.search(r"The product type `(\w+)`", read(page))] if match}
    return lists


def check_table_order(relative, text):
    """Check that the attribute tables, and the variable tables of some pages, are in alphabetical order."""
    errors = []
    for start, kind, names in table_blocks(text):
        alphabetical = kind == "attribute-table" or (kind == "variable-table" and relative.startswith(ALPHABETICAL_VARIABLE_PAGES))
        if alphabetical and names != sorted(names, key=str.lower):
            first = next(a for a, b in zip(names, sorted(names, key=str.lower)) if a != b)
            errors.append(f"the {kind} at line {start} is not in alphabetical order (first out of place: {first})")
    return errors


def global_tiers():
    """Return {name: tier} for the shared global attributes and the processing parameters."""
    tiers = {name: "required" for name in mandatory_attributes()}
    tiers.update((name, "highly recommended") for name in highly_recommended_attributes())
    tiers.update((name, "recommended") for name in recommended_global_section("Recommended") if name not in CONDITIONAL_ATTRIBUTES)
    tiers.update(table_tiers(read(os.path.join(ROOT, "contents/metadata_attributes/processing_parameters.md")), strict=False))
    return tiers


def variable_rules():
    """Return {variable: [variables it requires]} from the descriptions in product_variables.md."""
    rules = {}
    for line in read(os.path.join(ROOT, "contents/product_types/product_variables.md")).splitlines():
        if not line.startswith("| `"):
            continue
        cells = line.strip().strip("|").split("|")
        name = re.match(r"\s*`(\w+)`", cells[0]).group(1)
        for match in VARIABLE_RULE.finditer(cells[-1]):
            rules.setdefault(name, []).extend(re.findall(r"`(\w+)`", match.group(1)))
    return rules


def canonical_groups():
    groups = {}
    for path in glob.glob(os.path.join(ROOT, "contents/metadata_attributes/*.md")):
        for block in FENCE.findall(read(path)):
            match = re.match(r"group: (\w+) \{\n", block)
            if match:
                groups[match.group(1)] = block
    return groups


def standard_name_table():
    cache = os.path.join(tempfile.gettempdir(), f"cf-standard-name-table-{STANDARD_NAME_TABLE_VERSION}.xml")
    if not os.path.exists(cache):
        urllib.request.urlretrieve(STANDARD_NAME_TABLE_URL, cache)
    root = ET.parse(cache).getroot()
    entries = {e.get("id"): (e.findtext("canonical_units") or "").strip() for e in root.iter("entry")}
    aliases = {a.get("id"): a.findtext("entry_id") for a in root.iter("alias")}
    return entries, aliases


def cap_dimensions(cdl):
    lines, in_dimensions = [], False
    for line in cdl.splitlines():
        stripped = line.strip()
        if stripped == "dimensions:":
            in_dimensions = True
        elif stripped in ("variables:", "data:") or stripped.startswith("group:") or stripped.startswith("}"):
            in_dimensions = False
        elif in_dimensions:
            line = re.sub(r"= (\d+) ;", lambda m: f"= {min(int(m.group(1)), DIMENSION_CAP)} ;", line)
        lines.append(line)
    return "\n".join(lines) + "\n"


def prepare(block, groups):
    """Return the buildable CDL for a code block, or None if it is not checked."""
    first = block.lstrip().splitlines()[0] if block.strip() else ""
    if first.startswith("// excerpt"):
        return None
    if first.startswith("netcdf "):
        cdl = block
    elif first.startswith(("dimensions:", "variables:", "group:", "// global attributes:")):
        cdl = "netcdf fragment {\n" + block + "}\n"
    else:
        return None

    def expand(match):
        indent, name = match.groups()
        if name not in groups:
            raise ValueError(f'no canonical example for placeholder "group: {name} {{ ... }}"')
        return "".join(indent + line + "\n" for line in groups[name].splitlines())

    return cap_dimensions(PLACEHOLDER.sub(expand, cdl))


def comment(line):
    """Return the text of the line's trailing CDL comment, ignoring "//" inside strings."""
    in_string = False
    for i, char in enumerate(line):
        if char == '"' and line[i - 1 : i] != "\\":
            in_string = not in_string
        elif not in_string and line.startswith("//", i):
            return line[i + 2 :].strip()
    return ""


def tier(line):
    match = TIER.match(comment(line))
    return match.group(1) if match else None


def minimal(block):
    """Return the minimal form of an example: the block without the items marked as omissible.

    A marked placeholder or group is dropped whole, a marked variable with its attributes
    and data, and a marked attribute alone. References to dropped variables in
    REFERENCE_ATTRIBUTES are removed with them; others are kept, so that dropping a variable
    that something still refers to fails the check.
    """
    lines, dropped, stack, section, skip = [], set(), ["/"], None, None
    for line in block.splitlines():
        omitted = tier(line) in OMITTED_TIERS
        if skip is not None:
            match = GROUP_CLOSE.match(line)
            if match and match.group(1) == skip:
                skip = None
            continue
        if PLACEHOLDER.match(line):
            if not omitted:
                lines.append(line)
            continue
        match = GROUP_OPEN.match(line)
        if match:
            if omitted:
                skip = match.group(1)
                continue
            stack.append(stack[-1].rstrip("/") + "/" + match.group(1))
            section = None
        elif GROUP_CLOSE.match(line):
            stack.pop()
        elif line.strip() in ("dimensions:", "variables:", "data:"):
            section = line.strip()
        elif DECLARATION.match(line):
            if omitted:
                dropped.add((stack[-1], DECLARATION.match(line).group(1)))
                continue
        elif ATTRIBUTE.match(line):
            if omitted or (stack[-1], ATTRIBUTE.match(line).group(2)) in dropped:
                continue
        elif section == "data:" and re.match(r"^\s*(\w+) = ", line):
            if (stack[-1], re.match(r"^\s*(\w+) = ", line).group(1)) in dropped:
                continue
        lines.append(line)
    declared = {DECLARATION.match(line).group(1) for line in lines if DECLARATION.match(line)}
    gone = {name for _, name in dropped} - declared
    result = []
    for line in lines:
        match = ATTRIBUTE.match(line)
        if match and match.group(3) in REFERENCE_ATTRIBUTES:
            names = unquote(match.group(4)).split()
            kept = [name for name in names if name not in gone]
            if not kept:
                continue
            if kept != names:
                line = f'{match.group(1)}"{" ".join(kept)}" ;'
        result.append(line)
    return "\n".join(result) + "\n"


def check_tiers(block, tiers, variable_attribute_tiers):
    """Check the tier markers of global attributes, variables, variable attributes, and groups against the tables."""
    errors = []
    for number, line in enumerate(block.lstrip().splitlines()):
        match = ATTRIBUTE.match(line)
        # A block that is a group on its own, as on the Metadata pages, has no tier for it.
        group = number > 0 and (GROUP_OPEN.match(line) or PLACEHOLDER.match(line))
        if match and match.group(2) == "":
            kind, name, expected = "global attribute", match.group(3), tiers.get(match.group(3))
        elif match:
            kind, name, expected = "attribute", f"{match.group(2)}:{match.group(3)}", variable_attribute_tiers.get(match.group(3))
        elif DECLARATION.match(line):
            kind, name = "variable", DECLARATION.match(line).group(1)
            expected = tiers.get(name)
        elif group:
            kind, name = "group", group.group(group.lastindex)
            expected = GROUP_TIERS.get(name, "required")
        else:
            continue
        marked = tier(line) or "required"
        if expected is None or marked == expected or (marked == "required" and expected == "recommended" and tier(line)):
            continue
        errors.append(f'{kind} {name} is marked as {marked}, but the tables make it {expected}')
    return errors


def parse_header(text):
    """Parse "ncdump" output into {group path: {"variables": {...}, "attributes": {...}, "data": {...}, "strings": {...}, "dimensions": {...}}}.

    "data" holds the values of variables whose data section gives a single number, "strings"
    those whose data section gives a single string, and "dimensions" the dimension names of
    each variable.
    """
    groups = {"/": {"variables": {}, "attributes": {}, "data": {}, "strings": {}, "dimensions": {}}}
    stack = ["/"]
    section = None
    for line in text.splitlines():
        stripped = line.strip()
        match = re.match(r"group: (\w+) \{$", stripped)
        if match:
            path = stack[-1].rstrip("/") + "/" + match.group(1)
            groups[path] = {"variables": {}, "attributes": {}, "data": {}, "strings": {}, "dimensions": {}}
            stack.append(path)
            section = None
            continue
        if stripped.startswith("} // group"):
            stack.pop()
            continue
        if stripped in ("dimensions:", "variables:", "data:"):
            section = stripped
            continue
        group = groups[stack[-1]]
        if section == "data:":
            match = re.match(r"^(\w+) = (-?[0-9.]+(?:e[-+]?\d+)?) ;$", stripped)
            if match:
                group["data"][match.group(1)] = float(match.group(2))
            match = re.match(r'^(\w+) = "(.*)" ;$', stripped)
            if match:
                group["strings"][match.group(1)] = match.group(2)
            continue
        match = re.match(r"^(?:string )?(\w*):(\w+) = (.*) ;$", stripped)
        if match:
            variable, attribute, value = match.groups()
            target = group["attributes"] if variable == "" else group["variables"].setdefault(variable, {})
            target[attribute] = value
            continue
        match = re.match(r"^\w+ (\w+)(?:\((.*)\))? ;$", stripped)
        if match:
            group["variables"].setdefault(match.group(1), {})
            group["dimensions"][match.group(1)] = tuple(d.strip() for d in (match.group(2) or "").split(",") if d.strip())
    return groups


def number(value):
    """Return the number in an ncdump attribute value such as "15.03" or "15.03f", or None."""
    match = re.fullmatch(r"(-?[0-9.]+(?:e[-+]?\d+)?)[a-zA-Z]*", value or "")
    return float(match.group(1)) if match else None


def positions(groups):
    """Yield the known positions that the spatial bounds must enclose (see optional_global.md).

    These are the scalar latitude and longitude values in the data sections and, in groups
    without latitude and longitude variables, the projection origin of the crs variable.
    """
    for path, group in groups.items():
        if "latitude" in group["variables"] or "longitude" in group["variables"]:
            if "latitude" in group["data"] and "longitude" in group["data"]:
                yield path, group["data"]["latitude"], group["data"]["longitude"]
        elif "crs" in group["variables"]:
            crs = group["variables"]["crs"]
            latitude = number(crs.get("latitude_of_projection_origin"))
            longitude = number(crs.get("longitude_of_projection_origin"))
            if latitude is not None and longitude is not None:
                yield path, latitude, longitude


def moving_structure(groups):
    """Whether a file has the structure of a moving platform.

    That is time-bounded grids (groups named time_<YYYYMMDDHHMMSS>), georeference
    subgroups, or a longitude that varies with time.
    """
    for path, group in groups.items():
        name = path.rsplit("/", 1)[-1]
        if re.fullmatch(r"time_\d{14}", name) or name == "georeference":
            return True
        if "time" in group["dimensions"].get("longitude", ()):
            return True
    return False


def check_bounds(groups):
    root = groups["/"]["attributes"]
    bounds = {a: number(root.get(a)) for a in GEOSPATIAL_ATTRIBUTES}
    invalid = [a for a, value in bounds.items() if value is None and a in root]
    if invalid:
        return [f"{', '.join(invalid)} not numeric"]
    if None in bounds.values():
        return []
    lat_min, lat_max, lon_min, lon_max = (bounds[a] for a in GEOSPATIAL_ATTRIBUTES)
    errors = []
    if not -90 <= lat_min <= lat_max <= 90:
        errors.append("geospatial_lat_min and geospatial_lat_max must satisfy -90 <= min <= max <= 90")
    if not (-180 <= lon_min <= 180 and -180 <= lon_max <= 180):
        errors.append("geospatial_lon_min and geospatial_lon_max must lie between -180 and 180")
    for path, latitude, longitude in positions(groups):
        # Across the antimeridian, lon_min is greater than lon_max.
        inside = lon_min <= longitude <= lon_max if lon_min <= lon_max else longitude >= lon_min or longitude <= lon_max
        if not (lat_min <= latitude <= lat_max and inside):
            errors.append(f"position ({latitude}, {longitude}) in group {path} lies outside the geospatial bounds")
    return errors


def normalized(text):
    return [line.rstrip() for line in text.splitlines() if line.strip()]


def unquote(value):
    return value[1:-1] if value.startswith('"') and value.endswith('"') else value


def resolve(groups, path, name):
    """Return the path of the group that holds a variable, searching the group and its ancestors (CF 1.8 scoping), or None."""
    while True:
        if name in groups[path]["variables"]:
            return path
        if path == "/":
            return None
        path = path.rsplit("/", 1)[0] or "/"


def check_cell_methods(where, value, dimensions, coordinates):
    """Check a cell_methods value: entries of names and a CF method, whose names are dimensions of the
    variable, scalar coordinates listed in its coordinates attribute, or "area" (CF 7.3)."""
    if not re.fullmatch(rf"\s*(?:{CELL_METHOD.pattern}\s*)+", value):
        return [f'{where}: cell_methods "{value}" does not follow the CF syntax "name: method"']
    errors = []
    for match in CELL_METHOD.finditer(value):
        if match.group(2) not in CELL_METHODS:
            errors.append(f'{where}: cell_methods method "{match.group(2)}" is not a CF method')
        for name in re.findall(r"(\w+):", match.group(1)):
            if name not in dimensions and name not in coordinates and name != "area":
                errors.append(f'{where}: cell_methods names "{name}", which is neither a dimension nor a listed coordinate')
    return errors


def check_bounds_variable(groups, path, variable, name):
    """Check that a bounds variable has the dimensions of its variable plus one, and the same units and calendar (CF 7.1)."""
    errors, where = [], f"{path.rstrip('/')}/{variable}" if path != "/" else variable
    target = groups[resolve(groups, path, name)]
    dimensions, bounds_dimensions = groups[path]["dimensions"].get(variable, ()), target["dimensions"].get(name, ())
    if bounds_dimensions[:-1] != dimensions or len(bounds_dimensions) != len(dimensions) + 1:
        errors.append(f"{where}: bounds {name} has the dimensions ({', '.join(bounds_dimensions)}), expected those of {variable} and one more")
    for attribute in ("units", "calendar"):
        value = target["variables"][name].get(attribute)
        if value is not None and value != groups[path]["variables"][variable].get(attribute):
            errors.append(f"{where}: bounds {name} has {attribute} {value}, which differs from that of {variable}")
    return errors


def anywhere(groups, name):
    """Whether any group holds a variable of that name."""
    return any(name in group["variables"] for group in groups.values())


def check_rules(groups, is_file, expected):
    """Check the conditional requirements of the category pages and the required variables of a product."""
    errors = []
    root = groups["/"]["attributes"]
    product = unquote(root.get("product_type", ""))
    for path, group in groups.items():
        for variable, attributes in group["variables"].items():
            where = f"{path.rstrip('/')}/{variable}" if path != "/" else variable
            # averaged_quantity: on resampled or averaged backscatter and on relative_roughness (variable_attributes.md).
            method = unquote(attributes.get("azimuth_regularization", attributes.get("cartesian_resampling", "")))
            averaged = (method and method != "nearest_neighbor") or variable == "relative_roughness" or (
                variable in LEVEL1_DATA_VARIABLES and "time: mean" in unquote(attributes.get("cell_methods", "")))
            if averaged and "averaged_quantity" not in attributes:
                errors.append(f"{where}: is interpolated or averaged but has no averaged_quantity")
            # The data variables of a discrete sampling geometry name their coordinates (spatially_averaged.md).
            if "featureType" in root and "time" in group["dimensions"].get(variable, ()) and variable not in DSG_COORDINATES \
                    and unquote(attributes.get("coordinates", "")).split() != ["time", "longitude", "latitude"]:
                errors.append(f'{where}: a variable of a discrete sampling geometry needs coordinates = "time longitude latitude"')
        # fixed_angle is required in pointing sweeps and omitted otherwise (polar.md).
        pointing = group["strings"].get("sweep_mode") == "pointing"
        if pointing != ("fixed_angle" in group["variables"]):
            errors.append(f"{path}: fixed_angle is required if sweep_mode is \"pointing\" and omitted otherwise")
        # The local grid of a Level 2 product needs its crs (gridded.md).
        if product in expected["level2_product_types"] and {"x", "y"} <= group["variables"].keys() and not resolve(groups, path, "crs"):
            errors.append(f"{path}: a local grid needs a crs")
    if not is_file:
        return errors
    # Cartesian images carry a crs from a fixed platform only (gridded.md).
    if product == "radar_cartesian":
        fixed = groups["/"]["dimensions"].get("longitude") == ()
        if fixed != ("crs" in groups["/"]["variables"]):
            errors.append("Cartesian images need a crs from a fixed platform and none from a moving one")
    # Platform-fixed analysis windows require the platform velocity, which is omitted otherwise (spatially_averaged.md).
    platform_fixed = unquote(root.get("analysis_window_motion", "")) == "platform_fixed"
    for variable in ("platform_speed_wrt_ground", "platform_course"):
        if platform_fixed != anywhere(groups, variable):
            errors.append(f'{variable} is required if analysis_window_motion is "platform_fixed" and omitted otherwise')
    # The variables that the product-type table requires; of the Level 1 data variables, exactly one is checked above.
    for name, tier_of_name in expected["product_tiers"].get(product, {}).items():
        if tier_of_name == "required" and name not in LEVEL1_DATA_VARIABLES and not anywhere(groups, name):
            errors.append(f"misses {name}, which the product-type table requires for {product}")
    return errors


def raw_dimensions(cdl):
    """Return {group path: {dimension: length}} as written in a block, before the lengths are capped."""
    dimensions, stack, section = {"/": {}}, ["/"], None
    for line in cdl.splitlines():
        match = GROUP_OPEN.match(line)
        if match and not PLACEHOLDER.match(line):
            stack.append(stack[-1].rstrip("/") + "/" + match.group(1))
            dimensions[stack[-1]], section = {}, None
        elif GROUP_CLOSE.match(line):
            stack.pop()
        elif line.strip() in ("dimensions:", "variables:", "data:"):
            section = line.strip()
        elif section == "dimensions:":
            match = re.match(r"^\s*(\w+) = (\d+) ;", line)
            if match:
                dimensions[stack[-1]][match.group(1)] = int(match.group(2))
    return dimensions


def instant(value):
    """Return the datetime of an ISO 8601 string in UTC, or None."""
    try:
        return datetime.datetime.fromisoformat(unquote(value or "").replace("Z", "+00:00"))
    except ValueError:
        return None


def numbers(value):
    """Return the integers of an ncdump list such as "1UB, 2UB, 4UB"."""
    return [int(number) for number in re.findall(r"-?\d+", value or "")]


def length(dimensions, path, name):
    """Return the written length of a dimension, searching the group and its ancestors, or None."""
    while True:
        if name in dimensions.get(path, {}):
            return dimensions[path][name]
        if path == "/":
            return None
        path = path.rsplit("/", 1)[0] or "/"


def check_values(groups, is_file, expected):
    """Check that the times, flags, and spatial bounds of an example agree with each other."""
    errors = []
    root = groups["/"]["attributes"]
    starts = []
    for path, group in groups.items():
        name = re.fullmatch(r"time_(\d{14})", path.rsplit("/", 1)[-1])
        time = group["variables"].get("time", {})
        iso = instant(time.get("time_iso_8601"))
        value = group["data"].get("time")
        start = iso or (datetime.datetime.fromtimestamp(value, datetime.timezone.utc) if value is not None else None)
        # time_iso_8601 states the same instant as the value of time (variable_attributes.md).
        if iso and value is not None and abs(iso.timestamp() - value) > 0.001:
            errors.append(f"{path}: time_iso_8601 {iso.isoformat()} differs from the value of time")
        # A time-bounded grid is named after its start time (gridded.md).
        if name and start and start.strftime("%Y%m%d%H%M%S") != name.group(1):
            errors.append(f"{path}: the group is named after {name.group(1)}, but its time is {start.isoformat()}")
        if name and start:
            starts.append(start)
        # The flags of a flag variable lie within its valid range.
        for variable, attributes in group["variables"].items():
            valid = numbers(attributes.get("valid_range"))
            for attribute in ("flag_values", "flag_masks"):
                outside = [n for n in numbers(attributes.get(attribute)) if len(valid) == 2 and not valid[0] <= n <= valid[1]]
                if outside:
                    errors.append(f"{path.rstrip('/')}/{variable}: {attribute} {outside} lie outside valid_range")
    if not is_file:
        return errors
    first, last = instant(root.get("time_coverage_start")), instant(root.get("time_coverage_end"))
    # The file name gives the UTC date and hour, and the minute if any, at which the coverage begins (file_naming).
    match = FILE_NAME.match(expected["file_name"])
    if match and first:
        named = f"{match.group('date')}T{match.group('hour')}:{match.group('minute') or first.strftime('%M')}"
        if first.strftime("%Y-%m-%dT%H:%M") != named:
            errors.append(f'file name "{expected["file_name"]}" does not match time_coverage_start {first.isoformat()}')
    if first and last and last < first:
        errors.append("time_coverage_end lies before time_coverage_start")
    # The coverage begins with the first observation, the start of the earliest group (optional_global.md).
    if first and starts and abs(first.timestamp() - min(starts).timestamp()) > 0.001:
        errors.append(f"time_coverage_start {first.isoformat()} is not the start of the earliest group, {min(starts).isoformat()}")
    # A geographic grid of analysis windows spans (n - 1) spacings, which the spatial bounds must enclose.
    bounds = [number(root.get(a)) for a in GEOSPATIAL_ATTRIBUTES]
    spacing = number(root.get("analysis_window_spacing"))
    if None not in bounds and spacing:
        lat_min, lat_max, lon_min, lon_max = bounds
        for path, group in groups.items():
            if group["dimensions"].get("latitude") != ("latitude",) or group["dimensions"].get("longitude") != ("longitude",):
                continue
            n_lat, n_lon = length(expected["dimensions"], path, "latitude"), length(expected["dimensions"], path, "longitude")
            lat_span = (n_lat - 1) * spacing / METERS_PER_DEGREE
            lon_span = (n_lon - 1) * spacing / (METERS_PER_DEGREE * math.cos(math.radians((lat_min + lat_max) / 2)))
            if lat_max - lat_min < 0.99 * lat_span or (lon_max - lon_min) % 360 < 0.99 * lon_span:
                errors.append(f"{path}: the spatial bounds span less than the {n_lat} x {n_lon} grid of {spacing:g} m spacing "
                              f"({lat_span:.4f} degrees of latitude, {lon_span:.4f} of longitude)")
    return errors


def check_header(groups, is_file, names, units_module, expected, minimal_form=False):
    errors = []
    entries, aliases = names
    for path, group in groups.items():
        for variable, attributes in group["variables"].items():
            where = f"{path.rstrip('/')}/{variable}" if path != "/" else variable
            units = unquote(attributes["units"]) if "units" in attributes else None
            unit = None
            if units is not None and units_module and units not in EXTRA_UNITS:
                try:
                    unit = units_module.Unit(units)
                except ValueError:
                    errors.append(f'{where}: units "{units}" are not recognized by UDUNITS')
            if "standard_name" in attributes:
                name = unquote(attributes["standard_name"])
                if name in aliases:
                    errors.append(f'{where}: standard_name "{name}" is an alias; use "{aliases[name]}"')
                elif name not in entries:
                    errors.append(f'{where}: standard_name "{name}" is not in CF standard name table v{STANDARD_NAME_TABLE_VERSION}')
                elif unit is not None and entries[name] not in ("", "1"):
                    canonical = units_module.Unit(entries[name])
                    if not (unit.is_convertible(canonical) or (unit.is_time_reference() and canonical.is_convertible(units_module.Unit("s")))):
                        errors.append(f'{where}: units "{units}" cannot be converted to "{entries[name]}", the canonical units of {name}')
            for attribute in ("bounds", "grid_mapping", "coordinates", "ancillary_variables"):
                for target in unquote(attributes.get(attribute, "")).split():
                    if not resolve(groups, path, target):
                        errors.append(f'{where}: {attribute} names "{target}", which does not exist in scope')
            if is_file:
                for required in expected["variable_rules"].get(variable, []):
                    if not resolve(groups, path, required):
                        errors.append(f"{where}: requires {required}, which does not exist in scope (see product_variables.md)")
            if "cell_methods" in attributes:
                errors += check_cell_methods(where, unquote(attributes["cell_methods"]), group["dimensions"].get(variable, ()), unquote(attributes.get("coordinates", "")).split())
            if "bounds" in attributes and resolve(groups, path, unquote(attributes["bounds"])):
                errors += check_bounds_variable(groups, path, variable, unquote(attributes["bounds"]))
            names = [name for name in CRS_NAMES if name in attributes]
            if names and len(names) < len(CRS_NAMES):
                errors.append(f"{where}: has {', '.join(names)} but not {', '.join(n for n in CRS_NAMES if n not in names)}, which CF requires together")
            meanings = unquote(attributes.get("flag_meanings", "")).split()
            for attribute in ("flag_values", "flag_masks"):
                if attribute in attributes and len(attributes[attribute].split(",")) != len(meanings):
                    errors.append(f"{where}: {attribute} and flag_meanings differ in length")
    errors += check_rules(groups, is_file, expected)
    errors += check_values(groups, is_file, expected)
    if is_file:
        root = groups["/"]["attributes"]
        missing = [a for a in expected["mandatory_attributes"] if a not in root]
        if missing:
            errors.append(f"missing mandatory global attributes: {', '.join(missing)}")
        # The examples model good practice, so they carry the highly recommended attributes too.
        missing = [a for a in expected["highly_recommended_attributes"] if a not in root]
        if missing and not minimal_form:
            errors.append(f"missing highly recommended global attributes: {', '.join(missing)}")
        errors += check_bounds(groups)
        conventions = unquote(root.get("Conventions", ""))
        if conventions != expected["conventions"]:
            errors.append(f'Conventions is "{conventions}", expected "{expected["conventions"]}"')
        product = unquote(root.get("product_type", ""))
        if product not in expected["product_types"]:
            errors.append(f'product_type "{product}" is not one of the product types in mandatory_global.md')
        mobile = unquote(root.get("platform_is_mobile", "")) == "true"
        moving = moving_structure(groups)
        if moving and not mobile:
            errors.append('has the structure of a moving platform, but platform_is_mobile is not "true"')
        elif mobile and not moving and product in expected["level2_product_types"]:
            errors.append('sets platform_is_mobile to "true", but has the structure of a fixed platform')
        if product in expected["level1_product_types"]:
            found = set().union(*(LEVEL1_DATA_VARIABLES & group["variables"].keys() for group in groups.values()))
            if len(found) != 1:
                errors.append(f"has {len(found)} Level 1 data variables; expected exactly one of {', '.join(sorted(LEVEL1_DATA_VARIABLES))}")
        match = FILE_NAME.match(expected["file_name"])
        if not match:
            errors.append(f'file name "{expected["file_name"]}" does not follow the naming pattern')
        elif match.group("product") != product:
            errors.append(f'file name "{expected["file_name"]}" does not match product_type "{product}"')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true", help="fail if cf-units is not installed")
    args = parser.parse_args()

    try:
        import cf_units as units_module
    except ImportError:
        if args.strict:
            sys.exit("cf-units is required with --strict (pip install cf-units)")
        print("warning: cf-units is not installed; skipping unit checks", file=sys.stderr)
        units_module = None

    groups = canonical_groups()
    names = standard_name_table()
    expected = {
        "conventions": f"CF-1.13, ACDD-1.3, SOMaR-{config_value('somar_version')}" + ("-draft" if config_value("somar_status") == "draft" else ""),
        "product_types": product_types(),
        "mandatory_attributes": mandatory_attributes(),
        "highly_recommended_attributes": highly_recommended_attributes(),
        "variable_rules": variable_rules(),
    }

    tiers = global_tiers()
    products = registry()
    category_tiers = {page: table_tiers(read(os.path.join(ROOT, page))) for page in CATEGORY_PAGES}
    expected["level1_product_types"] = {p for p, (_, _, level) in products.items() if level.startswith("L1")}
    expected["level2_product_types"] = {p for p, (_, _, level) in products.items() if level.startswith("L2")}
    expected["product_tiers"] = {p: row for p, (_, row, _) in products.items()}
    variable_attribute_tiers = attribute_tiers()
    lists = {"the product-type tables": set(products), **product_type_lists()}
    for where, listed in lists.items():
        if listed != expected["product_types"]:
            differences = sorted(listed ^ expected["product_types"])
            sys.exit(f"the product types of {where} differ from those in mandatory_global.md: {', '.join(differences)}")
    pages = sorted(glob.glob(os.path.join(ROOT, "contents/**/*.md"), recursive=True))
    # The examples by file name, from which the written-out minimal forms are derived.
    examples = {block.split()[1]: block for page in pages for block in FENCE.findall(read(page)) if block.startswith("netcdf ")}

    failures = checked = minimal_forms = 0
    with tempfile.TemporaryDirectory() as tmp:

        def check(block, minimal_form):
            """Build a block and check it; return None if it is not checked, else its errors."""
            cdl = prepare(block, groups)
            if cdl is None:
                return None
            source = os.path.join(tmp, "example.cdl")
            target = os.path.join(tmp, "example.nc")
            with open(source, "w", encoding="utf-8") as f:
                f.write(cdl)
            build = subprocess.run(["ncgen", "-k", "nc4", "-o", target, source], capture_output=True, text=True)
            if build.returncode != 0:
                return ["ncgen: " + build.stderr.strip().replace(source, "block")]
            dump = subprocess.run(["ncdump", target], capture_output=True, text=True, check=True).stdout
            is_file = cdl.startswith("netcdf ") and not cdl.startswith("netcdf fragment ")
            expected["file_name"] = cdl.split()[1] if is_file else ""
            expected["dimensions"] = raw_dimensions(form)
            return check_header(parse_header(dump), is_file, names, units_module, expected, minimal_form)

        for page in pages:
            relative = os.path.relpath(page, ROOT)
            text = read(page)
            tiers_of_page = {**tiers, **table_tiers(text)}
            order = check_table_order(relative, text)
            if order:
                failures += 1
                print(f"FAIL {relative}:")
                for error in order:
                    print(f"     {error}")
            for number, block in enumerate(FENCE.findall(text), 1):
                first = block.lstrip().splitlines()[0] if block.strip() else ""
                product = PRODUCT_TYPE.search(block)
                if product and product.group(1) in products:
                    category, row, _ = products[product.group(1)]
                    tiers_of_block = {**tiers, **category_tiers[category], **row}
                else:
                    tiers_of_block = tiers_of_page
                if first.startswith("// minimal form"):
                    # A written-out minimal form must equal the one derived from its example.
                    body = block.split("\n", 1)[1]
                    name = body.split()[1] if body.startswith("netcdf ") else ""
                    errors = []
                    if name not in examples:
                        errors.append(f'no example "netcdf {name}" to derive the minimal form from')
                    elif normalized(body) != normalized(minimal(examples[name])):
                        errors.append(f'differs from the minimal form of the example "netcdf {name}"')
                    forms = [("", body, True, errors)]
                else:
                    forms = [("", block, False, check_tiers(block, tiers_of_block, variable_attribute_tiers))]
                    if block.startswith("netcdf "):
                        forms.append((" (minimal form)", minimal(block), True, []))
                for suffix, form, minimal_form, errors in forms:
                    label = f"{relative}, block {number}{suffix}"
                    try:
                        found = check(form, minimal_form)
                    except ValueError as error:
                        found = [str(error)]
                    if found is None:
                        break
                    checked += not suffix
                    minimal_forms += minimal_form
                    errors += found
                    if errors:
                        failures += 1
                        print(f"FAIL {label}:")
                        for error in errors:
                            print(f"     {error}")
                    else:
                        print(f"OK   {label}")

    print(f"{checked} examples and {minimal_forms} minimal forms checked, {failures} failed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
