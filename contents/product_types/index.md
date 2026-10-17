---
title: SOMaR product types
layout: default
nav_order: 5
has_children: true
---

# SOMaR product types

SOMaR products are organized by processing level, from radar data as recorded by the instrument to derived geophysical variables.
Every SOMaR NetCDF file carries a mandatory global attribute, `product_type`, which uniquely identifies the product's structure and schema.

| Level | Product | `product_type` |
|:---:|---|---|
| **L1a** | [Radar "raw" data](level1/level1a.md) | `radar_polar_raw` |
| **L1b** | [Polar image sequences](level1/level1b_polar.md) | `radar_polar_regularized` |
| **L1b** | [Cartesian image sequences](level1/level1b_cartesian.md) | `radar_cartesian` |
| **L2a** | [Roughness images](level2/roughness_images.md) | `sea_surface_roughness` |
| **L2a** | [Roughness image mosaics](level2/roughness_mosaics.md) | `sea_surface_roughness_mosaic` |
| **L2a** | [Near-surface current maps](level2/current_maps.md) | `currents` |
| **L2a** | [Near-surface current profile maps](level2/current_maps.md#near-surface-current-profile-maps) | `currents_profile` |
| **L2a** | [Bathymetric maps](level2/depth_maps.md) | `bathymetry` |
| **L2a** | [Sea ice drift maps](level2/sea_ice_drift.md) | `sea_ice_drift` |
| **L2a** | [Surface wave two-dimensional wavenumber spectra](level2/wave_wavenumber_spectra.md) | `wave_wavenumber_spectra` |
| **L2b** | [Surface wave frequency-direction spectra](level2/wave_frequency_direction_spectra.md) | `wave_frequency_direction_spectra` |
| **L2b** | [Surface wave one-dimensional frequency spectra](level2/wave_frequency_spectra.md) | `wave_frequency_spectra` |
| **L2b** | [Peak and mean wave parameters](level2/wave_parameters.md) | `wave_parameters` |
{: .product-table }

[Level 1](level1/index.md) products retain the radar's own measurement (backscatter intensity or amplitude in uncalibrated units), either pulse by pulse in the sensor's polar geometry ([Level 1a](level1/level1a.md)) or as individual images with a regular azimuth axis ([Level 1b polar](level1/level1b_polar.md)) or on a local Cartesian grid ([Level 1b Cartesian](level1/level1b_cartesian.md)).
[Level 2](level2/index.md) products are geophysical variables, either retrieved directly from image sequences (Level 2a) or derived from those retrievals (Level 2b).
Each page below documents the product-specific dimensions, variables, and attributes, with a minimal example, in addition to the [shared metadata](../metadata_attributes/index.md).
The tables state for each variable and attribute whether it is required or optional.
Sectors of the field of view that are shadowed or blanked are recorded in the `radar_parameters` group (see [Obstructed sectors](../metadata_attributes/radar_parameters.md#obstructed-sectors)).

{: .open_issue }
Wind speed and direction retrieved from radar backscatter are not yet defined, nor are products for coastal applications, such as the mapping of intertidal areas.
