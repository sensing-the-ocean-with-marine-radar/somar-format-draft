---
title: Level 2 data
layout: default
parent: SOMaR data types
#nav_order: 1
---

# Level 2 data

Level 2 products are geophysical quantities derived from sequences of Level 1b images, such as sea surface roughness, near-surface currents, bathymetry, sea ice drift, and surface waves.
They are divided into two sublevels according to how they are obtained: Level 2a products are retrieved directly from the Level 1b image sequences, while Level 2b products are derived from Level 2a products rather than from the images themselves.

## Level 2a

Level 2a products are the direct result of a retrieval applied to Level 1b image sequences.
[Roughness images](roughness_images.md) and [roughness image mosaics](roughness_mosaics.md) are mapped onto time-bounded local Cartesian grids stored as NetCDF groups.
[Near-surface current maps](current_maps.md), [bathymetric maps](depth_maps.md), and [sea ice drift maps](sea_ice_drift.md) are retrieved within analysis windows placed on an overlapping, approximately regular grid that follows the platform, and are stored as one two-dimensional map per measurement period, each in its own NetCDF group, on a longitude/latitude grid.
[Surface wave two-dimensional wavenumber spectra](wave_wavenumber_spectra.md) give one spectrum per analysis window along the platform's path, indexed by `time` with accompanying `longitude` and `latitude`.

## Level 2b

Level 2b products are computed from Level 2a products and therefore inherit their sampling, calibration, and quality control.
Currently all Level 2b products are surface wave products derived from the Level 2a two-dimensional wavenumber spectra: [two-dimensional frequency spectra](wave_frequency_direction_spectra.md), [one-dimensional frequency spectra](wave_frequency_spectra.md), and [peak and mean wave parameters](wave_parameters.md).
Like the wavenumber spectra, they are indexed by `time` with accompanying `longitude` and `latitude` and a `measurement_quality` flag.
