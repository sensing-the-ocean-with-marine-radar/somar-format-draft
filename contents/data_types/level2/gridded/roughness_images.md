---
title: Roughness images
layout: default
parent: Gridded data
nav_order: 1
---

# Roughness images

Roughness images provide temporally averaged sea surface roughness, derived from Level 1b Cartesian backscatter intensity images averaged over a short time window (typically tens of seconds) to reduce speckle noise while still resolving the length scales relevant to short wind waves.
Because the underlying platform continues to move during this averaging window, and because the local grid orientation and extent may change from one averaging window to the next, each averaging window is mapped onto its own time-bounded local Cartesian grid (see [Introduction](../../../introduction/index.md)).
All time-bounded grids belonging to one file (typically covering one hour of a platform trajectory) are stored as sibling NetCDF groups, one group per averaging window, named `time_<YYYYMMDDHHMMSS>` after the start time of that window.
Within each group, `mean_sea_surface_roughness` gives the temporally averaged, still uncalibrated and dimensionless (`units = "1"`), radar backscatter intensity, with `number_of_observations` as an ancillary variable recording how many Level 1b images contributed to each grid cell.
Each group carries both a local, radar-centric projection (`crs`), consistent with the Level 1b grid definition, and, for convenience, the corresponding UTM projection (`crs_utm`), together with along-axis coordinate variables in both systems (`x`/`y` and `x_utm`/`y_utm`).

## Minimal example
```
netcdf or_2025-01-15-11_sea_surface_roughness {

// global attributes:
                :instrument = "Helmholtz-Zentrum Hereon coherent-on-receive marine X-band radar" ;
                :platform = "R/V Ocean Research" ;
                :title = "Marine X-band radar temporally averaged sea surface roughness images from R/V Ocean Research" ;
                :comment = "The sea surface roughness images are temporal averages of approximately 19 consecutive radar backscatter intensity images, corresponding to 30.0 s. The images are corrected for ship motion and for the rapid radar backscatter intensity decay with range. Segments of the radar field of view that are obstructed by platform superstructures are disregarded." ;
                :contact = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13 SOMaR-0.3-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :featureType = "trajectory" ;

group: time_20250115110031 {
  dimensions:
        y = 1988 ;
        x = 1898 ;
  variables:
        char trajectory ;
                trajectory:cf_role = "trajectory_id" ;
                trajectory:long_name = "Mean sea surface roughness measurements along R/V Ocean Research trajectory" ;
        char crs ;
                crs:grid_mapping_name = "transverse_mercator" ;
                crs:longitude_of_projection_origin = 145.868167860183 ;
                crs:latitude_of_projection_origin = 14.9952749946079 ;
                crs:scale_factor_at_central_meridian = 1. ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:projected_crs_name = "WGS 84 / origin of coordinate sytem is radar location at measurement start time" ;
        char crs_utm ;
                crs_utm:grid_mapping_name = "transverse_mercator" ;
                crs_utm:longitude_of_projection_origin = 147. ;
                crs_utm:latitude_of_projection_origin = 0. ;
                crs_utm:false_easting = 500000. ;
                crs_utm:false_northing = 0. ;
                crs_utm:scale_factor_at_central_meridian = 0.9996 ;
                crs_utm:authority_string = "EPSG:32655" ;
                crs_utm:projected_crs_name = "WGS 84 / UTM zone 55N" ;
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "days since 2025-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T11:00:31.417000Z" ;
        double x(x) ;
                x:long_name = "distance from radar along grid x-axis at measurement start time" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "distance from radar along grid y-axis at measurement start time" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        float mean_sea_surface_roughness(y, x) ;
                mean_sea_surface_roughness:long_name = "temporally averaged radar backscatter intensity in uncalibrated analog-to-digital converter units" ;
                mean_sea_surface_roughness:units = "1" ;
                mean_sea_surface_roughness:grid_mapping = "crs: x y crs_utm: x_utm y_utm" ;
                mean_sea_surface_roughness:ancillary_variables = "number_of_observations" ;
        int number_of_observations(y, x) ;
                number_of_observations:standard_name = "number_of_observations" ;
                number_of_observations:long_name = "number of measurements from which the radar backscatter intensity averages have been derived" ;
                number_of_observations:units = "1" ;
                number_of_observations:grid_mapping = "crs: x y crs_utm: x_utm y_utm" ;
        double x_utm(x) ;
                x_utm:long_name = "easting along grid x-axis" ;
                x_utm:standard_name = "projection_x_coordinate" ;
                x_utm:units = "m" ;
        double y_utm(y) ;
                y_utm:long_name = "northing along grid y-axis" ;
                y_utm:standard_name = "projection_y_coordinate" ;
                y_utm:units = "m" ;
  } // group time_20250115110031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per averaging window ...
}
```
