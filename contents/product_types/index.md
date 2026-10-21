---
title: SOMaR product types
layout: default
nav_order: 5
has_children: true
---

# SOMaR product types

SOMaR products are organized by processing level, from radar data as recorded by the instrument to derived geophysical variables.
Every SOMaR NetCDF file carries a mandatory global attribute, `product_type`, which uniquely identifies the product's structure and schema.

| Level | Product | Category | `product_type` |
|:---:|---|---|---|
| **L1a** | [Radar "raw" data](level1/level1a.md) | — | `radar_polar_raw` |
| **L1b** | [Polar image sequences](level1/level1b_polar.md) | — | `radar_polar_regularized` |
| **L1b** | [Cartesian image sequences](level1/level1b_cartesian.md) | — | `radar_cartesian` |
| **L2a** | [Relative roughness images](../annex/relative_roughness_images.md) | [Gridded](level2/gridded.md#product-types) | `relative_roughness` |
| **L2a** | [Relative roughness image mosaics](../annex/relative_roughness_mosaics.md) | [Gridded](level2/gridded.md#product-types) | `relative_roughness_mosaic` |
| **L2a** | [Near-surface current maps](../annex/current_maps.md) | [Gridded](level2/gridded.md#product-types) | `currents` |
| **L2a** | [Near-surface current profile maps](../annex/current_profile_maps.md) | [Gridded](level2/gridded.md#product-types) | `currents_profile` |
| **L2a** | [Bathymetric maps](../annex/depth_maps.md) | [Gridded](level2/gridded.md#product-types) | `bathymetry` |
| **L2a** | [Sea ice drift maps](../annex/sea_ice_drift.md) | [Gridded](level2/gridded.md#product-types) | `sea_ice_drift` |
| **L2a** | [Surface wave two-dimensional wavenumber spectra](../annex/wave_wavenumber_spectra.md) | [Spatially averaged](level2/spatially_averaged.md#product-types) | `wave_wavenumber_spectra` |
| **L2b** | [Surface wave frequency-direction spectra](../annex/wave_frequency_direction_spectra.md) | [Spatially averaged](level2/spatially_averaged.md#product-types) | `wave_frequency_direction_spectra` |
| **L2b** | [Surface wave one-dimensional frequency spectra](../annex/wave_frequency_spectra.md) | [Spatially averaged](level2/spatially_averaged.md#product-types) | `wave_frequency_spectra` |
| **L2b** | [Peak and mean wave parameters](../annex/wave_parameters.md) | [Spatially averaged](level2/spatially_averaged.md#product-types) | `wave_parameters` |
{: .product-table }

[Level 1](level1/index.md) products retain the radar's own measurement (backscatter amplitude or power in uncalibrated units), either ray by ray in the sensor's polar geometry ([Level 1a](level1/level1a.md)) or as individual images with a regular azimuth axis ([Level 1b polar](level1/level1b_polar.md)) or on a local Cartesian grid ([Level 1b Cartesian](level1/level1b_cartesian.md)).
Each of them has a structure of its own and forms a category of its own: its page documents its dimensions, variables, and attributes.
[Level 2](level2/index.md) products are geophysical variables, either retrieved directly from image sequences (Level 2a) or derived from those retrievals (Level 2b).
They fall into two categories, [gridded products](level2/gridded.md) and [spatially averaged products](level2/spatially_averaged.md), whose pages document the structure that the products of a category share and, in a product-type table, the data variables of each product; the variables themselves are defined under [Product variables](../metadata_attributes/product_variables.md).
An example file of each product, and for Level 2 a description of the product and its retrieval, is given in the informative [Annex: Example products](../annex/index.md).
All products carry the [shared metadata](../metadata_attributes/index.md) in addition.
The tables state for each variable and attribute whether it is required, recommended, or optional:

- **Required** items are those without which a reader would misread the values or misplace them in time or space: the coordinates, the data variables that define the product, and the parameters that change what a value means.
- **Recommended** items document how the data were obtained and how good they are, such as the processing parameters, the quality flag, and retrieval diagnostics. A file should carry them where its producer can supply them.
- **Optional** items are further diagnostics and details that a producer may add.

Only the required items are part of [compliance](../metadata_attributes/mandatory_global.md#compliance).
Sectors of the field of view that are shadowed or blanked are recorded in the `radar_parameters` group (see [Obstructed sectors](../metadata_attributes/radar_parameters.md#obstructed-sectors)).

## Adding a product type

The product types are a closed list: a file whose content fits none of them is not a SOMaR file.
A new product type is proposed as an [issue](https://github.com/sensing-the-ocean-with-marine-radar/somar-format-draft/issues) or pull request that gives its row in the product-type table of its category, the definitions of any new variables under [Product variables](../metadata_attributes/product_variables.md), and an example file for the annex.
Adding a product type invalidates no existing file, so that it can be released in a minor version (see [Versioning](../../index.md#versioning)).

{: .open_issue }
> Radar product types that are not yet defined:
> * Wave spectrum partitioning results (wave parameters for wind sea and swell systems),
> * Wind speed and direction retrieved from radar backscatter,
> * Products for coastal applications, such as the mapping of intertidal areas.

