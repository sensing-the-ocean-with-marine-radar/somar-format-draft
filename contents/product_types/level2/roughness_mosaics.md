---
title: Roughness image mosaics (L2a)
layout: default
parent: Level 2 products
grand_parent: SOMaR product types
nav_order: 2
---

# L2a: Roughness image mosaics

Roughness image mosaics (`sea_surface_roughness_mosaic`) provide temporally averaged sea surface roughness on a single, larger local Cartesian grid per measurement period (typically ten minutes), assembled from a sequence of Level 1b Cartesian backscatter images acquired while the platform moves along its trajectory.
In contrast to [roughness images](roughness_images.md), where all pixels of a grid share one short averaging window, each pixel of a mosaic is a temporal average over only a few tens of seconds (typically about 19 consecutive images, corresponding to 30 s, the nominal `averaging_duration`), but the start of that averaging window differs from pixel to pixel.
The averaging start time is determined by data availability and hence by the platform track: a location is averaged while it lies within the part of the radar field of view that is suitable for the mosaic, and different locations are reached at different times as the platform passes by.
The mosaic therefore extends along the platform track beyond the footprint of a single roughness image, and the pixel-wise averaging start time is provided in `start_time_of_observations`, in seconds after the group's `time`.
Like the roughness images, all mosaics belonging to one file (typically covering one hour of a platform trajectory) are stored as sibling NetCDF groups, one group per measurement period, named `time_<YYYYMMDDHHMMSS>` after the start time of that period, and each group carries its own time-bounded local Cartesian grid (see [Time-bounded local grids](../../georeferencing/index.md#time-bounded-local-grids)).
Within each group, `sea_surface_roughness` gives the temporally averaged, still uncalibrated and dimensionless (`units = "1"`), radar backscatter power, with three ancillary variables: `number_of_observations` records how many Level 1b images contributed to each grid cell, `start_time_of_observations` records when the averaging of each grid cell started, and `scan_sectors` is a flag variable recording which part of the radar scan relative to the target area (`preceding_target_area`, `inside_target_area`, `trailing_target_area`) the observations of each grid cell belong to.
Each group carries its own local, radar-centric projection (`crs`), consistent with the Level 1b grid definition, together with the coordinate variables `x` and `y`, which give the distance in meters east and north of the radar (see [Georeferencing](../../georeferencing/index.md#time-bounded-local-grids)).

## Variables

Each `time_<YYYYMMDDHHMMSS>` group holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required. Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of the measurement period. |
| `x`<br><small>[CF][cf-names]</small> | double `(x)`; `m` | Required. Distance east of the radar antenna at the start of the measurement period. |
| `y`<br><small>[CF][cf-names]</small> | double `(y)`; `m` | Required. Distance north of the radar antenna at the start of the measurement period. |
| `sea_surface_roughness`<br><small>SOMaR</small> | float `(y, x)`; `1` | Required. Time mean of the radar backscatter power over the averaging window of each grid cell, in linear, uncalibrated analog-to-digital converter units. Level 1b amplitude (`backscatter_amplitude`) is squared, and values in `dB` are converted to linear units, before averaging. If the signal cannot be linearized, such as a log-compressed video signal, the mean is taken over the stored Level 1b values instead, and the `comment` must say so. Carries `cell_methods = "time: mean"` and `coordinates = "time"`. The averaging window of each grid cell starts at `time + start_time_of_observations` and lasts at most `averaging_duration`; it may be shorter for some cells, as recorded by `number_of_observations`. |
| `number_of_observations`<br><small>[CF][cf-names]</small> | int `(y, x)`; `1` | Optional. Number of Level 1b images that contributed to each grid cell. |
| `start_time_of_observations`<br><small>SOMaR</small> | float `(y, x)`; `s` | Required. Start of the averaging for each grid cell, in seconds after `time`. |
| `scan_sectors`<br><small>SOMaR</small> | byte `(y, x)`; `0b`, `1b`, `2b` | Optional. Part of the radar scan, relative to the target area, that the observations of each grid cell belong to: 0 preceding, 1 inside, 2 trailing. |
{: .variable-table }

The nominal length of the averaging window and the length of the measurement period are recorded in the global attributes [`averaging_duration` and `measurement_duration`](index.md#processing-parameters).

## Minimal example
```
netcdf or_2025-01-15-11_sea_surface_roughness_mosaic {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :averaging_duration = 30. ;
                :geospatial_lat_max = 14.98322 ;
                :geospatial_lat_min = 14.95348 ;
                :geospatial_lon_max = 145.94251 ;
                :geospatial_lon_min = 145.88642 ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :measurement_duration = 600. ;
                :product_type = "sea_surface_roughness_mosaic" ;
                :time_coverage_end = "2025-01-15T11:59:59Z" ;
                :time_coverage_start = "2025-01-15T11:00:00Z" ;
                :title = "Marine X-band radar sea surface roughness image mosaics from R/V Ocean Research" ;

group: time_20250115111001 {
  dimensions:
        y = 2182 ;
        x = 2195 ;
  variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 145.886424800978 ;
                crs:latitude_of_projection_origin = 14.9832181178649 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T11:10:01.357666Z" ;
        double x(x) ;
                x:long_name = "eastward distance from radar position at measurement start time" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from radar position at measurement start time" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        float sea_surface_roughness(y, x) ;
                sea_surface_roughness:long_name = "temporally averaged radar backscatter power in uncalibrated analog-to-digital converter units" ;
                sea_surface_roughness:units = "1" ;
                sea_surface_roughness:grid_mapping = "crs" ;
                sea_surface_roughness:coordinates = "time" ;
                sea_surface_roughness:cell_methods = "time: mean" ;
                sea_surface_roughness:ancillary_variables = "number_of_observations start_time_of_observations scan_sectors" ;
        int number_of_observations(y, x) ;
                number_of_observations:standard_name = "number_of_observations" ;
                number_of_observations:long_name = "number of measurements from which the radar backscatter power averages have been derived" ;
                number_of_observations:units = "1" ;
                number_of_observations:grid_mapping = "crs" ;
        float start_time_of_observations(y, x) ;
                start_time_of_observations:long_name = "start time of the radar backscatter power averages in seconds after the group time" ;
                start_time_of_observations:units = "s" ;
                start_time_of_observations:grid_mapping = "crs" ;
        byte scan_sectors(y, x) ;
                scan_sectors:long_name = "part of the radar scan relative to the target area" ;
                scan_sectors:flag_values = 0b, 1b, 2b ;
                scan_sectors:flag_meanings = "preceding_target_area inside_target_area trailing_target_area" ;
                scan_sectors:_FillValue = -1b ;
                scan_sectors:grid_mapping = "crs" ;
  } // group time_20250115111001

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per mosaic (here, every 10 minutes) ...
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
