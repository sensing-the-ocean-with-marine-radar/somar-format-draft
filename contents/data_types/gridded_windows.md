---
title: gridded_windows (L2a)
layout: default
parent: SOMaR data types
nav_order: 6
---

# gridded_windows (L2a)

Files of the data type `gridded_windows` hold Level 2a values in analysis windows, one value set per window, retrieved from a sequence of radar images within the window, where the windows form a regular lattice that stays fixed to the Earth for the duration of a measurement period ([`analysis_window_motion`](../metadata_attributes/processing_parameters.md#analysis_window_motion) is omitted or `earth_fixed`).
Windows that move with the platform, or that do not form such a lattice, are stored as [`discrete_windows`](discrete_windows.md).
The annex gives a complete [example](../annex/current_maps.md#example).

## Grids

The lattice is the [geographic grid](../georeferencing/index.md#geographic-grid) or the [local grid](../georeferencing/index.md#local-grid) of the measurement, and the center of each cell is the center of one window.
From a moving platform, each measurement period has its own [time-bounded grid](../georeferencing/index.md#time-bounded-grids), in a `time_<YYYYMMDDHHMMSS>` group; from a fixed platform, all measurement periods share a [single grid](../georeferencing/index.md#single-grid) in the root group, with the leading dimension `time`.
From a fixed platform, the local grid may be a [rotated local grid](../georeferencing/index.md#rotated-local-grids); the geographic grid is not rotated.

## Variables

Each grid holds the following variables, in each `time_<YYYYMMDDHHMMSS>` group or in the root group of a file from a fixed platform, in addition to those of its product (see [Products](#products)).
The data variables of a product are defined under [Product variables](product_variables.md), where `(…)` stands for the dimensions of the grid, preceded by `time` from a fixed platform.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required on the local grid; recommended on the geographic grid. Coordinate reference system (see [Georeferencing](../georeferencing/index.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double, or double `(time)` from a fixed platform; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of the measurement period. Carries `bounds = "time_bounds"` where `time_bounds` is present. |
| `time_bounds`<br><small>[CF][cf-bounds]</small> | double `(nv)`, or double `(time, nv)` from a fixed platform; `seconds since 1970-01-01T00:00:00Z` | Optional. Start and end of the measurement period, along the dimension `nv` of size 2 ([CF][cf-bounds] section 7.1). |
| `x`<br><small>SOMaR</small> | double `(x)`; `m` | Required on the local grid. Distance east of the radar antenna at the start of the measurement, or along the x axis of a rotated grid. |
| `y`<br><small>SOMaR</small> | double `(y)`; `m` | Required on the local grid. Distance north of the radar antenna at the start of the measurement, or along the y axis of a rotated grid. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(longitude)` on the geographic grid, `(y, x)` on the local grid; `degrees_east` | Required. Longitude of the centers of the analysis windows. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(latitude)` on the geographic grid, `(y, x)` on the local grid; `degrees_north` | Required. Latitude of the centers of the analysis windows. |
| `radar_longitude`<br><small>SOMaR</small> | double; `degrees_east` | Optional. Longitude of the radar antenna at the start of the measurement period, or of the fixed radar antenna, from which the range and bearing of each analysis window can be recovered. |
| `radar_latitude`<br><small>SOMaR</small> | double; `degrees_north` | Optional. Latitude of the radar antenna at the start of the measurement period, or of the fixed radar antenna, from which the range and bearing of each analysis window can be recovered. |
| `measurement_quality`<br><small>SOMaR</small> | ubyte `(…)`; bit flags | Recommended. Quality flag. 0 is good; each bit that is set marks a failed check (see [Quality flags](../metadata_attributes/quality_flags.md)). |
{: .variable-table }

The data variables carry `grid_mapping = "crs"` if the group holds a `crs`, and, on the local grid, `coordinates = "longitude latitude"`.
The processing parameters are recorded in global attributes (see [Processing parameters](../metadata_attributes/processing_parameters.md)).

## Products

The following products have the data type `gridded_windows`.
For each, the table lists the data variables that it requires, recommends, or allows, in addition to the variables above; they are defined under [Product variables](product_variables.md).
The name of each product links to the table of its file contents in the annex, which lists everything a file of the product holds.

| Product | `data_type` | `product_type` | Variables |
|---|---|---|---|
| [Near-surface current maps](../annex/current_maps.md#file-contents) (L2a) | `gridded_windows` | `currents` | **Required:** [`eastward_sea_water_velocity`](product_variables.md#eastward_sea_water_velocity), [`northward_sea_water_velocity`](product_variables.md#northward_sea_water_velocity)<br>**Recommended:** [`mean_wavenumber`](product_variables.md#mean_wavenumber)<br>**Optional:** [`eastward_sea_water_velocity_standard_error`](product_variables.md#eastward_sea_water_velocity_standard_error), [`northward_sea_water_velocity_standard_error`](product_variables.md#northward_sea_water_velocity_standard_error), [`number_of_fitted_spectral_points`](product_variables.md#number_of_fitted_spectral_points), [`signal_to_noise_ratio`](product_variables.md#signal_to_noise_ratio) |
| [Near-surface current profile maps](../annex/current_profile_maps.md#file-contents) (L2a) | `gridded_windows` | `currents_profile` | **Required:** [`wavenumber_bin`](product_variables.md#wavenumber_bin), [`wavenumber_bin_bounds`](product_variables.md#wavenumber_bin_bounds), [`eastward_sea_water_velocity`](product_variables.md#eastward_sea_water_velocity), [`northward_sea_water_velocity`](product_variables.md#northward_sea_water_velocity)<br>**Recommended:** [`mean_wavenumber`](product_variables.md#mean_wavenumber)<br>**Optional:** [`eastward_sea_water_velocity_standard_error`](product_variables.md#eastward_sea_water_velocity_standard_error), [`northward_sea_water_velocity_standard_error`](product_variables.md#northward_sea_water_velocity_standard_error), [`number_of_fitted_spectral_points`](product_variables.md#number_of_fitted_spectral_points), [`signal_to_noise_ratio`](product_variables.md#signal_to_noise_ratio) |
| [Bathymetric maps](../annex/depth_maps.md#file-contents) (L2a) | `gridded_windows` | `bathymetry` | **Required:** [`sea_floor_depth_below_sea_surface`](product_variables.md#sea_floor_depth_below_sea_surface)<br>**Recommended:** [`mean_wavenumber`](product_variables.md#mean_wavenumber)<br>**Optional:** [`sea_floor_depth_below_sea_surface_standard_error`](product_variables.md#sea_floor_depth_below_sea_surface_standard_error), [`number_of_fitted_spectral_points`](product_variables.md#number_of_fitted_spectral_points) |
| [Sea ice drift maps](../annex/sea_ice_drift.md#file-contents) (L2a) | `gridded_windows` | `sea_ice_drift` | **Required:** [`eastward_sea_ice_velocity`](product_variables.md#eastward_sea_ice_velocity), [`northward_sea_ice_velocity`](product_variables.md#northward_sea_ice_velocity)<br>**Optional:** [`correlation_coefficient`](product_variables.md#correlation_coefficient), [`eastward_sea_ice_velocity_backward`](product_variables.md#eastward_sea_ice_velocity_backward), [`northward_sea_ice_velocity_backward`](product_variables.md#northward_sea_ice_velocity_backward), [`correlation_coefficient_backward`](product_variables.md#correlation_coefficient_backward) |
{: .product-type-table }

In current profile maps, all data variables, `measurement_quality` included, have the additional dimension [`wavenumber_bin`](product_variables.md#wavenumber_bin), one layer per wavenumber band.
On a rotated local grid, the x and y components of the currents and of the sea ice drift take the place of the eastward and northward components listed here.

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/95/build/cf-standard-name-table.html
[cf-bounds]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#cell-boundaries
