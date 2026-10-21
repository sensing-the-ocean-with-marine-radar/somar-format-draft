---
title: SOMaR product types
layout: default
nav_order: 5
has_children: true
---

# SOMaR product types

SOMaR products are organized in three categories by their geometry, i.e. by how their values are located in space.
The processing level, from radar data as recorded by the instrument to derived geophysical quantities, is a property of each product.
Every SOMaR NetCDF file carries a mandatory global attribute, `product_type`, which uniquely identifies the product and thereby its category, structure, and schema.

| Level | Product | Category | `product_type` |
|:---:|---|---|---|
| **L1a** | [Radar "raw" data](../annex/level1a.md) | [Polar](polar.md#product-types) | `radar_polar_raw` |
| **L1b** | [Polar image sequences](../annex/level1b_polar.md) | [Polar](polar.md#product-types) | `radar_polar_regularized` |
| **L1b** | [Cartesian image sequences](../annex/level1b_cartesian.md) | [Gridded](gridded.md#product-types) | `radar_cartesian` |
| **L2a** | [Relative roughness images](../annex/relative_roughness_images.md) | [Gridded](gridded.md#product-types) | `relative_roughness` |
| **L2a** | [Relative roughness image mosaics](../annex/relative_roughness_mosaics.md) | [Gridded](gridded.md#product-types) | `relative_roughness_mosaic` |
| **L2a** | [Near-surface current maps](../annex/current_maps.md) | [Gridded](gridded.md#product-types) | `currents` |
| **L2a** | [Near-surface current profile maps](../annex/current_profile_maps.md) | [Gridded](gridded.md#product-types) | `currents_profile` |
| **L2a** | [Bathymetric maps](../annex/depth_maps.md) | [Gridded](gridded.md#product-types) | `bathymetry` |
| **L2a** | [Sea ice drift maps](../annex/sea_ice_drift.md) | [Gridded](gridded.md#product-types) | `sea_ice_drift` |
| **L2a** | [Surface wave two-dimensional wavenumber spectra](../annex/wave_wavenumber_spectra.md) | [Spatially averaged](spatially_averaged.md#product-types) | `wave_wavenumber_spectra` |
| **L2b** | [Surface wave frequency-direction spectra](../annex/wave_frequency_direction_spectra.md) | [Spatially averaged](spatially_averaged.md#product-types) | `wave_frequency_direction_spectra` |
| **L2b** | [Surface wave one-dimensional frequency spectra](../annex/wave_frequency_spectra.md) | [Spatially averaged](spatially_averaged.md#product-types) | `wave_frequency_spectra` |
| **L2b** | [Peak and mean wave parameters](../annex/wave_parameters.md) | [Spatially averaged](spatially_averaged.md#product-types) | `wave_parameters` |
{: .product-table }

## Processing levels

Level 1 products retain the radar's own measurement (backscatter amplitude or power in uncalibrated units), either ray by ray in the sensor's polar geometry ([Level 1a](polar.md)) or as individual images, one per antenna revolution, with a regular azimuth axis ([Level 1b polar](polar.md#image-cube)) or on a local Cartesian grid ([Level 1b Cartesian](gridded.md#image-cube-with-moving-origin)), and serve as the input of the Level 2 retrievals.
Level 2 products are geophysical quantities derived from sequences of Level 1b images, such as relative sea surface roughness, near-surface currents, bathymetry, sea ice drift, and surface waves.
Level 2a products are the direct result of a retrieval applied to Level 1b image sequences: relative roughness images and mosaics, maps of near-surface currents, current profiles, bathymetry, and sea ice drift, and two-dimensional wavenumber spectra.
Level 2b products are computed from Level 2a products and therefore inherit their sampling, calibration, and quality control; currently all of them are surface wave products derived from the two-dimensional wavenumber spectra.
How the Level 2 products were obtained is recorded in their [processing parameters](../metadata_attributes/processing_parameters.md), and how good they are in their [quality flags](../metadata_attributes/quality_flags.md).

## Categories

Each product belongs to one of three categories, according to how its values are located in space:

- [Polar products](polar.md) (radar data in sensor coordinates) locate each value by the range and azimuth of the sensor, with the radar antenna at the origin.
- [Gridded products](gridded.md) (maps, images) give one value set for each cell of a grid that resolves the area covered: each analysis window, or each pixel of an image, keeps its own position.
- [Spatially averaged products](spatially_averaged.md) (spectra, bulk parameters) combine several analysis windows into one value set per measurement, located at their mean position.

Each category page defines the structure that its products share and lists its products, in a product-type table, with the variables that each of them holds.
The variables themselves are defined under [Product variables](../metadata_attributes/product_variables.md).
An example file of each product, and for Level 2 a description of the product and its retrieval, is given in the informative [Annex: Example products](../annex/index.md).
All products carry the [shared metadata](../metadata_attributes/index.md) in addition.

### Moving and fixed platforms

The structure of a file depends on its category and on whether the platform moves, which a file from a moving platform states by setting [`platform_is_mobile`](../metadata_attributes/optional_global.md) to `"true"`:

| | Moving platform | Fixed platform |
|---|---|---|
| **Polar products** | the position and heading of the platform per sweep or per ray (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)) | scalar `latitude` and `longitude` of the radar antenna |
| **Gridded products** | one [time-bounded grid](gridded.md#time-bounded-grids) per measurement, each in its own `time_<YYYYMMDDHHMMSS>` group; for Level 1b Cartesian images, one [image cube](gridded.md#image-cube-with-moving-origin) whose origin `longitude(time)`, `latitude(time)` moves with the platform | a [single grid](gridded.md#fixed-platform) for the whole file, with the leading dimension `time` |
| **Spatially averaged products** | a [trajectory](spatially_averaged.md#moving-and-fixed-platforms): `longitude(time)` and `latitude(time)` | a [time series](spatially_averaged.md#moving-and-fixed-platforms): scalar `longitude` and `latitude` |

## Requirements

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

