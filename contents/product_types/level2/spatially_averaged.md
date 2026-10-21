---
title: Spatially averaged products
layout: default
parent: "Level 2: Geophysical quantities"
grand_parent: SOMaR product types
nav_order: 2
---

# Spatially averaged products

Spatially averaged products combine the results of several analysis windows into one value set per measurement, located at the mean position of the windows.
What sets them apart from [gridded products](gridded.md) is not that their values are averages over an area, since a map cell is an average over its analysis window too, but that the windows do not keep their own positions.
The windows need not span the radar footprint; "spatially" distinguishes this averaging from the averaging over time that all Level 2 products share.
The spatially averaged products are currently the surface wave products: two-dimensional wavenumber spectra, frequency-direction spectra, one-dimensional frequency spectra, and bulk wave parameters.
They are listed, with the variables that each of them holds, under [Product types](#product-types).

## Measurements

A file holds a sequence of measurements along the dimension `time`, and the variables `longitude` and `latitude`, with the same dimension, give the mean position of the analysis windows that contribute to each measurement (see [Georeferencing](../../georeferencing/index.md#positions-of-analysis-windows)).
The windows are spread across the radar field of view, and their placement is left to the processor and should be described in the `comment` global attribute.
Depending on the processor, the analysis windows are fixed to the Earth for the duration of a measurement period, so that their bearing and range from a moving platform change during the period, or they move with the platform at a fixed bearing and range; which of the two is given by [`analysis_window_motion`](index.md#processing-parameters).
Windows that move with the platform cover a track rather than a fixed area during the period.
Their retrieval assumes that the wave field is spatially homogeneous along this track and that the platform moves at constant velocity during the period, and the mean platform velocity is subtracted afterwards from the current obtained.
This velocity is stored as the speed over ground and course of the platform, in the variables `platform_speed_wrt_ground` and `platform_course` with the dimension `time`, which are required for windows that move with the platform and omitted otherwise:

```
// excerpt: the platform velocity of a measurement with platform-fixed analysis windows
variables:
        double platform_speed_wrt_ground(time) ;
                platform_speed_wrt_ground:long_name = "mean platform speed over ground during the measurement" ;
                platform_speed_wrt_ground:standard_name = "platform_speed_wrt_ground" ;
                platform_speed_wrt_ground:units = "m s-1" ;
                platform_speed_wrt_ground:coordinates = "longitude latitude" ;
                platform_speed_wrt_ground:grid_mapping = "crs" ;
        double platform_course(time) ;
                platform_course:long_name = "mean platform course during the measurement" ;
                platform_course:standard_name = "platform_course" ;
                platform_course:units = "degree" ;
                platform_course:coordinates = "longitude latitude" ;
                platform_course:grid_mapping = "crs" ;
```

The wavenumber spectra do not depend on the frame of reference, since a wavenumber is the same whether seen from the ground or from the moving water.
Wave frequencies and periods do: relative to the ground, the current shifts the frequency of each wave component by the Doppler shift.
Whether the frequencies and periods of the Level 2b products include this shift is given by [`wave_frequency_frame`](index.md#processing-parameters).
In windows that move with the platform, the observed frequencies are encounter frequencies, which are also shifted by the platform velocity; the Level 2b products give them as intrinsic or absolute frequencies all the same.

The wave energy density is calibrated, typically against a reference wave data set, and the parameters of this calibration should be recorded in the `wave_calibration` group (see [Wave calibration parameters](../../metadata_attributes/wave_calibration.md)).

## Variables

The file holds the following variables, in addition to those of its product (see [Product types](#product-types)).
The data variables of a product are defined under [Level 2 variables](../../metadata_attributes/level2_variables.md), where `(…)` stands for the dimension `time`.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Recommended. Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). Without it, `latitude` and `longitude` refer to WGS 84. |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each measurement. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_east` | Required. Mean longitude of the analysis windows contributing to each measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_north` | Required. Mean latitude of the analysis windows contributing to each measurement. |
| `platform_speed_wrt_ground`<br><small>[CF][cf-names]</small> | double `(time)`; `m s-1` | Required if `analysis_window_motion` is `platform_fixed`; omitted otherwise. Mean speed over ground of the platform during each measurement (see [Measurements](#measurements)). |
| `platform_course`<br><small>[CF][cf-names]</small> | double `(time)`; `degree` | Required if `analysis_window_motion` is `platform_fixed`; omitted otherwise. Mean course of the platform during each measurement. |
| `radar_longitude`<br><small>SOMaR</small> | double `(time)`; `degrees_east` | Optional. Longitude of the radar antenna at the start of each measurement (see [Georeferencing](../../georeferencing/index.md#radar-position)). |
| `radar_latitude`<br><small>SOMaR</small> | double `(time)`; `degrees_north` | Optional. Latitude of the radar antenna at the start of each measurement. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(time)`; bit flags | Recommended. Quality flag. 0 is good; each bit that is set marks a failed check (see [Quality flags](index.md#quality-flags)). |
{: .variable-table }

The data variables carry `coordinates = "longitude latitude"`, and `grid_mapping = "crs"` if the file holds a `crs`.
The processing parameters of spatially averaged products are recorded in global attributes (see [Processing parameters](index.md#processing-parameters)).

## Product types

The following products are spatially averaged products.
For each, the table lists the data variables that it requires, recommends, or allows, in addition to the variables above; they are defined under [Level 2 variables](../../metadata_attributes/level2_variables.md).

| Product | `product_type` | Variables |
|---|---|---|
| [Surface wave two-dimensional wavenumber spectra](wave_wavenumber_spectra.md) (L2a) | `wave_wavenumber_spectra` | **Required:** `eastward_wave_wavenumber`, `northward_wave_wavenumber`, `sea_surface_wave_wavenumber_variance_spectral_density`<br>**Optional:** `wave_signal`, `background_noise`, `sea_surface_wave_mean_square_slope` |
| [Surface wave frequency-direction spectra](wave_frequency_direction_spectra.md) (L2b) | `wave_frequency_direction_spectra` | **Required:** `wave_frequency`, `sea_surface_wave_from_direction`, `sea_surface_wave_directional_variance_spectral_density` |
| [Surface wave one-dimensional frequency spectra](wave_frequency_spectra.md) (L2b) | `wave_frequency_spectra` | **Required:** `wave_frequency`, `sea_surface_wave_variance_spectral_density`<br>**Optional:** `sea_surface_wave_directional_spread`, `sea_surface_wave_mean_from_direction` |
| [Peak and mean wave parameters](wave_parameters.md) (L2b) | `wave_parameters` | **Recommended:** `sea_surface_wave_significant_height`, `sea_surface_wave_from_direction_at_variance_spectral_density_maximum`, `sea_surface_wave_period_at_variance_spectral_density_maximum`, `sea_surface_wave_mean_period`, `sea_surface_wave_from_direction`<br>**Optional:** `eastward_sea_water_velocity`, `northward_sea_water_velocity`, `wave_signal`, `background_noise`, `sea_surface_wave_mean_square_slope` |
{: .product-type-table }

Of the five bulk wave parameters that the peak and mean wave parameters recommend, at least one is required.
Their current vector is obtained from the same analysis windows as the wave parameters.

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
