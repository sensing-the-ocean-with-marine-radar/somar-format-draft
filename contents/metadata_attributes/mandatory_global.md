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
| `Conventions`<br><small>[CF][cf-conventions]</small> | String; comma-separated list of the form `CF-<version>, ACDD-<version>, SOMaR-<version>` | The versions of the CF conventions, of ACDD, and of the SOMaR format that the file complies with. |
| `product_type`<br><small>SOMaR</small> | String; one of `radar_polar_raw`, `radar_polar_regularized`, `radar_cartesian`, `sea_surface_roughness`, `sea_surface_roughness_mosaic`, `currents`, `currents_profile`, `bathymetry`, `sea_ice_drift`, `wave_wavenumber_spectra`, `wave_frequency_direction_spectra`, `wave_frequency_spectra`, `wave_parameters` | The specific SOMaR product type of the file's content (see [SOMaR product types](../product_types/index.md)). |
{: .mandatory-attribute-table }

The WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes), which SOMaR follows for [Level 1a data](../product_types/level1/level1a.md), defines mandatory global attributes of its own (Tables 301-1 and 301-2). SOMaR does not require them: Level 1a files are not FM 301 files, so `Conventions` does not list the WMO-CF extensions and `wmo__cf_profile` is not set. Those that SOMaR adopts (`institution`, `source`, `history`, and `platform_is_mobile`) are optional, and the FM 301 `instrument_name` is replaced by the ACDD `instrument` (see [Optional global attributes](optional_global.md)).

SOMaR adopts ACDD attribute names wherever it defines an attribute that ACDD also defines, but it does not require the attributes recommended by ACDD.

{: .open_issue }
It is under discussion whether to make more attributes mandatory (e.g. `title`, `institution`, `time_coverage_start`, `time_coverage_end`, `processing_level`). Also under discussion: recommending further ACDD attributes (`id`, `naming_authority`, `keywords`, `standard_name_vocabulary`, `project`), and a `station_id` attribute matching the [file name](../file_naming/index.md). How compliance is checked (e.g. with the CF checker) and how the `SOMaR-<version>` string is versioned are not yet specified.

[cf-conventions]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#identification-of-conventions
