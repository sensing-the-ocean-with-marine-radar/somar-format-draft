---
title: Gridded products
layout: default
parent: "Level 2: Geophysical quantities"
grand_parent: SOMaR product types
nav_order: 1
---

# Gridded products

Gridded products give one value set for each cell of a grid that resolves the area covered by a measurement: each analysis window, or each pixel of an image, keeps its own position.
They comprise the roughness images and mosaics, which average Level 1b images on a local Cartesian grid, and the maps of near-surface currents, current profiles, bathymetry, and sea ice drift, which are retrieved within analysis windows.
The products of this kind, and the variables that each of them holds, are listed under [Product types](#product-types).
Their structure depends on whether the platform moves: a file from a moving platform, which must set the global attribute [`platform_is_mobile`](../../metadata_attributes/optional_global.md) to `"true"`, stores each measurement on its own [time-bounded grid](#time-bounded-grids), and a file from a fixed platform stores all measurements on a [single grid](#fixed-platform).

## Time-bounded grids

The cells of one measurement form a grid over the area it covers: the radar footprint for a map or a roughness image, and for a mosaic an area along the platform track.
With a moving platform, this area changes from one measurement to the next, so that a file holds a sequence of grids rather than one grid sampled repeatedly.
All grids of a file from a moving platform are therefore stored as sibling NetCDF groups, one group per measurement period, or per averaging window for roughness images, named `time_<YYYYMMDDHHMMSS>` (UTC) after its start time.
Within each group, the scalar variable `time` gives that start time, and the variables are stored on a two-dimensional grid, either the geographic grid or the local grid described below.
Cells without a value hold the `_FillValue`: the cells in the corners of the grid, since the radar footprint is circular, and the cells of analysis windows without a result or inside an [obstructed sector](../../metadata_attributes/radar_parameters.md#obstructed-sectors).

### Geographic grid

Maps whose analysis windows lie on an Earth-fixed lattice are stored on a grid with the dimensions `(latitude, longitude)`.
The coordinate variables `latitude` and `longitude` give the centers of the analysis windows; they are one-dimensional because the windows lie on a lattice in longitude and latitude (see [Georeferencing](../../georeferencing/index.md#positions-of-analysis-windows)).
On this grid, `crs` is recommended rather than required: without it, `latitude` and `longitude` refer to WGS 84.

### Local grid

Roughness images and mosaics, and maps whose analysis windows lie on a local grid around the radar, are stored on the local grid of the measurement: `x` and `y` give the distance in meters east and north of the radar antenna at the start of the measurement, and `crs` describes the local azimuthal equidistant projection centered on that position (see [Time-bounded local grids](../../georeferencing/index.md#time-bounded-local-grids)).
In this form, `crs` is required, since its projection origin locates the grid.
A roughness image mosaic is stored on a single, larger local grid per measurement period, which extends along the platform track beyond the footprint of a single roughness image.
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
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
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

## Fixed platform

From a fixed platform, every measurement covers the same area on the same grid, and all measurements of a file are stored on a single grid in the root group, without `time_<YYYYMMDDHHMMSS>` groups.
The dimension `time` then precedes the dimensions of the grid, `(time, latitude, longitude)` on the geographic grid or `(time, y, x)` on the local grid, and the variable `time` gives the start time of each measurement.
A single `crs` describes the grid; on the local grid, its projection origin is the position of the radar antenna.
A file therefore holds measurements on one grid only, and a change of grid, such as a new analysis window spacing, starts a new file.
Roughness image mosaics are not defined for a fixed platform, since a radar that does not move covers no more than the footprint of a roughness image.
A near-surface current map from a fixed platform holds, for example:

```
dimensions:
        time = 15 ;
        latitude = 17 ;
        longitude = 17 ;
variables:
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of current measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
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

Each `time_<YYYYMMDDHHMMSS>` group, or the root group of a file from a fixed platform, holds the following variables, in addition to those of its product (see [Product types](#product-types)).
The data variables of a product are defined under [Level 2 variables](../../metadata_attributes/level2_variables.md), where `(…)` stands for the dimensions of the grid, preceded by `time` from a fixed platform.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required on the local grid, recommended on the geographic grid. Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). Without it, `latitude` and `longitude` refer to WGS 84. |
| `time`<br><small>[CF][cf-names]</small> | double, or double `(time)` from a fixed platform; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of the measurement period, or of the averaging window of a roughness image. |
| `x`<br><small>[CF][cf-names]</small> | double `(x)`; `m` | Required on the local grid. Distance east of the radar antenna at the start of the measurement. |
| `y`<br><small>[CF][cf-names]</small> | double `(y)`; `m` | Required on the local grid. Distance north of the radar antenna at the start of the measurement. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(longitude)` on the geographic grid, `(y, x)` on the local grid; `degrees_east` | Required for maps; omitted for roughness images and mosaics. Longitude of the centers of the analysis windows. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(latitude)` on the geographic grid, `(y, x)` on the local grid; `degrees_north` | Required for maps; omitted for roughness images and mosaics. Latitude of the centers of the analysis windows. |
| `radar_longitude`<br><small>SOMaR</small> | double; `degrees_east` | Optional, for maps. Longitude of the radar antenna at the start of the measurement period, or of the fixed radar antenna (see [Georeferencing](../../georeferencing/index.md#radar-position)). |
| `radar_latitude`<br><small>SOMaR</small> | double; `degrees_north` | Optional, for maps. Latitude of the radar antenna at the start of the measurement period, or of the fixed radar antenna. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(…)`; bit flags | Recommended. Quality flag. 0 is good; each bit that is set marks a failed check (see [Quality flags](index.md#quality-flags)). |
{: .variable-table }

On the local grid, the data variables of a map carry `coordinates = "longitude latitude"`; on either grid, they carry `grid_mapping = "crs"` if the group holds a `crs`.
The processing parameters of gridded products are recorded in global attributes (see [Processing parameters](index.md#processing-parameters)).

## Product types

The following products are gridded products.
For each, the table lists the data variables that it requires, recommends, or allows, in addition to the variables above; they are defined under [Level 2 variables](../../metadata_attributes/level2_variables.md).

| Product | `product_type` | Variables |
|---|---|---|
| [Roughness images](roughness_images.md) (L2a) | `sea_surface_roughness` | **Required:** `sea_surface_roughness`<br>**Optional:** `number_of_observations` |
| [Roughness image mosaics](roughness_mosaics.md) (L2a) | `sea_surface_roughness_mosaic` | **Required:** `sea_surface_roughness`, `start_time_of_observations`<br>**Optional:** `number_of_observations`, `scan_sectors` |
| [Near-surface current maps](current_maps.md) (L2a) | `currents` | **Required:** `eastward_sea_water_velocity`, `northward_sea_water_velocity`<br>**Recommended:** `mean_wavenumber`<br>**Optional:** `eastward_sea_water_velocity_standard_error`, `northward_sea_water_velocity_standard_error`, `number_of_wave_coordinates`, `signal_to_noise_ratio` |
| [Near-surface current profile maps](current_profile_maps.md) (L2a) | `currents_profile` | **Required:** `wavenumber_bin`, `wavenumber_bin_bounds`, `eastward_sea_water_velocity`, `northward_sea_water_velocity`<br>**Recommended:** `mean_wavenumber`<br>**Optional:** `eastward_sea_water_velocity_standard_error`, `northward_sea_water_velocity_standard_error`, `number_of_wave_coordinates`, `signal_to_noise_ratio` |
| [Bathymetric maps](depth_maps.md) (L2a) | `bathymetry` | **Required:** `sea_floor_depth_below_sea_surface`<br>**Recommended:** `mean_wavenumber`<br>**Optional:** `sea_floor_depth_below_sea_surface_standard_error`, `number_of_wave_coordinates` |
| [Sea ice drift maps](sea_ice_drift.md) (L2a) | `sea_ice_drift` | **Required:** `eastward_sea_ice_velocity`, `northward_sea_ice_velocity`<br>**Optional:** `correlation_coefficient`, `eastward_sea_ice_velocity_backward`, `northward_sea_ice_velocity_backward`, `correlation_coefficient_backward` |
{: .product-type-table }

In current profile maps, all data variables, `measurement_quality` included, have the additional dimension `wavenumber_bin`, one layer per wavenumber band.
Roughness images and mosaics are stored on the local grid; the maps on either grid.
Roughness image mosaics are defined for moving platforms only.

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
