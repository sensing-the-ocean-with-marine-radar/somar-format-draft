---
title: Mandatory global attributes
layout: default
parent: Metadata
nav_order: 1
---

# Mandatory global attributes

Every SOMaR NetCDF file must carry the following three global attributes, regardless of processing level or product.
They name the conventions that the file follows, its data type, and whether its platform moves, and so tell a reader how the rest of the file is structured.
Further global attributes, which describe the file for discovery and citation, are [highly recommended or recommended](optional_global.md), among them [`product_type`](optional_global.md#product_type), which names the product of a Level 2 file.
The convention an attribute is taken from is named in small print under the attribute (see [Metadata](index.md)).

| Attribute | Values | Description |
|---|---|---|
| `Conventions`<br><small>[CF][cf-conventions]</small> | String; comma-separated list of the form `CF-<version>, ACDD-<version>, SOMaR-<major>.<minor>`, with the suffix `-draft` after a SOMaR draft version (e.g. `SOMaR-0.5-draft`) | The versions of the CF conventions, of ACDD, and of the SOMaR format that the file complies with (see [Versioning](../../index.md#versioning)). |
| `data_type`<br><small>SOMaR</small> | String; one of `polar_raw`, `polar_pulse_averaged`, `polar_image_cube`, `cartesian_image_cube`, `gridded_pixels`, `gridded_windows`, `discrete_windows`, `averaged_windows` | The SOMaR data type of the file's content, which defines its structure (see [SOMaR data types](../data_types/index.md)). |
| `platform_is_mobile`<br><small>[FM 301][fm301], Table 301-1</small> | String; `true` or `false` | Whether the platform moves: `"true"` for a moving platform, such as a ship, and `"false"` for a fixed one, such as a coastal station. FM 301 allows only `false`; SOMaR also allows `true`. It chooses between the layouts of a moving and a fixed platform (see [Moving and fixed platforms](../data_types/index.md#moving-and-fixed-platforms)): polar data types should then record the position and heading of the platform for every sweep or every ray (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)), and the Level 2 data types take the structure of a moving platform. |
{: .mandatory-attribute-table }

## Compliance

Compliance has two tiers: the structure of the file's data type is always checked, and the variables of its product are checked where the file names its product type.
A file complies with SOMaR if:

- it complies with the CF conventions of the version named in `Conventions`, which can be checked with an existing CF checker such as [`cfchecks`](https://github.com/cedadev/cf-checker) or the [IOOS compliance checker](https://github.com/ioos/compliance-checker), as far as they support the CF version and NetCDF groups: `cfchecks` 4.1.0, for example, checks against CF versions up to 1.8 and only the root group, which leaves out the groups that most SOMaR files use;
- it carries the mandatory global attributes, with values as specified above;
- it holds the dimensions, variables, and attributes that are marked as required for its `data_type` on the page of its data type, with the stated types, dimensions, and units (see [SOMaR data types](../data_types/index.md));
- if it carries [`product_type`](optional_global.md#product_type), its value is one of the registered product types, the file has the data type of that product in the product table, and it holds the variables that are marked as required in the row of the product there, as defined under [Product variables](../data_types/product_variables.md);
- any other attribute or variable it carries follows its definition, including restricted values such as those of [`processing_level`](optional_global.md#processing_level) or `product_type`.

The [highly recommended global attributes](optional_global.md#highly-recommended) are not part of compliance, but a file should carry them unless its producer cannot supply them: without them, data catalogs and users cannot tell what the file contains.
The same holds for `product_type` in a Level 2 file, and for the variables and attributes that are marked as recommended for its data type and product (see [Requirements](../data_types/index.md#requirements)).
A checker should report a missing highly recommended global attribute or recommended product item as a warning rather than an error.
The [recommended global attributes](optional_global.md#recommended) the [file naming](../file_naming/index.md), and the [storage recommendations](../storage/index.md) are not part of compliance either.

## Relation to FM 301 and ACDD

The WMO-CF Radial profile [FM 301][fm301], which SOMaR follows for [Level 1a data](../data_types/polar_raw.md), defines mandatory global attributes of its own (Tables 301-1 and 301-2). SOMaR does not require them: Level 1a files are not FM 301 files, so `Conventions` does not list the WMO-CF extensions and `wmo__cf_profile` is not set. Of those that SOMaR adopts, [`comment`](optional_global.md#comment), [`history`](optional_global.md#history), [`institution`](optional_global.md#institution), [`references`](optional_global.md#references), and [`source`](optional_global.md#source) are recommended, [`platform_is_mobile`](#platform_is_mobile) is mandatory, and the FM 301 `instrument_name` is replaced by the ACDD [`instrument`](optional_global.md#instrument) (see [Recommended](optional_global.md#recommended)).

SOMaR adopts ACDD attribute names wherever it defines an attribute that ACDD also defines, and the ACDD terms "highly recommended" and "recommended". ACDD requires no attribute; of those that it highly recommends, [`title`](optional_global.md#title), [`summary`](optional_global.md#summary), [`keywords`](optional_global.md#keywords), and `Conventions`, SOMaR highly recommends the first three and makes `Conventions` mandatory. The other ACDD attributes that SOMaR adopts, among them `institution`, the time coverage, and the spatial bounds, which ACDD recommends, and [`platform`](optional_global.md#platform), `instrument`, and [`keywords_vocabulary`](optional_global.md#keywords_vocabulary), which ACDD suggests, are recommended.

[cf-conventions]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#identification-of-conventions
[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
