---
title: SOMaR product types
layout: default
nav_order: 4
---

# SOMaR product types

SOMaR products are organized by processing level, from radar data as recorded by the instrument to derived geophysical variables.
Every SOMaR NetCDF file carries a mandatory global attribute, `product_type`, which uniquely identifies the product's structure and schema.
In addition to the canonical `product_type` name, a recognized short abbreviation is defined for each product type for compact referencing, software variables, and directory naming.

| Level | Product | Canonical `product_type` | Short abbreviation | Description |
|---|---|---|---|---|
| **L1a** | [Radar "raw" data](level1/level1a.md) | `radar_polar_raw` | `pol_raw` | Unmodified pulse sequences in sensor polar geometry |
| **L1b** | [Polar image sequences](level1/level1b_polar.md) | `radar_polar_regularized` | `pol3d` | Radar images resampled onto a regular azimuth axis |
| **L1b** | [Cartesian image sequences](level1/level1b_cartesian.md) | `radar_cartesian` | `cart3d` | Radar images mapped onto a local Cartesian grid |
| **L2a** | [Roughness images](level2/roughness_images.md) | `sea_surface_roughness` | `roughness` | Temporally averaged backscatter intensity on local grids |
| **L2a** | [Roughness image mosaics](level2/roughness_mosaics.md) | `sea_surface_roughness_mosaic` | `roughness_mosaic` | Spatial mosaics of roughness images |
| **L2a** | [Near-surface current maps](level2/current_maps.md) | `currents` | `currents` | Horizontal current vectors from Doppler dispersion analysis |
| **L2a** | [Near-surface current profile maps](level2/current_maps.md#near-surface-current-profile-maps) | `currents_profile` | `currents_profile` | Vertical profiles of near-surface currents across wavenumber bins |
| **L2a** | [Bathymetric maps](level2/depth_maps.md) | `bathymetry` | `bathymetry` | Water depth maps from wave dispersion analysis |
| **L2a** | [Sea ice drift maps](level2/sea_ice_drift.md) | `sea_ice_drift` | `sea_ice_drift` | Horizontal ice drift vectors from image cross-correlation |
| **L2a** | [Surface wave 2D wavenumber spectra](level2/wave_wavenumber_spectra.md) | `wavenumber_spectra` | `wave_k2d` | Directional wave energy density spectra |
| **L2b** | [Surface wave 2D frequency spectra](level2/wave_frequency_direction_spectra.md) | `frequency_direction_spectra` | `wave_fdir` | Directional frequency wave spectra derived from wavenumber spectra |
| **L2b** | [Surface wave 1D frequency spectra](level2/wave_frequency_spectra.md) | `wave_spectrograms` | `wave_f1d` | One-dimensional frequency wave energy spectra and directional parameters |
| **L2b** | [Peak and mean wave parameters](level2/wave_parameters.md) | `wave_parameters` | `wave_params` | Summary bulk wave parameters (Hs, Tp, Tm, direction) |
{: .attribute-table }

[Level 1](level1/index.md) products retain the radar's own measurement (backscatter intensity or amplitude in uncalibrated units), either pulse by pulse in the sensor's polar geometry ([Level 1a](level1/level1a.md)) or as individual images with a regular azimuth axis ([Level 1b polar](level1/level1b_polar.md)) or on a local Cartesian grid ([Level 1b Cartesian](level1/level1b_cartesian.md)).
[Level 2](level2/index.md) products are geophysical variables, either retrieved directly from image sequences (Level 2a) or derived from those retrievals (Level 2b).
Each page below documents the product-specific dimensions, variables, and attributes, with a minimal example, in addition to the [shared metadata](../metadata_attributes/index.md).

## Terms

- A **sweep** is the sequence of pulses of one antenna revolution, or of one pass over the sector for a radar that scans a sector. It is the unit in which Level 1a data are stored.
- A **revolution** yields one **image** at Level 1b.
- An **analysis window** is the area, within the radar footprint, from which one Level 2 measurement is retrieved.
- A **measurement period** is the time span over which the images contributing to one Level 2 map or measurement are collected.
