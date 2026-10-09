---
title: Roughness images (L2a)
layout: default
parent: Level 2 data
nav_order: 1
---

# L2a: Roughness images

Roughness images provide temporally averaged sea surface roughness, derived from Level 1b Cartesian backscatter intensity images averaged over a short time window (typically tens of seconds) to reduce speckle noise while still resolving the length scales relevant to short wind waves.
Because the underlying platform continues to move during this averaging window, and because the local grid origin and extent may change from one averaging window to the next, each averaging window is mapped onto its own time-bounded local Cartesian grid (see [Introduction](../../introduction/index.md)).
All time-bounded grids belonging to one file (typically covering one hour of a platform trajectory) are stored as sibling NetCDF groups, one group per averaging window, named `time_<YYYYMMDDHHMMSS>` after the start time of that window.
Within each group, `mean_sea_surface_roughness` gives the temporally averaged, still uncalibrated and dimensionless (`units = "1"`), radar backscatter intensity, with `number_of_observations` as an ancillary variable recording how many Level 1b images contributed to each grid cell.
Each group carries its own local, radar-centric projection (`crs`), consistent with the Level 1b grid definition, together with the coordinate variables `x` and `y`, which give the distance in meters east and north of the radar (see [Georeferencing](../../metadata_attributes/georeferencing.md#time-bounded-local-grids)).

## Minimal example
```
netcdf or_2025-01-15-11_sea_surface_roughness {

// global attributes:
                :instrument = "Helmholtz-Zentrum Hereon coherent-on-receive marine X-band radar" ;
                :platform = "R/V Ocean Research" ;
                :title = "Marine X-band radar temporally averaged sea surface roughness images from R/V Ocean Research" ;
                :summary = "The sea surface roughness images are temporal averages of approximately 19 consecutive radar backscatter intensity images, corresponding to 30.0 s. The images are corrected for ship motion and for the rapid radar backscatter intensity decay with range. Segments of the radar field of view that are obstructed by platform superstructures are disregarded." ;
                :creator_email = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :featureType = "trajectory" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :history = "20250115T120500Z: File creation time" ;
                :processing_level = "L2a" ;

group: time_20250115110031 {
  dimensions:
        y = 1988 ;
        x = 1898 ;
  variables:
        char trajectory ;
                trajectory:cf_role = "trajectory_id" ;
                trajectory:long_name = "Mean sea surface roughness measurements along R/V Ocean Research trajectory" ;
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 145.868167860183 ;
                crs:latitude_of_projection_origin = 14.9952749946079 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:projected_crs_name = "WGS 84 / origin of coordinate system is radar location at measurement start time" ;
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
        float mean_sea_surface_roughness(y, x) ;
                mean_sea_surface_roughness:long_name = "temporally averaged radar backscatter intensity in uncalibrated analog-to-digital converter units" ;
                mean_sea_surface_roughness:units = "1" ;
                mean_sea_surface_roughness:grid_mapping = "crs" ;
                mean_sea_surface_roughness:ancillary_variables = "number_of_observations" ;
        int number_of_observations(y, x) ;
                number_of_observations:standard_name = "number_of_observations" ;
                number_of_observations:long_name = "number of measurements from which the radar backscatter intensity averages have been derived" ;
                number_of_observations:units = "1" ;
                number_of_observations:grid_mapping = "crs" ;
  } // group time_20250115110031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per averaging window ...
}
```
