---
title: "Level 2: Geophysical quantities"
layout: default
parent: SOMaR product types
nav_order: 2
has_children: true
---

# Level 2: Geophysical quantities

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
Like the wavenumber spectra, they are indexed by `time` with accompanying `longitude` and `latitude` and a `measurement_quality` bit flag.

## Map products

[Near-surface current maps](current_maps.md), [current profile maps](current_profile_maps.md), [bathymetric maps](depth_maps.md), and [sea ice drift maps](sea_ice_drift.md) share one structure.
The analysis windows of one measurement period form a map that spans the radar footprint, and with a moving vessel the area covered changes from one period to the next.
All maps belonging to one file are therefore stored as sibling NetCDF groups, one group per measurement period, named `time_<YYYYMMDDHHMMSS>` (UTC) after the start time of that period, as for the [roughness images](roughness_images.md).
Within each group, the scalar variable `time` gives the start time of the period, and the variables are stored on a two-dimensional grid with the dimensions `(latitude, longitude)`.
Since the radar footprint is circular, the cells in the corners of the grid hold the `_FillValue`, as do the cells of analysis windows without a result or inside an [obstructed sector](../../metadata_attributes/radar_parameters.md#obstructed-sectors).
The coordinate variables `latitude` and `longitude` give the centers of the analysis windows; they are one-dimensional because the windows lie on an Earth-fixed lattice (see [Georeferencing](../../georeferencing/index.md#positions-of-analysis-windows)).
A processor whose analysis windows lie on a local grid around the radar instead uses the [local-grid form](current_maps.md#local-grid-form).
The radar position for the period may optionally be stored in the scalar variables [`radar_longitude` and `radar_latitude`](../../georeferencing/index.md#radar-position).

The processing parameters of the maps are recorded in global attributes (see [Processing parameters](#processing-parameters)).

## Wave products

The wave products ([wavenumber spectra](wave_wavenumber_spectra.md), [frequency-direction spectra](wave_frequency_direction_spectra.md), [frequency spectra](wave_frequency_spectra.md), and [wave parameters](wave_parameters.md)) are retrieved within a small number of analysis windows that are spread across the radar field of view.
Each measurement is the average over these analysis windows, and its `longitude` and `latitude` give their mean position (see [Georeferencing](../../georeferencing/index.md#positions-of-analysis-windows)).
The analysis windows are fixed to the Earth for the duration of a measurement period, so that their bearing and range from a moving platform change during the period.
Their placement is left to the processor and should be described in the `comment` global attribute.

The wavenumber spectra do not depend on the frame of reference, since a wavenumber is the same whether seen from the ground or from the moving water.
Wave frequencies and periods do: relative to the ground, the current shifts the frequency of each wave component by the Doppler shift.
Whether the frequencies and periods of the Level 2b products include this shift is given by [`wave_frequency_frame`](#processing-parameters).

## Retrieval methods

SOMaR defines the content of the Level 2 products, not the methods by which they are retrieved.
The method of a product is named by the global attribute [`retrieval_method`](#processing-parameters), using one of the following names where it applies.

| Name | Products | Description |
|---|---|---|
| `dispersion_relation_least_squares_fit` | [Currents](current_maps.md), [current profiles](current_profile_maps.md), [bathymetry](depth_maps.md) | Least-squares fit of the wave signal in the wavenumber-frequency spectrum of an analysis window to the linear dispersion relation (Young et al. [1985](../../references/index.md#young-1985); Senet et al. [2001](../../references/index.md#senet-2001); Bell [1999](../../references/index.md#bell-1999)). |
| `normalized_scalar_product` | [Currents](current_maps.md) | Maximization of the normalized scalar product between the wavenumber-frequency spectrum of an analysis window and a filter following the dispersion relation (Serafino et al. [2010](../../references/index.md#serafino-2010)). |
| `cross_correlation` | [Sea ice drift](sea_ice_drift.md) | Displacement at the peak of the cross-correlation between two images (Lund et al. [2018](../../references/index.md#lund-2018)). |
| `optical_flow` | [Sea ice drift](sea_ice_drift.md) | Displacement field estimated by optical flow between two images (Thomson et al. [2021](../../references/index.md#thomson-2021)). |

Another method is named by the processor with a short lowercase name with underscores, so that files using the same method can be recognized; the method is then described in the `comment` global attribute.
For any method, the underlying literature is given in the `references` global attribute of [CF][cf-description].

Each product requires only the variables that every method yields, such as the current vector and `measurement_quality`.
The diagnostics that only some methods yield are optional, and SOMaR names the known ones so that processors using the same method store them alike: the standard errors and `number_of_wave_coordinates` of a least-squares fit, the `signal_to_noise_ratio` of the current retrieval, and the `correlation_coefficient` of a cross-correlation.
A processor may store further diagnostics; the variables they describe list them in their `ancillary_variables` attribute.

## Quality flags

Every Level 2 product carries a `measurement_quality` variable of type `ubyte`, a bit flag in the sense of [CF][cf-flags]: 0 means that the measurement passed all checks, and each bit that is set marks a check that it failed.
The checks depend on the retrieval method and the processor, and are therefore defined by each file through the `flag_masks` and `flag_meanings` attributes.
The flag meanings used in the examples are recommended for the checks they describe, so that the same check carries the same name in the files of different processors.

## Processing parameters

The processing parameters needed to interpret the [roughness images](roughness_images.md), the [roughness image mosaics](roughness_mosaics.md), the [map products](#map-products), and the [wave products](#wave-products) are recorded in the following global attributes, in addition to the [shared global attributes](../../metadata_attributes/index.md).

| Attribute | Values | Description |
|---|---|---|
| `analysis_window_shape`<br><small>SOMaR</small> | String; `circle`, `square`, `rectangle`, or a name chosen by the processor | Required for map and wave products retrieved within analysis windows. The shape of the analysis windows, which defines `analysis_window_size`. A shape other than these three is named with a short lowercase name with underscores and described in the `comment` global attribute. |
| `analysis_window_size`<br><small>SOMaR</small> | Number or pair of numbers; `m` | Required for map and wave products retrieved within analysis windows. The size of the analysis windows: the diameter of a `circle`, the side length of a `square`, or the east–west and north–south extents of a `rectangle`, in that order. |
| `analysis_window_spacing`<br><small>SOMaR</small> | Number; `m` | Required for map products. The distance between the centers of neighboring analysis windows, i.e. the grid spacing of the map. |
| `averaging_duration`<br><small>SOMaR</small> | Number; `s` | Required for [roughness images](roughness_images.md) and [roughness image mosaics](roughness_mosaics.md), and for [sea ice drift maps](sea_ice_drift.md) whose images are averaged before the drift is retrieved. The nominal duration over which Level 1b images are averaged: into one roughness image or mosaic pixel, or into each of the two correlated images of a drift vector. The window of an individual grid cell may be shorter, but never longer. |
| `measurement_duration`<br><small>SOMaR</small> | Number; `s` | Required for [roughness image mosaics](roughness_mosaics.md), map products, and wave products. The duration of the radar image sequence used for each mosaic, map, or wave measurement. |
| `number_of_analysis_windows`<br><small>SOMaR</small> | Integer | Required for wave products. The number of analysis windows averaged into each measurement. |
| `number_of_images`<br><small>SOMaR</small> | Integer | Required for map and wave products. The number of radar images used for each map or wave measurement. Omitted for [sea ice drift maps](sea_ice_drift.md), which are described by `time_lag` and `averaging_duration` instead. |
| `retrieval_method`<br><small>SOMaR</small> | String; a name from [Retrieval methods](#retrieval-methods) or a name chosen by the processor | Required for map products; optional for the others. The method by which the product is retrieved. |
| `wave_frequency_frame`<br><small>SOMaR</small> | String; `intrinsic` or `absolute` | Required for [frequency-direction spectra](wave_frequency_direction_spectra.md), [frequency spectra](wave_frequency_spectra.md), and [wave parameters](wave_parameters.md). The frame of reference of the wave frequencies and periods: `intrinsic` relative to the moving water, with the Doppler shift by the current removed, or `absolute` relative to the ground, with the Doppler shift included. |
{: .attribute-table }

[cf-description]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents
[cf-flags]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#flags
