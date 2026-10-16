---
title: Level 2 products
layout: default
parent: SOMaR product types
nav_order: 2
has_children: true
---

# Level 2 products

Level 2 products are geophysical quantities derived from sequences of Level 1b images, such as sea surface roughness, near-surface currents, bathymetry, sea ice drift, and surface waves.
They are divided into two sublevels according to how they are obtained: Level 2a products are retrieved directly from the Level 1b image sequences, while Level 2b products are derived from Level 2a products rather than from the images themselves.

## Level 2a

Level 2a products are the direct result of a retrieval applied to Level 1b image sequences.
[Roughness images](roughness_images.md) and [roughness image mosaics](roughness_mosaics.md) are mapped onto time-bounded local Cartesian grids stored as NetCDF groups.
[Near-surface current maps](current_maps.md), [bathymetric maps](depth_maps.md), and [sea ice drift maps](sea_ice_drift.md) are retrieved within overlapping analysis windows that follow the platform, and are stored as one two-dimensional map per measurement period, each in its own NetCDF group, on a regular longitude/latitude grid or, depending on the processor, on a local grid (see [Map products](#map-products)).
[Surface wave two-dimensional wavenumber spectra](wave_wavenumber_spectra.md) give one spectrum per measurement along the platform's path, averaged over the analysis windows that contribute to it and indexed by `time` with accompanying `longitude` and `latitude`.

## Level 2b

Level 2b products are computed from Level 2a products and therefore inherit their sampling, calibration, and quality control.
Currently all Level 2b products are surface wave products derived from the Level 2a two-dimensional wavenumber spectra: [frequency-direction spectra](wave_frequency_direction_spectra.md), [one-dimensional frequency spectra](wave_frequency_spectra.md), and [peak and mean wave parameters](wave_parameters.md).
Like the wavenumber spectra, they are indexed by `time` with accompanying `longitude` and `latitude` and a `measurement_quality` flag.

## Map products

[Near-surface current maps](current_maps.md), [current profile maps](current_maps.md#near-surface-current-profile-maps), [bathymetric maps](depth_maps.md), and [sea ice drift maps](sea_ice_drift.md) share one structure.
The analysis windows of one measurement period form a map that spans the radar footprint, and with a moving vessel the area covered changes from one period to the next.
All maps belonging to one file are therefore stored as sibling NetCDF groups, one group per measurement period, named `time_<YYYYMMDDHHMMSS>` (UTC) after the start time of that period, as for the [roughness images](roughness_images.md).
Within each group, the scalar variable `time` gives the start time of the period, and the variables are stored on a two-dimensional grid with the dimensions `(latitude, longitude)`.
Since the radar footprint is circular, the cells in the corners of the grid hold the `_FillValue`, as do the cells of analysis windows without a result.
The coordinate variables `latitude` and `longitude` give the centers of the analysis windows; they are one-dimensional because the windows lie on an Earth-fixed lattice (see [Georeferencing](../../georeferencing/index.md#positions-of-analysis-windows)).
A processor whose analysis windows lie on a local grid around the radar instead uses the [local-grid form](current_maps.md#local-grid-form).
The radar position for the period may optionally be stored in the scalar variables [`radar_longitude` and `radar_latitude`](../../georeferencing/index.md#radar-position).
