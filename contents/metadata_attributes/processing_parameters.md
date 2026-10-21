---
title: Processing parameters
layout: default
parent: Metadata
nav_order: 5
---

# Processing parameters

The processing parameters needed to interpret the Level 2 products are recorded in the following global attributes, in addition to the [shared global attributes](index.md).
They document how the data were obtained and are recommended for the products named in each row, except `analysis_window_motion`, which is optional: windows that move with the platform require further variables, so its default cannot be mistaken.

| Attribute | Values | Description |
|---|---|---|
| `analysis_window_motion`<br><small>SOMaR</small> | String; `earth_fixed` or `platform_fixed` | Optional, for spatially averaged products. Whether the analysis windows are fixed to the Earth for the duration of a measurement period (`earth_fixed`) or move with the platform at a fixed bearing and range (`platform_fixed`; see [Measurements](../product_types/spatially_averaged.md#measurements)). Assumed `earth_fixed` if missing; `platform_fixed` requires `platform_speed_wrt_ground` and `platform_course`. |
| `analysis_window_shape`<br><small>SOMaR</small> | String; `circle`, `square`, `rectangle`, or a name chosen by the processor | Recommended for products retrieved within analysis windows: maps and spatially averaged products. The shape of the analysis windows, which defines `analysis_window_size`. A shape other than these three is named with a short lowercase name with underscores and described in the `comment` global attribute. |
| `analysis_window_size`<br><small>SOMaR</small> | Number or pair of numbers; `m` | Recommended for products retrieved within analysis windows: maps and spatially averaged products. The size of the analysis windows: the diameter of a `circle`, the side length of a `square`, or the east–west and north–south extents of a `rectangle`, in that order. |
| `analysis_window_spacing`<br><small>SOMaR</small> | Number; `m` | Recommended for maps. The distance between the centers of neighboring analysis windows, i.e. the grid spacing of the map. |
| `averaging_duration`<br><small>SOMaR</small> | Number; `s` | Recommended for `relative_roughness` and `relative_roughness_mosaic`, and for `sea_ice_drift` whose images are averaged before the drift is retrieved. The nominal duration over which Level 1b images are averaged: into one relative roughness image or mosaic pixel, or into each of the two correlated images of a drift vector. The window of an individual grid cell may be shorter, but never longer. |
| `measurement_duration`<br><small>SOMaR</small> | Number; `s` | Recommended for `relative_roughness_mosaic`, maps, and spatially averaged products. The duration of the radar image sequence used for each mosaic, map, or spatially averaged measurement. |
| `number_of_analysis_windows`<br><small>SOMaR</small> | Integer | Recommended for spatially averaged products. The number of analysis windows averaged into each measurement. |
| `number_of_images`<br><small>SOMaR</small> | Integer | Recommended for maps and spatially averaged products. The number of radar images used for each map or spatially averaged measurement. Omitted for `sea_ice_drift`, whose maps are described by `time_lag` and `averaging_duration` instead. |
| `retrieval_method`<br><small>SOMaR</small> | String; a name from [Retrieval methods](#retrieval-methods) or a name chosen by the processor | Recommended for maps; optional for the others. The method by which the product is retrieved. |
| `time_lag`<br><small>SOMaR</small> | Number; `s` | Recommended for `sea_ice_drift`. The time between the two correlated images of a drift vector. |
| `wave_frequency_frame`<br><small>SOMaR</small> | String; `intrinsic` or `absolute` | Recommended for `wave_frequency_direction_spectra`, `wave_frequency_spectra`, and `wave_parameters`. The frame of reference of the wave frequencies and periods: `intrinsic` relative to the moving water, with the Doppler shift by the current removed, or `absolute` relative to the ground, with the Doppler shift included. Assumed `intrinsic` if missing; since nothing else in the file shows the frame, it should be stated even when it is `intrinsic`. |
{: .attribute-table }

## Retrieval methods

SOMaR defines the content of the Level 2 products, not the methods by which they are retrieved.
The method of a product is named by the global attribute [`retrieval_method`](#processing-parameters), using one of the following names where it applies.

| Name | Products | Description |
|---|---|---|
| `dispersion_relation_least_squares_fit` | `currents`, `currents_profile`, `bathymetry` | Least-squares fit of the wave signal in the wavenumber-frequency spectrum of an analysis window to the linear dispersion relation (Young et al. [1985](../references/index.md#young-1985); Senet et al. [2001](../references/index.md#senet-2001); Bell [1999](../references/index.md#bell-1999)). |
| `normalized_scalar_product` | `currents` | Maximization of the normalized scalar product between the wavenumber-frequency spectrum of an analysis window and a filter following the dispersion relation (Serafino et al. [2010](../references/index.md#serafino-2010)). |
| `cross_correlation` | `sea_ice_drift` | Displacement at the peak of the cross-correlation between two images (Lund et al. [2018](../references/index.md#lund-2018)). |
| `optical_flow` | `sea_ice_drift` | Displacement field estimated by optical flow between two images (Thomson et al. [2021](../references/index.md#thomson-2021)). |

Another method is named by the processor with a short lowercase name with underscores, so that files using the same method can be recognized; the method is then described in the `comment` global attribute.
For any method, the underlying literature is given in the `references` global attribute of [CF][cf-description].

Each product requires only the variables that every method yields, such as the current vector, and recommends the quality flag `measurement_quality`.
The diagnostics that only some methods yield are optional, and SOMaR names the known ones so that processors using the same method store them alike: the standard errors and `number_of_wave_coordinates` of a least-squares fit, the `signal_to_noise_ratio` of the current retrieval, and the `correlation_coefficient` of a cross-correlation.
A processor may store further diagnostics; the variables they describe list them in their `ancillary_variables` attribute.

[cf-description]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents
