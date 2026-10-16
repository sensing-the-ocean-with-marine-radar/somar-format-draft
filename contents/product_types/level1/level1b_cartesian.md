---
title: Cartesian image sequences (L1b)
layout: default
parent: Level 1 products
grand_parent: SOMaR product types
nav_order: 3
---

# L1b: Cartesian image sequences

Level 1b Cartesian images (`radar_cartesian`, a three-dimensional cube in Cartesian coordinates) are radar images, one per antenna revolution, that have been mapped from the polar coordinates of the sensor onto a regular Cartesian `x`/`y` grid, while otherwise remaining as close as possible to the underlying Level 1a data.
The grid is defined in a local, radar-centric coordinate system whose origin is given by the `longitude`/`latitude` of the radar antenna at the start of each revolution; since the grid origin moves with the platform from one image to the next, each image has its own origin, as in the [time-bounded local grids](../../georeferencing/index.md#time-bounded-local-grids), but all images share one `x`/`y` grid and are stored as a single cube.
Grid cells that fall outside the valid field of view, for example those obstructed by platform superstructure, hold the `_FillValue`; the obstructed sectors themselves may be recorded in the `radar_parameters` group (see [Obstructed sectors](../../metadata_attributes/radar_parameters.md#obstructed-sectors)).
As at Level 1a, values are stored in uncalibrated analog-to-digital converter units and are therefore dimensionless (`units = "1"`); no radiometric calibration or temporal averaging is applied at this level, and the `comment` attribute of the data variable states whether the values are amplitude or power.

## Position and orientation

`x` and `y` are distances in meters east and north of the grid origin.
The images are north-oriented: the platform heading and the azimuth and range corrections have been applied in the mapping, so no `heading` is stored. This is the main difference from the polar form, which is stored as recorded.

The grid origin is the position of the radar antenna at the start of each revolution, i.e. the recorded position after application of the [position offsets](../../georeferencing/index.md#position-offset), and is given by `longitude` and `latitude`.
For a moving platform, they have the dimension `time`, with one value per image; for a fixed platform, they are scalar.

| Variable | Values | Description |
|---|---|---|
| `time`<br><small>[CF](https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html)</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each revolution. |
| `x`<br><small>SOMaR</small> | double `(x)`; `m` | Required. Distance east of the grid origin. |
| `y`<br><small>SOMaR</small> | double `(y)`; `m` | Required. Distance north of the grid origin. |
| `longitude`<br><small>SOMaR</small> | double `(time)` or scalar; `degrees_east` | Required. Longitude (WGS 84) of the grid origin. |
| `latitude`<br><small>SOMaR</small> | double `(time)` or scalar; `degrees_north` | Required. Latitude (WGS 84) of the grid origin. |
| data variable, e.g. `radar_backscatter_intensity`<br><small>SOMaR</small> | float `(time, y, x)`; `1` or `dB` | Required. Uncalibrated amplitude or power, with `_FillValue` and `comment`. |
{: .variable-table }

The file has no `crs` variable and the data variable no `grid_mapping` attribute, since a single coordinate reference system variable can describe only one grid origin, whereas the origin here changes from image to image (see [Georeferencing](../../georeferencing/index.md#time-bounded-local-grids)).
For the same reason, `x` and `y` carry no `standard_name`: CF defines `projection_x_coordinate` and `projection_y_coordinate` in relation to a grid mapping.

{: .open_issue }
Only backscatter amplitude or power is specified. Variables for the data of coherent radars, such as phase or radial Doppler velocity, are not yet defined (see [Level 1a](level1a.md#coherent-data)).

## Minimal example

A radar on a moving platform.

```
netcdf or_2025-01-15-11-00_radar_cartesian {
dimensions:
        time = 41 ;
        y = 1980 ;
        x = 1980 ;
variables:
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude(time) ;
                longitude:long_name = "longitude" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(time) ;
                latitude:long_name = "latitude" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double x(x) ;
                x:long_name = "distance from radar along grid x-axis at measurement start time for each image" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "distance from radar along grid y-axis at measurement start time for each image" ;
                y:units = "m" ;
        float radar_backscatter_intensity(time, y, x) ;
                radar_backscatter_intensity:long_name = "radar backscatter intensity in uncalibrated analog-to-digital converter units" ;
                radar_backscatter_intensity:units = "1" ;
                radar_backscatter_intensity:_FillValue = NaNf ;
                radar_backscatter_intensity:comment = "backscatter power (I^2 + Q^2) in uncalibrated analog-to-digital units, mapped from polar coordinates by bilinear interpolation" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 14.99584 ;
                :geospatial_lat_min = 14.99466 ;
                :geospatial_lon_max = 145.86905 ;
                :geospatial_lon_min = 145.86733 ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :product_type = "radar_cartesian" ;
                :time_coverage_end = "2025-01-15T11:00:59Z" ;
                :time_coverage_start = "2025-01-15T11:00:00Z" ;
                :title = "Marine X-band radar Cartesian images from R/V Ocean Research" ;
}
```

For a fixed platform, `longitude` and `latitude` are scalar.
