---
title: Cartesian image sequences (L1b)
layout: default
parent: Level 1 products
nav_order: 3
---

# L1b: Cartesian image sequences

Level 1b Cartesian images (`radar_cartesian`, short `cart3d`, a three-dimensional cube in Cartesian coordinates) are radar images, one per antenna revolution, that have been mapped from the polar coordinates of the sensor onto a regular Cartesian `x`/`y` grid, while otherwise remaining as close as possible to the underlying Level 1a data.
The grid is defined in a local, radar-centric coordinate system whose origin is given by the `longitude`/`latitude` of the radar antenna at the start of each revolution; this is an instance of the time-bounded local grid concept introduced in the [Introduction](../../introduction/index.md), since the grid origin moves with the platform from one image to the next.
Grid cells that fall outside the calibrated field of view, for example those obstructed by platform superstructure, are blanked.
As at Level 1a, values are stored in uncalibrated analog-to-digital converter units and are therefore dimensionless (`units = "1"`); no radiometric calibration or temporal averaging is applied at this level.

## Position and orientation

`x` and `y` are distances in meters east and north of the grid origin.
The images are north-oriented: the platform heading and the azimuth and range corrections have been applied in the mapping, so no `heading` is stored. This is the main difference from the polar form, which is stored as recorded.

The grid origin is the position of the radar antenna at the start of each revolution, i.e. the recorded position after application of the [position offsets](../../metadata_attributes/radar_parameters.md#position-offset), and is given by `longitude` and `latitude`.
For a moving platform, they have the dimension `time`, with one value per image; for a fixed platform, they are scalar.

| Variable | Values | Description |
|---|---|---|
| `longitude`<br><small>SOMaR</small> | double `(time)` or scalar; `degrees_east` | Longitude (WGS 84) of the grid origin. |
| `latitude`<br><small>SOMaR</small> | double `(time)` or scalar; `degrees_north` | Latitude (WGS 84) of the grid origin. |
{: .variable-table }

The file has no `crs` variable and the data variable no `grid_mapping` attribute, since a single coordinate reference system variable can describe only one grid origin, whereas the origin here changes from image to image (see [Georeferencing](../../metadata_attributes/georeferencing.md#time-bounded-local-grids)).
For the same reason, `x` and `y` carry no `standard_name`: CF defines `projection_x_coordinate` and `projection_y_coordinate` in relation to a grid mapping.

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

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :title = "Marine X-band radar backscatter intensity images from R/V Ocean Research" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :creator_email = "famous.scientist@frori.org" ;
                :summary = "The marine X-band radar backscatter intensity images are corrected for ship motion. Segments of the radar field of view that are obstructed by platform superstructures are blanked. The origin of the coordinate system is given by (longitude, latitude), which corresponds to the radar location at the measurement start time for each image." ;
                :history = "20250115T120500Z: File creation time" ;
                :processing_level = "L1b" ;
                :product_type = "radar_cartesian" ;
}
```

For a fixed platform, `longitude` and `latitude` are scalar.
