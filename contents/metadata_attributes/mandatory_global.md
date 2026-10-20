---
title: Mandatory global attributes
layout: default
parent: Metadata
nav_order: 1
---

# Mandatory global attributes

Every SOMaR NetCDF file must carry the following two global attributes, regardless of processing level or product.
They name the conventions and the product that the file follows, and so tell a reader how to interpret the rest of the file.
Further global attributes, which describe the file for discovery and citation, are [highly recommended or recommended where applicable](optional_global.md).
The convention an attribute is taken from is named in small print under the attribute (see [Metadata](index.md)).

| Attribute | Values | Description |
|---|---|---|
| `Conventions`<br><small>[CF][cf-conventions]</small> | String; comma-separated list of the form `CF-<version>, ACDD-<version>, SOMaR-<major>.<minor>`, with the suffix `-draft` after a SOMaR draft version (e.g. `SOMaR-0.5-draft`) | The versions of the CF conventions, of ACDD, and of the SOMaR format that the file complies with (see [Versioning](../../index.md#versioning)). |
| `product_type`<br><small>SOMaR</small> | String; one of `radar_polar_raw`, `radar_polar_regularized`, `radar_cartesian`, `sea_surface_roughness`, `sea_surface_roughness_mosaic`, `currents`, `currents_profile`, `bathymetry`, `sea_ice_drift`, `wave_wavenumber_spectra`, `wave_frequency_direction_spectra`, `wave_frequency_spectra`, `wave_parameters` | The specific SOMaR product type of the file's content (see [SOMaR product types](../product_types/index.md)). |
{: .mandatory-attribute-table }

The WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes), which SOMaR follows for [Level 1a data](../product_types/level1/level1a.md), defines mandatory global attributes of its own (Tables 301-1 and 301-2). SOMaR does not require them: Level 1a files are not FM 301 files, so `Conventions` does not list the WMO-CF extensions and `wmo__cf_profile` is not set. Of those that SOMaR adopts, `institution`, `source`, `history`, and `platform_is_mobile` are recommended where applicable, and the FM 301 `instrument_name` is replaced by the ACDD `instrument` (see [Recommended global attributes](optional_global.md)).

SOMaR adopts ACDD attribute names wherever it defines an attribute that ACDD also defines, and the ACDD tier of highly recommended attributes. ACDD requires no attribute; of those that it highly recommends, `title`, `summary`, `keywords`, and `Conventions`, SOMaR highly recommends the first three and makes `Conventions` mandatory. The other ACDD attributes that SOMaR adopts, among them `institution`, the time coverage, and the spatial bounds, which ACDD recommends, and `platform`, `instrument`, and `keywords_vocabulary`, which ACDD suggests, are recommended where applicable (see [Recommended global attributes](optional_global.md)).

## Compliance

A file complies with SOMaR if:

- it complies with the CF conventions of the version named in `Conventions`, which can be checked with an existing CF checker such as [`cfchecks`](https://github.com/cedadev/cf-checker) or the [IOOS compliance checker](https://github.com/ioos/compliance-checker), although their support for NetCDF groups varies;
- it carries the mandatory global attributes, with values as specified above;
- it holds the dimensions, variables, and attributes that the page of its `product_type` marks as required (see [SOMaR product types](../product_types/index.md)), with the stated types, dimensions, and units;
- any other attribute or variable it carries follows its definition, including restricted values such as those of `processing_level` or `platform_is_mobile`.

The [highly recommended global attributes](optional_global.md#highly-recommended) are not part of compliance, but a file should carry them unless its producer cannot supply them: without them, data catalogs and users cannot tell what the file contains.
A checker should report a missing highly recommended attribute as a warning rather than an error.
The [file naming](../file_naming/index.md) is a recommendation and not part of compliance either.

[cf-conventions]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#identification-of-conventions
