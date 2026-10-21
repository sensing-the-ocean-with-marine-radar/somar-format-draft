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
coordinate reference system, and the SOMaR rules for global attributes and
file names, among them that a file whose structure is that of a moving
platform sets platform_is_mobile to "true" and that a Level 2 file that sets
it has that structure; the examples must carry the highly recommended global
attributes as well as the mandatory ones, and the variables that the product
variables they carry require (see product_variables.md). The spatial bounds
are checked against the positions the example gives: scalar latitude and
longitude values in the data sections and the projection origins of crs
variables.

Items that a file may omit are marked by a trailing comment with their tier
("// highly recommended", "// recommended", or "// optional"). The markers
of global attributes and variables are checked against the tables of the
global attribute pages, the processing parameters, and the page of the
example; for a product type, against the tables of its page instead, as
linked from the product types index for Level 1, and for Level 2 those of
its category page and its row in the product-type table there. Each file example is also checked in its minimal form, without the
marked items; a block whose first line is "// minimal form" must equal the
minimal form of the example with the same "netcdf" name.

Usage: python3 scripts/check_examples.py [--strict]

Without cf-units installed, the unit checks are skipped with a warning;
--strict makes that an error.
"""

import argparse
import glob
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
# Level 1 product types and the names of their backscatter variables, of which a file holds exactly one.
LEVEL1_PRODUCT_TYPES = {"radar_polar_raw", "radar_polar_regularized", "radar_cartesian"}
LEVEL1_DATA_VARIABLES = {"backscatter_amplitude", "backscatter_power"}
GEOSPATIAL_ATTRIBUTES = ("geospatial_lat_min", "geospatial_lat_max", "geospatial_lon_min", "geospatial_lon_max")
FILE_NAME = re.compile(
    r"^(?P<station>[a-z0-9]+)_\d{4}-\d{2}-\d{2}-\d{2}(-\d{2})?_"
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
CATEGORY_PAGES = ("contents/product_types/level2/gridded.md", "contents/product_types/level2/spatially_averaged.md")
PRODUCT_TYPE = re.compile(r':product_type = "(\w+)"')
# The rules of the product variables: "Carried together with `x`." and "Requires `x`." (see product_variables.md).
VARIABLE_RULE = re.compile(r"(?:Carried together with|Requires) ((?:`\w+`(?:,? and |, )?)+)\.")
# The names of a coordinate reference system, which CF requires all together if any is given (Appendix F).
CRS_NAMES = ("reference_ellipsoid_name", "prime_meridian_name", "horizontal_datum_name", "geographic_crs_name")
# Attributes whose references to omitted variables are dropped in the minimal form.
REFERENCE_ATTRIBUTES = ("grid_mapping", "ancillary_variables")


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


def level1_pages():
    """Return {product_type: page} for the Level 1 products, from the table of the product types index."""
    text = read(os.path.join(ROOT, "contents/product_types/index.md"))
    return {product: "contents/product_types/" + page for page, product in re.findall(r"\]\((level1/\w+\.md)\) \| [^|]* \| `(\w+)`", text)}


def registry():
    """Return {product_type: (category page, {name: tier})} from the product-type tables of the categories.

    The tiers are those of the "**Required:**", "**Recommended:**", and "**Optional:**" lines of a row.
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
            products[re.search(r"`(\w+)`", cells[1]).group(1)] = (page, tiers)
    return products


def global_tiers():
    """Return {name: tier} for the shared global attributes and the processing parameters."""
    tiers = {name: "required" for name in mandatory_attributes()}
    tiers.update((name, "highly recommended") for name in highly_recommended_attributes())
    tiers.update((name, "recommended") for name in recommended_global_section("Recommended"))
    tiers.update(table_tiers(read(os.path.join(ROOT, "contents/metadata_attributes/processing_parameters.md")), strict=False))
    return tiers


def variable_rules():
    """Return {variable: [variables it requires]} from the descriptions in product_variables.md."""
    rules = {}
    for line in read(os.path.join(ROOT, "contents/metadata_attributes/product_variables.md")).splitlines():
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


def check_tiers(block, tiers):
    """Check the tier markers of global attributes and variables against the tables."""
    errors = []
    for line in block.splitlines():
        match = ATTRIBUTE.match(line)
        if match and match.group(2) == "":
            kind, name = "global attribute", match.group(3)
        elif DECLARATION.match(line):
            kind, name = "variable", DECLARATION.match(line).group(1)
        else:
            continue
        expected = tiers.get(name)
        marked = tier(line) or "required"
        if expected is None or marked == expected or (marked == "required" and expected == "recommended" and tier(line)):
            continue
        errors.append(f'{kind} {name} is marked as {marked}, but the tables make it {expected}')
    return errors


def parse_header(text):
    """Parse "ncdump" output into {group path: {"variables": {...}, "attributes": {...}, "data": {...}, "dimensions": {...}}}.

    "data" holds the values of variables whose data section gives a single number, and
    "dimensions" the dimension names of each variable.
    """
    groups = {"/": {"variables": {}, "attributes": {}, "data": {}, "dimensions": {}}}
    stack = ["/"]
    section = None
    for line in text.splitlines():
        stripped = line.strip()
        match = re.match(r"group: (\w+) \{$", stripped)
        if match:
            path = stack[-1].rstrip("/") + "/" + match.group(1)
            groups[path] = {"variables": {}, "attributes": {}, "data": {}, "dimensions": {}}
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
    """Find a variable by name in the group or one of its ancestors (CF 1.8 scoping)."""
    while True:
        if name in groups[path]["variables"]:
            return True
        if path == "/":
            return False
        path = path.rsplit("/", 1)[0] or "/"


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
            for attribute in ("grid_mapping", "coordinates", "ancillary_variables"):
                for target in unquote(attributes.get(attribute, "")).split():
                    if not resolve(groups, path, target):
                        errors.append(f'{where}: {attribute} names "{target}", which does not exist in scope')
            if is_file:
                for required in expected["variable_rules"].get(variable, []):
                    if not resolve(groups, path, required):
                        errors.append(f"{where}: requires {required}, which does not exist in scope (see product_variables.md)")
            names = [name for name in CRS_NAMES if name in attributes]
            if names and len(names) < len(CRS_NAMES):
                errors.append(f"{where}: has {', '.join(names)} but not {', '.join(n for n in CRS_NAMES if n not in names)}, which CF requires together")
            meanings = unquote(attributes.get("flag_meanings", "")).split()
            for attribute in ("flag_values", "flag_masks"):
                if attribute in attributes and len(attributes[attribute].split(",")) != len(meanings):
                    errors.append(f"{where}: {attribute} and flag_meanings differ in length")
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
        if product in LEVEL1_PRODUCT_TYPES:
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
    level1 = {product: table_tiers(read(os.path.join(ROOT, page))) for product, page in level1_pages().items()}
    if level1.keys() != LEVEL1_PRODUCT_TYPES:
        sys.exit(f"the product types index links {', '.join(sorted(level1))} as Level 1 products")
    expected["level2_product_types"] = set(products)
    unlisted = expected["product_types"] - LEVEL1_PRODUCT_TYPES - products.keys()
    if unlisted:
        sys.exit(f"product types missing from the product-type tables: {', '.join(sorted(unlisted))}")
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
            return check_header(parse_header(dump), is_file, names, units_module, expected, minimal_form)

        for page in pages:
            relative = os.path.relpath(page, ROOT)
            text = read(page)
            tiers_of_page = {**tiers, **table_tiers(text)}
            for number, block in enumerate(FENCE.findall(text), 1):
                first = block.lstrip().splitlines()[0] if block.strip() else ""
                product = PRODUCT_TYPE.search(block)
                if product and product.group(1) in products:
                    category, row = products[product.group(1)]
                    tiers_of_block = {**tiers, **category_tiers[category], **row}
                elif product and product.group(1) in level1:
                    tiers_of_block = {**tiers, **level1[product.group(1)]}
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
                    forms = [("", block, False, check_tiers(block, tiers_of_block))]
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
