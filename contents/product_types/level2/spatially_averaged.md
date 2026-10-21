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

A file holds a sequence of measurements along the dimension `time`, and the variables `longitude` and `latitude` give the mean position of the analysis windows that contribute to each measurement (see [Georeferencing](../../georeferencing/index.md#positions-of-analysis-windows)), as described under [Moving and fixed platforms](#moving-and-fixed-platforms).
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
                platform_speed_wrt_ground:coordinates = "time longitude latitude" ;
                platform_speed_wrt_ground:grid_mapping = "crs" ;
        double platform_course(time) ;
                platform_course:long_name = "mean platform course during the measurement" ;
                platform_course:standard_name = "platform_course" ;
                platform_course:units = "degree" ;
                platform_course:coordinates = "time longitude latitude" ;
                platform_course:grid_mapping = "crs" ;
```

The near-surface current retrieved within the same analysis windows may be stored with any spatially averaged product, in `eastward_sea_water_velocity` and `northward_sea_water_velocity`, for windows that move with the platform after subtracting the mean platform velocity (see [Level 2 variables](../../metadata_attributes/level2_variables.md)).

The wavenumber spectra do not depend on the frame of reference, since a wavenumber is the same whether seen from the ground or from the moving water.
Wave frequencies and periods do: relative to the ground, the current shifts the frequency of each wave component by the Doppler shift.
Whether the frequencies and periods of the Level 2b products include this shift is given by [`wave_frequency_frame`](index.md#processing-parameters).
In windows that move with the platform, the observed frequencies are encounter frequencies, which are also shifted by the platform velocity; the Level 2b products give them as intrinsic or absolute frequencies all the same.

The wave energy density is calibrated, typically against a reference wave data set, and the parameters of this calibration should be recorded in the `wave_calibration` group (see [Wave calibration parameters](../../metadata_attributes/wave_calibration.md)).

## Moving and fixed platforms

The layout of a file follows the [discrete sampling geometries][cf-dsg] of CF, according to whether the platform moves:

- From a moving platform, which must set the global attribute [`platform_is_mobile`](../../metadata_attributes/optional_global.md) to `"true"`, the measurements form a **trajectory**: `longitude` and `latitude` have the dimension `time`, since the mean position of the windows moves with the platform.
- From a fixed platform, they form a **time series**: `longitude` and `latitude` are scalar, since the windows are fixed to the Earth and their mean position does not change. Windows that move with the platform do not apply, and `analysis_window_motion` is omitted or `earth_fixed`.

The file should declare its layout by the global attribute `featureType`, `"trajectory"` or `"timeSeries"`, and identify the trajectory or time series by a scalar string variable, `trajectory` with `cf_role = "trajectory_id"` or `station` with `cf_role = "timeseries_id"`, whose value names the platform, the cruise, or the station.
The data variables carry `coordinates = "time longitude latitude"`, which CF requires of discrete sampling geometries.
Since the location of a discrete sampling geometry is a point, CF provides for data that are averaged over an area by assigning them a representative position ([CF][cf-dsg], section 9.1), here the mean position of the windows; the data variables that hold averaged quantities should state this averaging by `cell_methods = "area: mean"` ([CF][cf-cell-methods], section 7.3).
Wave parameters from a fixed platform hold, for example:

```
dimensions:
        time = 29 ;
variables:
        string station ; // recommended
                station:long_name = "name of the radar station" ;
                station:cf_role = "timeseries_id" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_significant_height(time) ;
                sea_surface_wave_significant_height:long_name = "significant wave height" ;
                sea_surface_wave_significant_height:standard_name = "sea_surface_wave_significant_height" ;
                sea_surface_wave_significant_height:units = "m" ;
                sea_surface_wave_significant_height:coordinates = "time longitude latitude" ;
                sea_surface_wave_significant_height:cell_methods = "area: mean" ; // recommended

// global attributes:
                :featureType = "timeSeries" ; // recommended
```

## Variables

The file holds the following variables, in addition to those of its product (see [Product types](#product-types)).
The data variables of a product are defined under [Level 2 variables](../../metadata_attributes/level2_variables.md), where `(…)` stands for the dimension `time`.
Where the dimensions differ between a moving and a fixed platform, the second is that of a fixed platform.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Recommended. Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). Without it, `latitude` and `longitude` refer to WGS 84. |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each measurement. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)` or scalar; `degrees_east` | Required. Mean longitude of the analysis windows contributing to each measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)` or scalar; `degrees_north` | Required. Mean latitude of the analysis windows contributing to each measurement. |
| `platform_speed_wrt_ground`<br><small>[CF][cf-names]</small> | double `(time)`; `m s-1` | Required if `analysis_window_motion` is `platform_fixed`; omitted otherwise. Mean speed over ground of the platform during each measurement (see [Measurements](#measurements)). |
| `platform_course`<br><small>[CF][cf-names]</small> | double `(time)`; `degree` | Required if `analysis_window_motion` is `platform_fixed`; omitted otherwise. Mean course of the platform during each measurement. |
| `radar_longitude`<br><small>SOMaR</small> | double `(time)` or scalar; `degrees_east` | Optional. Longitude of the radar antenna at the start of each measurement (see [Georeferencing](../../georeferencing/index.md#radar-position)). |
| `radar_latitude`<br><small>SOMaR</small> | double `(time)` or scalar; `degrees_north` | Optional. Latitude of the radar antenna at the start of each measurement. |
| `trajectory`<br><small>[CF][cf-dsg]</small> | string | Recommended from a moving platform. Identifier of the trajectory, with `cf_role = "trajectory_id"` (see [Moving and fixed platforms](#moving-and-fixed-platforms)). |
| `station`<br><small>[CF][cf-dsg]</small> | string | Recommended from a fixed platform. Identifier of the time series, with `cf_role = "timeseries_id"`. |
| `eastward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(time)`; `m s-1` | Optional. Eastward component of the near-surface current retrieved within the same analysis windows (see [Level 2 variables](../../metadata_attributes/level2_variables.md)). |
| `northward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(time)`; `m s-1` | Optional. Northward component of the near-surface current retrieved within the same analysis windows. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(time)`; bit flags | Recommended. Quality flag. 0 is good; each bit that is set marks a failed check (see [Quality flags](index.md#quality-flags)). |
{: .variable-table }

The data variables carry `coordinates = "time longitude latitude"`, and `grid_mapping = "crs"` if the file holds a `crs`.
The processing parameters of spatially averaged products are recorded in global attributes (see [Processing parameters](index.md#processing-parameters)).

## Product types

The following products are spatially averaged products.
For each, the table lists the data variables that it requires, recommends, or allows, in addition to the variables above; they are defined under [Level 2 variables](../../metadata_attributes/level2_variables.md).

| Product | `product_type` | Variables |
|---|---|---|
| [Surface wave two-dimensional wavenumber spectra](../../annex/wave_wavenumber_spectra.md) (L2a) | `wave_wavenumber_spectra` | **Required:** `eastward_wave_wavenumber`, `northward_wave_wavenumber`, `sea_surface_wave_wavenumber_variance_spectral_density`<br>**Optional:** `wave_signal`, `background_noise`, `sea_surface_wave_mean_square_slope` |
| [Surface wave frequency-direction spectra](../../annex/wave_frequency_direction_spectra.md) (L2b) | `wave_frequency_direction_spectra` | **Required:** `wave_frequency`, `sea_surface_wave_from_direction`, `sea_surface_wave_directional_variance_spectral_density` |
| [Surface wave one-dimensional frequency spectra](../../annex/wave_frequency_spectra.md) (L2b) | `wave_frequency_spectra` | **Required:** `wave_frequency`, `sea_surface_wave_variance_spectral_density`<br>**Optional:** `sea_surface_wave_directional_spread`, `sea_surface_wave_mean_from_direction` |
| [Peak and mean wave parameters](../../annex/wave_parameters.md) (L2b) | `wave_parameters` | **Recommended:** `sea_surface_wave_significant_height`, `sea_surface_wave_from_direction_at_variance_spectral_density_maximum`, `sea_surface_wave_period_at_variance_spectral_density_maximum`, `sea_surface_wave_mean_period`, `sea_surface_wave_from_direction`<br>**Optional:** `wave_signal`, `background_noise`, `sea_surface_wave_mean_square_slope` |
{: .product-type-table }

Of the five bulk wave parameters that the peak and mean wave parameters recommend, at least one is required.

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
[cf-dsg]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#discrete-sampling-geometries
[cf-cell-methods]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#cell-methods
