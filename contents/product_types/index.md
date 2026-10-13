---
title: SOMaR product types
layout: default
nav_order: 4
---

# SOMaR product types

SOMaR products are organized by processing level, from radar data as recorded by the instrument to derived geophysical variables.
Every SOMaR NetCDF file carries a mandatory global attribute, `product_type`, which uniquely identifies the product's structure and schema.
In addition to the canonical `product_type` name, a recognized short abbreviation is defined for each product type for compact referencing, software variables, and directory naming.

| Level | Product | Canonical `product_type` | Short abbreviation |
|:---:|---|---|---|
| **L1a** | [Radar "raw" data](level1/level1a.md) | `radar_polar_raw` | `pol_raw` |
| **L1b** | [Polar image sequences](level1/level1b_polar.md) | `radar_polar_regularized` | `pol3d` |
| **L1b** | [Cartesian image sequences](level1/level1b_cartesian.md) | `radar_cartesian` | `cart3d` |
| **L2a** | [Roughness images](level2/roughness_images.md) | `sea_surface_roughness` | `rough` |
| **L2a** | [Roughness image mosaics](level2/roughness_mosaics.md) | `sea_surface_roughness_mosaic` | `rough_mosaic` |
| **L2a** | [Near-surface current maps](level2/current_maps.md) | `currents` | `cur` |
| **L2a** | [Near-surface current profile maps](level2/current_maps.md#near-surface-current-profile-maps) | `currents_profile` | `cur_profile` |
| **L2a** | [Bathymetric maps](level2/depth_maps.md) | `bathymetry` | `bathy` |
| **L2a** | [Sea ice drift maps](level2/sea_ice_drift.md) | `sea_ice_drift` | `ice_drift` |
| **L2a** | [Surface wave 2D wavenumber spectra](level2/wave_wavenumber_spectra.md) | `wavenumber_spectra` | `wav_k2d` |
| **L2b** | [Surface wave 2D frequency spectra](level2/wave_frequency_direction_spectra.md) | `frequency_direction_spectra` | `wav_fdir` |
| **L2b** | [Surface wave 1D frequency spectra](level2/wave_frequency_spectra.md) | `wave_spectrograms` | `wav_f1d` |
| **L2b** | [Peak and mean wave parameters](level2/wave_parameters.md) | `wave_parameters` | `wav_params` |
{: .product-table }

[Level 1](level1/index.md) products retain the radar's own measurement (backscatter intensity or amplitude in uncalibrated units), either pulse by pulse in the sensor's polar geometry ([Level 1a](level1/level1a.md)) or as individual images with a regular azimuth axis ([Level 1b polar](level1/level1b_polar.md)) or on a local Cartesian grid ([Level 1b Cartesian](level1/level1b_cartesian.md)).
[Level 2](level2/index.md) products are geophysical variables, either retrieved directly from image sequences (Level 2a) or derived from those retrievals (Level 2b).
Each page below documents the product-specific dimensions, variables, and attributes, with a minimal example, in addition to the [shared metadata](../metadata_attributes/index.md).

## Terms

- A **sweep** is the sequence of pulses of one antenna revolution, or of one pass over the sector for a radar that scans a sector. It is the unit in which Level 1a data are stored.
- A **revolution** yields one **image** at Level 1b.
- An **analysis window** is the area, within the radar footprint, from which one Level 2 measurement is retrieved.
- A **measurement period** is the time span over which the images contributing to one Level 2 map or measurement are collected.
