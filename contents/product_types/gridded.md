---
title: Gridded products
layout: default
parent: SOMaR product types
nav_order: 2
---

# Gridded products

Gridded products give one value set for each cell of a grid that resolves the area covered by a measurement: each analysis window, or each pixel of an image, keeps its own position.
They comprise the Cartesian image sequences of Level 1b, which map each antenna revolution onto a local Cartesian grid, the relative roughness images and mosaics, which average Level 1b images on a local Cartesian grid, and the maps of near-surface currents, current profiles, bathymetry, and sea ice drift, which are retrieved within analysis windows.
The products of this kind, and the variables that each of them holds, are listed under [Product types](#product-types).
Their structure depends on whether the platform moves: a file from a moving platform, which must set the global attribute [`platform_is_mobile`](../metadata_attributes/optional_global.md#platform_is_mobile) to `"true"`, stores each measurement on its own [time-bounded grid](#time-bounded-grids), or, for Level 1b Cartesian images, all images in an [image cube with a moving origin](#image-cube-with-moving-origin), and a file from a fixed platform stores all measurements on a [single grid](#fixed-platform).

## Grids

The cells of one measurement form a grid over the area it covers: the radar footprint for a map, a relative roughness image, or a Level 1b Cartesian image, and for a mosaic an area along the platform track.
The grid is either the geographic grid or the local grid described below.
Cells without a value hold the `_FillValue`: the cells in the corners of the grid, since the radar footprint is circular, and the cells of analysis windows without a result or inside an [obstructed sector](../metadata_attributes/radar_parameters.md#obstructed-sectors).

### Geographic grid

Maps whose analysis windows lie on an Earth-fixed lattice are stored on a grid with the dimensions `(latitude, longitude)`.
The coordinate variables `latitude` and `longitude` give the centers of the analysis windows; they are one-dimensional because the windows lie on a lattice in longitude and latitude (see [Georeferencing](../georeferencing/index.md#positions-of-analysis-windows)).
On this grid, `crs` is recommended rather than required: without it, `latitude` and `longitude` refer to WGS 84.

### Local grid

Relative roughness images and mosaics, and maps whose analysis windows lie on a local grid around the radar, are stored on the local grid of the measurement: `x` and `y` give the distance in meters east and north of the radar antenna at the start of the measurement, and `crs` describes the local azimuthal equidistant projection centered on that position (see [Time-bounded local grids](../georeferencing/index.md#time-bounded-local-grids)).
In this form, `crs` is required, since its projection origin locates the grid.
A relative roughness image mosaic is stored on a single, larger local grid per measurement period, which extends along the platform track beyond the footprint of a single relative roughness image.
Maps on the local grid also store two-dimensional `longitude` and `latitude`, so that every file gives the geographic position of each analysis window.
For a map, the variables that differ from the geographic grid are:

```
// excerpt: a near-surface current map on the local grid, only the variables that differ from the geographic grid
group: time_20250115110031 {
  dimensions:
        y = 17 ;
        x = 17 ;
  variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 145.868167860183 ;
                crs:latitude_of_projection_origin = 14.9952749946079 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double x(x) ;
                x:long_name = "eastward distance from radar position at measurement start time" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from radar position at measurement start time" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        double longitude(y, x) ;
                longitude:long_name = "center longitude of current measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(y, x) ;
                latitude:long_name = "center latitude of current measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_water_velocity(y, x) ;
                eastward_sea_water_velocity:long_name = "eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:coordinates = "longitude latitude" ;
                eastward_sea_water_velocity:_FillValue = NaN ;
        ... // all other data variables likewise on (y, x), with grid_mapping and coordinates ...
  } // group time_20250115110031
```

## Time-bounded grids

With a moving platform, the area covered changes from one measurement to the next, so that a file holds a sequence of grids rather than one grid sampled repeatedly.
All grids of a file from a moving platform are therefore stored as sibling NetCDF groups, one group per measurement period, or per averaging window for relative roughness images, named `time_<YYYYMMDDHHMMSS>` (UTC) after its start time.
Within each group, the scalar variable `time` gives that start time, and the variables are stored on the two-dimensional grid of the measurement.

## Image cube with moving origin

Level 1b Cartesian images (`radar_cartesian`) are radar images, one per antenna revolution, that have been mapped from the polar coordinates of the sensor onto a regular Cartesian `x`/`y` grid, while otherwise remaining as close as possible to the underlying [Level 1a data](polar.md).
All images of a file share one grid of fixed extent and resolution, and only its origin, the position of the radar antenna at the start of each revolution, moves with the platform.
They are therefore stored as a single cube in the root group, whose data variable, [`backscatter_amplitude` or `backscatter_power`](product_variables.md), has the dimensions `(time, y, x)`, rather than as time-bounded grids, which would take thousands of groups for the short-lived images of one file.
The grids of the Level 2 products, by contrast, can change their extent and dimensions from one measurement to the next with the motion of the ship, and are therefore stored as time-bounded grids.
Grid cells that fall outside the valid field of view, for example those obstructed by platform superstructure, hold the `_FillValue`.
No radiometric calibration or temporal averaging is applied at this level.

### Position and orientation

`x` and `y` are distances in meters east and north of the grid origin.
The images are north-oriented: the platform heading and the azimuth and range corrections have been applied in the mapping, so no `heading` is stored. This is the main difference from the [polar products](polar.md), which are stored as recorded.

The grid origin is the position of the radar antenna at the start of each revolution, i.e. the recorded position after application of the [position offsets](../georeferencing/index.md#position-offset), and is given by `longitude` and `latitude`.
For a moving platform, they have the dimension `time`, with one value per image; for a fixed platform, they are scalar, and the cube is the [single grid](#fixed-platform) of a fixed platform.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required for a fixed platform; omitted for a moving platform. Local azimuthal equidistant projection centered on the radar antenna (see [Georeferencing](../georeferencing/index.md#time-bounded-local-grids)). |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each revolution. |
| `x`<br><small>SOMaR</small> | double `(x)`; `m` | Required. Distance east of the grid origin. |
| `y`<br><small>SOMaR</small> | double `(y)`; `m` | Required. Distance north of the grid origin. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)` or scalar; `degrees_east` | Required. Longitude (WGS 84) of the grid origin. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)` or scalar; `degrees_north` | Required. Latitude (WGS 84) of the grid origin. |
{: .variable-table }

From a moving platform, the file has no `crs` variable and the data variable no `grid_mapping` attribute, since a single coordinate reference system variable can describe only one grid origin, whereas the origin here changes from image to image (see [Georeferencing](../georeferencing/index.md#time-bounded-local-grids)).
For the same reason, `x` and `y` then carry no `standard_name`: CF defines `projection_x_coordinate` and `projection_y_coordinate` in relation to a grid mapping.
From a fixed platform, the origin does not move: the file carries a `crs` that describes the azimuthal equidistant projection centered on the radar antenna, the data variable carries `grid_mapping = "crs"`, and `x` and `y` carry the standard names `projection_x_coordinate` and `projection_y_coordinate`.

### Resampling

The polar data are resampled onto the Cartesian grid by selection, interpolation, or averaging, and the method is recorded in one attribute; as for the [azimuth regularization](polar.md#image-cube) of the polar images, the quantity on which interpolation and averaging are done is recorded in [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity).

| Attribute | Values | Description |
|---|---|---|
| `cartesian_resampling`<br><small>SOMaR</small> | String; one of `nearest_neighbor`, `linear_interpolation`, `average`, `average_or_interpolation` | Required. On the data variable: the method used to resample the polar data onto the Cartesian grid: selection of the polar sample closest to the cell center, bilinear interpolation in range and azimuth between the surrounding polar samples, the mean of all polar samples falling within the cell (cells holding no sample are set to `_FillValue`), or that mean where the cell holds at least one polar sample and linear interpolation where it holds none, typically at far range. Except for `nearest_neighbor`, the data variable also carries [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity), which states whether interpolation and averaging are done on power, amplitude, or the stored values. Should be accompanied by a `comment` describing the method in words. |
{: .attribute-table }

## Fixed platform

From a fixed platform, every measurement covers the same area on the same grid, and all measurements of a file are stored on a single grid in the root group, without `time_<YYYYMMDDHHMMSS>` groups.
The dimension `time` then precedes the dimensions of the grid, `(time, latitude, longitude)` on the geographic grid or `(time, y, x)` on the local grid, and the variable `time` gives the start time of each measurement.
A single `crs` describes the grid; on the local grid, its projection origin is the position of the radar antenna.
A file therefore holds measurements on one grid only, and a change of grid, such as a new analysis window spacing, starts a new file.
Relative roughness image mosaics are not defined for a fixed platform, since a radar that does not move covers no more than the footprint of a relative roughness image.
A near-surface current map from a fixed platform holds, for example:

```
dimensions:
        time = 15 ;
        nv = 2 ;
        latitude = 17 ;
        longitude = 17 ;
variables:
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of current measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:bounds = "time_bounds" ; // optional
        double time_bounds(time, nv) ; // optional
                time_bounds:calendar = "standard" ;
                time_bounds:long_name = "start and end time of current measurement" ;
                time_bounds:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude(longitude) ;
                longitude:long_name = "center longitude of current measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(latitude) ;
                latitude:long_name = "center latitude of current measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_water_velocity(time, latitude, longitude) ;
                eastward_sea_water_velocity:long_name = "eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:_FillValue = NaN ;
        double northward_sea_water_velocity(time, latitude, longitude) ;
                northward_sea_water_velocity:long_name = "northward component of the near-surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
                northward_sea_water_velocity:grid_mapping = "crs" ;
                northward_sea_water_velocity:_FillValue = NaN ;
```

## Variables

The time-bounded grids and the single grid of the Level 2 products hold the following variables, in each `time_<YYYYMMDDHHMMSS>` group or in the root group of a file from a fixed platform, in addition to those of their product (see [Product types](#product-types)); the variables of the Level 1b Cartesian images are given under [Image cube with moving origin](#image-cube-with-moving-origin).
The data variables of a product are defined under [Product variables](product_variables.md), where `(…)` stands for the dimensions of the grid, preceded by `time` from a fixed platform.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required on the local grid, recommended on the geographic grid. Coordinate reference system (see [Georeferencing](../georeferencing/index.md#coordinate-reference-system-variables)). Without it, `latitude` and `longitude` refer to WGS 84. |
| `time`<br><small>[CF][cf-names]</small> | double, or double `(time)` from a fixed platform; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of the measurement period, or of the averaging window of a relative roughness image. Carries `bounds = "time_bounds"` where `time_bounds` is present. |
| `time_bounds`<br><small>[CF][cf-bounds]</small> | double `(nv)`, or double `(time, nv)` from a fixed platform; `seconds since 1970-01-01T00:00:00Z` | Optional. Start and end of the measurement period, or of the nominal averaging window of a relative roughness image, along the dimension `nv` of size 2 ([CF][cf-bounds] section 7.1). |
| `x`<br><small>SOMaR</small> | double `(x)`; `m` | Required on the local grid. Distance east of the radar antenna at the start of the measurement. |
| `y`<br><small>SOMaR</small> | double `(y)`; `m` | Required on the local grid. Distance north of the radar antenna at the start of the measurement. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(longitude)` on the geographic grid, `(y, x)` on the local grid; `degrees_east` | Required for maps; omitted for relative roughness images and mosaics. Longitude of the centers of the analysis windows. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(latitude)` on the geographic grid, `(y, x)` on the local grid; `degrees_north` | Required for maps; omitted for relative roughness images and mosaics. Latitude of the centers of the analysis windows. |
| `radar_longitude`<br><small>SOMaR</small> | double; `degrees_east` | Optional for maps; omitted for relative roughness images and mosaics. Longitude of the radar antenna at the start of the measurement period, or of the fixed radar antenna (see [Georeferencing](../georeferencing/index.md#radar-position)). |
| `radar_latitude`<br><small>SOMaR</small> | double; `degrees_north` | Optional for maps; omitted for relative roughness images and mosaics. Latitude of the radar antenna at the start of the measurement period, or of the fixed radar antenna. |
| `measurement_quality`<br><small>SOMaR</small> | ubyte `(…)`; bit flags | Recommended for maps; not defined for relative roughness images and mosaics. Quality flag. 0 is good; each bit that is set marks a failed check (see [Quality flags](../metadata_attributes/quality_flags.md)). Level 1 products carry no quality flag either. |
{: .variable-table }

On the local grid, the data variables of a map carry `coordinates = "longitude latitude"`; on either grid, they carry `grid_mapping = "crs"` if the group holds a `crs`.
The processing parameters of gridded products are recorded in global attributes (see [Processing parameters](../metadata_attributes/processing_parameters.md)).

## Product types

The following products are gridded products.
For each, the table lists the data variables that it requires, recommends, or allows, in addition to the variables above; they are defined under [Product variables](product_variables.md).
The name of each product links to the table of its file contents in the annex, which lists everything a file of the product holds.

| Product | `product_type` | Variables |
|---|---|---|
| [Cartesian image sequences](../annex/level1b_cartesian.md#file-contents) (L1b) | `radar_cartesian` | **Required:** one of [`backscatter_amplitude`](product_variables.md#backscatter_amplitude) or [`backscatter_power`](product_variables.md#backscatter_power) |
| [Relative roughness images](../annex/relative_roughness_images.md#file-contents) (L2a) | `relative_roughness` | **Required:** [`relative_roughness`](product_variables.md#relative_roughness)<br>**Optional:** [`number_of_observations`](product_variables.md#number_of_observations) |
| [Relative roughness image mosaics](../annex/relative_roughness_mosaics.md#file-contents) (L2a) | `relative_roughness_mosaic` | **Required:** [`relative_roughness`](product_variables.md#relative_roughness), [`start_time_of_observations`](product_variables.md#start_time_of_observations)<br>**Optional:** [`number_of_observations`](product_variables.md#number_of_observations), [`scan_sectors`](product_variables.md#scan_sectors) |
| [Near-surface current maps](../annex/current_maps.md#file-contents) (L2a) | `currents` | **Required:** [`eastward_sea_water_velocity`](product_variables.md#eastward_sea_water_velocity), [`northward_sea_water_velocity`](product_variables.md#northward_sea_water_velocity)<br>**Recommended:** [`mean_wavenumber`](product_variables.md#mean_wavenumber)<br>**Optional:** [`eastward_sea_water_velocity_standard_error`](product_variables.md#eastward_sea_water_velocity_standard_error), [`northward_sea_water_velocity_standard_error`](product_variables.md#northward_sea_water_velocity_standard_error), [`number_of_fitted_spectral_points`](product_variables.md#number_of_fitted_spectral_points), [`signal_to_noise_ratio`](product_variables.md#signal_to_noise_ratio) |
| [Near-surface current profile maps](../annex/current_profile_maps.md#file-contents) (L2a) | `currents_profile` | **Required:** [`wavenumber_bin`](product_variables.md#wavenumber_bin), [`wavenumber_bin_bounds`](product_variables.md#wavenumber_bin_bounds), [`eastward_sea_water_velocity`](product_variables.md#eastward_sea_water_velocity), [`northward_sea_water_velocity`](product_variables.md#northward_sea_water_velocity)<br>**Recommended:** [`mean_wavenumber`](product_variables.md#mean_wavenumber)<br>**Optional:** [`eastward_sea_water_velocity_standard_error`](product_variables.md#eastward_sea_water_velocity_standard_error), [`northward_sea_water_velocity_standard_error`](product_variables.md#northward_sea_water_velocity_standard_error), [`number_of_fitted_spectral_points`](product_variables.md#number_of_fitted_spectral_points), [`signal_to_noise_ratio`](product_variables.md#signal_to_noise_ratio) |
| [Bathymetric maps](../annex/depth_maps.md#file-contents) (L2a) | `bathymetry` | **Required:** [`sea_floor_depth_below_sea_surface`](product_variables.md#sea_floor_depth_below_sea_surface)<br>**Recommended:** [`mean_wavenumber`](product_variables.md#mean_wavenumber)<br>**Optional:** [`sea_floor_depth_below_sea_surface_standard_error`](product_variables.md#sea_floor_depth_below_sea_surface_standard_error), [`number_of_fitted_spectral_points`](product_variables.md#number_of_fitted_spectral_points) |
| [Sea ice drift maps](../annex/sea_ice_drift.md#file-contents) (L2a) | `sea_ice_drift` | **Required:** [`eastward_sea_ice_velocity`](product_variables.md#eastward_sea_ice_velocity), [`northward_sea_ice_velocity`](product_variables.md#northward_sea_ice_velocity)<br>**Optional:** [`correlation_coefficient`](product_variables.md#correlation_coefficient), [`eastward_sea_ice_velocity_backward`](product_variables.md#eastward_sea_ice_velocity_backward), [`northward_sea_ice_velocity_backward`](product_variables.md#northward_sea_ice_velocity_backward), [`correlation_coefficient_backward`](product_variables.md#correlation_coefficient_backward) |
{: .product-type-table }

Of `backscatter_amplitude` and `backscatter_power`, a Cartesian image sequence holds exactly one; it takes the form of an [image cube with a moving origin](#image-cube-with-moving-origin).
In current profile maps, all data variables, `measurement_quality` included, have the additional dimension `wavenumber_bin`, one layer per wavenumber band.
Relative roughness images and mosaics are stored on the local grid; the maps on either grid.
Relative roughness image mosaics are defined for moving platforms only.

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
[cf-bounds]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#cell-boundaries
