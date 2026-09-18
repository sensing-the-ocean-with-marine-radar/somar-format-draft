---
title: Roughness image mosaics
layout: default
parent: Gridded data
nav_order: 2
---

# Roughness image mosaics

Roughness image mosaics provide temporally averaged sea surface roughness on a single, larger local Cartesian grid per analysis period (typically ten minutes), assembled from a sequence of Level 1b Cartesian backscatter intensity images acquired while the platform moves along its trajectory.
In contrast to [roughness images](roughness_images.md), where all pixels of a grid share one short averaging window, each pixel of a mosaic is a temporal average over only a few tens of seconds (typically about 19 consecutive images, corresponding to 30 s), but the start of that averaging window differs from pixel to pixel.
The averaging start time is determined by data availability and hence by the platform track: a location is averaged while it lies within the part of the radar field of view that is suitable for the mosaic, and different locations are reached at different times as the platform passes by.
The mosaic therefore covers a much larger area than a single roughness image, and the pixel-wise averaging start time is provided in `start_time_of_observations`, in seconds after the group's `time`.
Like the roughness images, all mosaics belonging to one file (typically covering one hour of a platform trajectory) are stored as sibling NetCDF groups, one group per analysis period, named `time_<YYYYMMDDHHMMSS>` after the start time of that period, and each group carries its own time-bounded local Cartesian grid (see [Introduction](../../../introduction/index.md)).
Within each group, `mean_sea_surface_roughness` gives the temporally averaged, still uncalibrated and dimensionless (`units = "1"`), radar backscatter intensity, with three ancillary variables: `number_of_observations` records how many Level 1b images contributed to each grid cell, `start_time_of_observations` records when the averaging of each grid cell started, and `scan_sectors` is a lookup table flagging which part of the radar scan relative to the target area (`preceding_target_area`, `inside_target_area`, `trailing_target_area`) the observations of each grid cell belong to.
Each group carries both a local, radar-centric projection (`crs`), consistent with the Level 1b grid definition, and, for convenience, the corresponding UTM projection (`crs_utm`), together with along-axis coordinate variables in both systems (`x`/`y` and `x_utm`/`y_utm`).

## Minimal example
```
netcdf or_2025-01-15-11_sea_surface_roughness_mosaic {

// global attributes:
                :instrument = "Helmholtz-Zentrum Hereon coherent-on-receive marine X-band radar" ;
                :platform = "R/V Ocean Research" ;
                :title = "Marine X-band radar temporally averaged sea surface roughness images from R/V Ocean Research" ;
                :comment = "The sea surface roughness images are mosaics composed of approximately 375 consecutive radar backscatter intensity images, corresponding to 600.0 s. The images are corrected for ship motion and for the rapid radar backscatter intensity decay with range. Segments of the radar field of view that are obstructed by platform superstructures are disregarded. Each image pixel is a temporal average of approximately 19 consecutive radar backscatter intensity images. The averaging start time for each pixel varies across the image and is determined by the data availability and hence the ship track." ;
                :contact = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13 SOMaR-0.3-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :featureType = "trajectory" ;

group: time_20250115111001 {
  dimensions:
        y = 2182 ;
        x = 2195 ;
  variables:
        char trajectory ;
                trajectory:cf_role = "trajectory_id" ;
                trajectory:long_name = "Mean sea surface roughness measurements along R/V Ocean Research trajectory" ;
        char crs ;
                crs:grid_mapping_name = "transverse_mercator" ;
                crs:longitude_of_projection_origin = 145.886424800978 ;
                crs:latitude_of_projection_origin = 14.9832181178649 ;
                crs:scale_factor_at_central_meridian = 1. ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:projected_crs_name = "WGS 84 / origin of coordinate system is radar location at measurement start time" ;
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
                time:time_iso_8601 = "2025-01-15T11:10:01.357666Z" ;
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
                mean_sea_surface_roughness:ancillary_variables = "number_of_observations start_time_of_observations scan_sectors" ;
        int number_of_observations(y, x) ;
                number_of_observations:standard_name = "number_of_observations" ;
                number_of_observations:long_name = "number of measurements from which the radar backscatter intensity averages have been derived" ;
                number_of_observations:units = "1" ;
                number_of_observations:grid_mapping = "crs: x y crs_utm: x_utm y_utm" ;
        float start_time_of_observations(y, x) ;
                start_time_of_observations:long_name = "start time of the radar backscatter intensity averages in seconds after the group time" ;
                start_time_of_observations:units = "s" ;
                start_time_of_observations:grid_mapping = "crs: x y crs_utm: x_utm y_utm" ;
        byte scan_sectors(y, x) ;
                scan_sectors:long_name = "scan sector lookup table" ;
                scan_sectors:flag_values = 0b, 1b, 2b ;
                scan_sectors:flag_meanings = "preceding_target_area inside_target_area trailing_target_area" ;
                scan_sectors:_FillValue = -1b ;
                scan_sectors:grid_mapping = "crs: x y crs_utm: x_utm y_utm" ;
        double x_utm(x) ;
                x_utm:long_name = "easting along grid x-axis" ;
                x_utm:standard_name = "projection_x_coordinate" ;
                x_utm:units = "m" ;
        double y_utm(y) ;
                y_utm:long_name = "northing along grid y-axis" ;
                y_utm:standard_name = "projection_y_coordinate" ;
                y_utm:units = "m" ;
  } // group time_20250115111001

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per mosaic (here, every 10 minutes) ...
}
```
