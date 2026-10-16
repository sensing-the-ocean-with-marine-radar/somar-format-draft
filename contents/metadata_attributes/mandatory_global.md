---
title: Mandatory global attributes
layout: default
parent: Metadata
nav_order: 1
---

# Mandatory global attributes

Every SOMaR NetCDF file must carry the following global attributes, regardless of processing level or product.
The convention an attribute is taken from is named in small print under the attribute (see [Metadata](index.md)).

| Attribute | Values | Description |
|---|---|---|
| `Conventions`<br><small>[CF][cf-conventions]</small> | String; comma-separated list of the form `CF-<version>, ACDD-<version>, SOMaR-<major>.<minor>`, with the suffix `-draft` after a SOMaR draft version (e.g. `SOMaR-0.5-draft`) | The versions of the CF conventions, of ACDD, and of the SOMaR format that the file complies with (see [Versioning](../../index.md#versioning)). |
| `institution`<br><small>[CF][cf-description]</small> | String; free text | The institution responsible for producing the file. |
| `product_type`<br><small>SOMaR</small> | String; one of `radar_polar_raw`, `radar_polar_regularized`, `radar_cartesian`, `sea_surface_roughness`, `sea_surface_roughness_mosaic`, `currents`, `currents_profile`, `bathymetry`, `sea_ice_drift`, `wave_wavenumber_spectra`, `wave_frequency_direction_spectra`, `wave_frequency_spectra`, `wave_parameters` | The specific SOMaR product type of the file's content (see [SOMaR product types](../product_types/index.md)). |
| `time_coverage_end`<br><small>[ACDD][acdd]</small> | String; ISO 8601 date and time in UTC, fractional seconds permitted | The time of the latest observation contributing to the data in the file. For products organized in time-bounded groups of fixed window length, this is the end of the last window. |
| `time_coverage_start`<br><small>[ACDD][acdd]</small> | String; ISO 8601 date and time in UTC, fractional seconds permitted | The time of the first observation contributing to the data in the file. |
| `title`<br><small>[CF][cf-description]</small> | String; free text | A short, human-readable description of the file's content. |
{: .mandatory-attribute-table }

The WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes), which SOMaR follows for [Level 1a data](../product_types/level1/level1a.md), defines mandatory global attributes of its own (Tables 301-1 and 301-2). SOMaR does not require them: Level 1a files are not FM 301 files, so `Conventions` does not list the WMO-CF extensions and `wmo__cf_profile` is not set. Of those that SOMaR adopts, `institution` is mandatory and `source`, `history`, and `platform_is_mobile` are optional, and the FM 301 `instrument_name` is replaced by the ACDD `instrument` (see [Optional global attributes](optional_global.md)).

SOMaR adopts ACDD attribute names wherever it defines an attribute that ACDD also defines. Of the attributes that ACDD recommends, SOMaR requires only `title`, `time_coverage_start`, and `time_coverage_end`; others are listed among the [optional global attributes](optional_global.md).

## Compliance

A file complies with SOMaR if:

- it complies with the CF conventions of the version named in `Conventions`, which can be checked with an existing CF checker such as [`cfchecks`](https://github.com/cedadev/cf-checker) or the [IOOS compliance checker](https://github.com/ioos/compliance-checker), although their support for NetCDF groups varies;
- it carries all mandatory global attributes, with values as specified above;
- it holds the dimensions, variables, and attributes that the page of its `product_type` marks as required (see [SOMaR product types](../product_types/index.md)), with the stated types, dimensions, and units;
- any optional attribute or variable it carries follows its definition, including restricted values such as those of `processing_level` or `platform_is_mobile`.

The [file naming](../file_naming/index.md) is a recommendation and not part of compliance.

[cf-conventions]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#identification-of-conventions
[cf-description]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents
[acdd]: https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
