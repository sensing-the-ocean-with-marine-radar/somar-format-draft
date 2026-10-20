---
title: Roughness images (L2a)
layout: default
parent: Usage examples
grand_parent: SOMaR product types
nav_order: 1
---

# L2a: Roughness images

Roughness images (`sea_surface_roughness`) provide temporally averaged sea surface roughness, derived from Level 1b Cartesian backscatter images averaged over a short time window (typically tens of seconds) to reduce speckle noise.
Because the underlying platform continues to move during this averaging window, and because the local grid origin and extent may change from one averaging window to the next, each averaging window is mapped onto its own time-bounded local Cartesian grid (see [Time-bounded local grids](../../georeferencing/index.md#time-bounded-local-grids)).
All time-bounded grids belonging to one file (typically covering one hour of a platform trajectory) are stored as sibling NetCDF groups, one group per averaging window, named `time_<YYYYMMDDHHMMSS>` after the start time of that window.
Within each group, `sea_surface_roughness` gives the temporally averaged, still uncalibrated and dimensionless (`units = "1"` or `"dB"`), radar backscatter power, with `number_of_observations` as an ancillary variable recording how many Level 1b images contributed to each grid cell.
Each group carries its own local, radar-centric projection (`crs`), consistent with the Level 1b grid definition, together with the coordinate variables `x` and `y`, which give the distance in meters east and north of the radar (see [Georeferencing](../../georeferencing/index.md#time-bounded-local-grids)).

## Variables

Each `time_<YYYYMMDDHHMMSS>` group holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required. Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of the averaging window. |
| `x`<br><small>[CF][cf-names]</small> | double `(x)`; `m` | Required. Distance east of the radar antenna at the start of the averaging window. |
| `y`<br><small>[CF][cf-names]</small> | double `(y)`; `m` | Required. Distance north of the radar antenna at the start of the averaging window. |
| `sea_surface_roughness`<br><small>SOMaR</small> | float `(y, x)`; `1` or `dB` | Required. Time mean of the radar backscatter power over the window, in uncalibrated analog-to-digital converter units. Level 1b amplitude (`backscatter_amplitude`) is squared, and values in `dB` are converted to linear units, before averaging, and the mean is stored in linear (`1`) or logarithmic (`dB`) units. If the signal cannot be linearized, such as a log-compressed video signal, the mean is taken over the stored Level 1b values instead, the units are `1`, and the `comment` must say so. Carries `cell_methods = "time: mean"`, or `"time: mean (comment: computed on linear power)"` when the units are `dB`, and `coordinates = "time"`. The averaging window of each grid cell starts at `time` and lasts at most `averaging_duration`; it may be shorter for some cells, as recorded by `number_of_observations`. |
| `number_of_observations`<br><small>[CF][cf-names]</small> | int `(y, x)`; `1` | Optional. Number of Level 1b images that contributed to each grid cell. |
{: .variable-table }

The nominal length of the averaging window is recorded in the global attribute [`averaging_duration`](index.md#processing-parameters).

## Minimal example
```
netcdf or_2025-01-15-11_sea_surface_roughness {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :averaging_duration = 30. ;
                :geospatial_lat_max = 14.99528 ;
                :geospatial_lat_min = 14.95348 ;
                :geospatial_lon_max = 145.94251 ;
                :geospatial_lon_min = 145.86816 ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :product_type = "sea_surface_roughness" ;
                :time_coverage_end = "2025-01-15T11:59:59Z" ;
                :time_coverage_start = "2025-01-15T11:00:00Z" ;
                :title = "Marine X-band radar sea surface roughness images from R/V Ocean Research" ;

group: time_20250115110031 {
  dimensions:
        y = 1988 ;
        x = 1898 ;
  variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 145.868167860183 ;
                crs:latitude_of_projection_origin = 14.9952749946079 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T11:00:31.417000Z" ;
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
                sea_surface_roughness:ancillary_variables = "number_of_observations" ;
        int number_of_observations(y, x) ;
                number_of_observations:standard_name = "number_of_observations" ;
                number_of_observations:long_name = "number of measurements from which the radar backscatter power averages have been derived" ;
                number_of_observations:units = "1" ;
                number_of_observations:grid_mapping = "crs" ;
  } // group time_20250115110031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per averaging window ...
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
