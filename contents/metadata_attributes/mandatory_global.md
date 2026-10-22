---
title: Mandatory global attributes
layout: default
parent: Metadata
nav_order: 1
---

# Mandatory global attributes

Every SOMaR NetCDF file must carry the following two global attributes, regardless of processing level or product.
They name the conventions and the product that the file follows, and so tell a reader how to interpret the rest of the file.
Further global attributes, which describe the file for discovery and citation, are [highly recommended or recommended](optional_global.md).
The convention an attribute is taken from is named in small print under the attribute (see [Metadata](index.md)).

| Attribute | Values | Description |
|---|---|---|
| `Conventions`<br><small>[CF][cf-conventions]</small> | String; comma-separated list of the form `CF-<version>, ACDD-<version>, SOMaR-<major>.<minor>`, with the suffix `-draft` after a SOMaR draft version (e.g. `SOMaR-0.5-draft`) | The versions of the CF conventions, of ACDD, and of the SOMaR format that the file complies with (see [Versioning](../../index.md#versioning)). |
| `product_type`<br><small>SOMaR</small> | String; one of `radar_polar_raw`, `radar_polar_regularized`, `radar_polar_averaged`, `radar_cartesian`, `relative_roughness`, `relative_roughness_mosaic`, `currents`, `currents_profile`, `bathymetry`, `sea_ice_drift`, `wave_wavenumber_spectra`, `wave_frequency_direction_spectra`, `wave_frequency_spectra`, `wave_parameters` | The specific SOMaR product type of the file's content (see [SOMaR product types](../product_types/index.md)). |
{: .mandatory-attribute-table }

The WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes), which SOMaR follows for [Level 1a data](../product_types/polar.md), defines mandatory global attributes of its own (Tables 301-1 and 301-2). SOMaR does not require them: Level 1a files are not FM 301 files, so `Conventions` does not list the WMO-CF extensions and `wmo__cf_profile` is not set. Of those that SOMaR adopts, `institution`, `source`, `history`, and `platform_is_mobile` are recommended, and the FM 301 `instrument_name` is replaced by the ACDD `instrument` (see [Recommended global attributes](optional_global.md)).

SOMaR adopts ACDD attribute names wherever it defines an attribute that ACDD also defines, and the ACDD terms "highly recommended" and "recommended". ACDD requires no attribute; of those that it highly recommends, `title`, `summary`, `keywords`, and `Conventions`, SOMaR highly recommends the first three and makes `Conventions` mandatory. The other ACDD attributes that SOMaR adopts, among them `institution`, the time coverage, and the spatial bounds, which ACDD recommends, and `platform`, `instrument`, and `keywords_vocabulary`, which ACDD suggests, are recommended (see [Recommended global attributes](optional_global.md)).

## Compliance

A file complies with SOMaR if:

- it complies with the CF conventions of the version named in `Conventions`, which can be checked with an existing CF checker such as [`cfchecks`](https://github.com/cedadev/cf-checker) or the [IOOS compliance checker](https://github.com/ioos/compliance-checker), as far as they support the CF version and NetCDF groups: `cfchecks` 4.1.0, for example, checks against CF versions up to 1.8 and only the root group, which leaves out the groups that most SOMaR products use;
- it carries the mandatory global attributes, with values as specified above, and, if it is from a moving platform, `platform_is_mobile = "true"`;
- it holds the dimensions, variables, and attributes that are marked as required for its `product_type` on the page of its category and in its row of the product-type table there, with the stated types, dimensions, and units and with the variables as defined under [Product variables](../product_types/product_variables.md) (see [SOMaR product types](../product_types/index.md));
- any other attribute or variable it carries follows its definition, including restricted values such as those of `processing_level` or `platform_is_mobile`.

The [highly recommended global attributes](optional_global.md#highly-recommended) are not part of compliance, but a file should carry them unless its producer cannot supply them: without them, data catalogs and users cannot tell what the file contains.
The same holds for the variables and attributes that are marked as recommended for its `product_type` (see [SOMaR product types](../product_types/index.md)).
A checker should report a missing highly recommended global attribute or recommended product item as a warning rather than an error.
The [recommended global attributes](optional_global.md#recommended) and the [file naming](../file_naming/index.md) are not part of compliance either.

[cf-conventions]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#identification-of-conventions
