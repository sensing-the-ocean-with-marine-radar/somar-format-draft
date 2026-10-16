#!/usr/bin/env python3
"""Build and check the CDL examples of the SOMaR specification.

Every fenced code block in contents/**/*.md is checked unless its first line
is "// excerpt":

- Blocks starting with "netcdf" are built as they are; blocks starting with
  "variables:", "group:", or "// global attributes:" are wrapped in a
  "netcdf fragment { ... }" first.
- Placeholders of the form "group: <name> { ... }" are replaced by the
  canonical group of that name, taken from the examples on the Metadata pages.
- Dimension lengths are capped at 3 so that the built files stay small; the
  data sections of the examples must therefore hold scalars only.

Each block is built with "ncgen -k nc4" and its "ncdump" output checked
against the pinned CF standard name table, UDUNITS (through cf-units), CF
scoping rules for references between variables, and the SOMaR rules for
global attributes and file names. The spatial bounds are checked against
the positions the example gives: scalar latitude and longitude values in
the data sections and the projection origins of crs variables.

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
GEOSPATIAL_ATTRIBUTES = ("geospatial_lat_min", "geospatial_lat_max", "geospatial_lon_min", "geospatial_lon_max")
FILE_NAME = re.compile(
    r"^(?P<station>[a-z0-9]+)_\d{4}-\d{2}-\d{2}-\d{2}(-\d{2})?_"
    r"(?P<product>[a-z0-9_]+)$"
)
FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.M | re.S)
PLACEHOLDER = re.compile(r"^(\s*)group: (\w+) \{ \.\.\. \}.*$", re.M)


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
    elif first.startswith(("variables:", "group:", "// global attributes:")):
        cdl = "netcdf fragment {\n" + block + "}\n"
    else:
        return None

    def expand(match):
        indent, name = match.groups()
        if name not in groups:
            raise ValueError(f'no canonical example for placeholder "group: {name} {{ ... }}"')
        return "".join(indent + line + "\n" for line in groups[name].splitlines())

    return cap_dimensions(PLACEHOLDER.sub(expand, cdl))


def parse_header(text):
    """Parse "ncdump" output into {group path: {"variables": {...}, "attributes": {...}, "data": {...}}}.

    "data" holds the values of variables whose data section gives a single number.
    """
    groups = {"/": {"variables": {}, "attributes": {}, "data": {}}}
    stack = ["/"]
    section = None
    for line in text.splitlines():
        stripped = line.strip()
        match = re.match(r"group: (\w+) \{$", stripped)
        if match:
            path = stack[-1].rstrip("/") + "/" + match.group(1)
            groups[path] = {"variables": {}, "attributes": {}, "data": {}}
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
        match = re.match(r"^\w+ (\w+)(\(.*\))? ;$", stripped)
        if match:
            group["variables"].setdefault(match.group(1), {})
    return groups


def number(value):
    """Return the number in an ncdump attribute value such as "15.03" or "15.03f", or None."""
    match = re.fullmatch(r"(-?[0-9.]+(?:e[-+]?\d+)?)[a-zA-Z]*", value or "")
    return float(match.group(1)) if match else None


def positions(groups):
    """Yield the known positions that the spatial bounds must enclose (see mandatory_global.md).

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


def check_header(groups, is_file, names, units_module, expected):
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
            meanings = unquote(attributes.get("flag_meanings", "")).split()
            for attribute in ("flag_values", "flag_masks"):
                if attribute in attributes and len(attributes[attribute].split(",")) != len(meanings):
                    errors.append(f"{where}: {attribute} and flag_meanings differ in length")
    if is_file:
        root = groups["/"]["attributes"]
        missing = [a for a in expected["mandatory_attributes"] if a not in root]
        if missing:
            errors.append(f"missing mandatory global attributes: {', '.join(missing)}")
        errors += check_bounds(groups)
        conventions = unquote(root.get("Conventions", ""))
        if conventions != expected["conventions"]:
            errors.append(f'Conventions is "{conventions}", expected "{expected["conventions"]}"')
        product = unquote(root.get("product_type", ""))
        if product not in expected["product_types"]:
            errors.append(f'product_type "{product}" is not one of the product types in mandatory_global.md')
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
    }

    failures = checked = 0
    with tempfile.TemporaryDirectory() as tmp:
        for page in sorted(glob.glob(os.path.join(ROOT, "contents/**/*.md"), recursive=True)):
            relative = os.path.relpath(page, ROOT)
            for number, block in enumerate(FENCE.findall(read(page)), 1):
                try:
                    cdl = prepare(block, groups)
                except ValueError as error:
                    print(f"FAIL {relative}, block {number}: {error}")
                    failures += 1
                    continue
                if cdl is None:
                    continue
                checked += 1
                source = os.path.join(tmp, f"example{checked}.cdl")
                target = os.path.join(tmp, f"example{checked}.nc")
                with open(source, "w", encoding="utf-8") as f:
                    f.write(cdl)
                build = subprocess.run(["ncgen", "-k", "nc4", "-o", target, source], capture_output=True, text=True)
                if build.returncode != 0:
                    message = build.stderr.strip().replace(source, "block")
                    print(f"FAIL {relative}, block {number}: ncgen: {message}")
                    failures += 1
                    continue
                dump = subprocess.run(["ncdump", target], capture_output=True, text=True, check=True).stdout
                is_file = cdl.startswith("netcdf ") and not cdl.startswith("netcdf fragment ")
                expected["file_name"] = cdl.split()[1] if is_file else ""
                errors = check_header(parse_header(dump), is_file, names, units_module, expected)
                if errors:
                    failures += 1
                    print(f"FAIL {relative}, block {number}:")
                    for error in errors:
                        print(f"     {error}")
                else:
                    print(f"OK   {relative}, block {number}")

    print(f"{checked} examples checked, {failures} failed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
