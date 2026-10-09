---
title: Roughness image mosaics (L2a)
layout: default
parent: Level 2 data
nav_order: 2
---

# L2a: Roughness image mosaics

Roughness image mosaics provide temporally averaged sea surface roughness on a single, larger local Cartesian grid per analysis period (typically ten minutes), assembled from a sequence of Level 1b Cartesian backscatter intensity images acquired while the platform moves along its trajectory.
In contrast to [roughness images](roughness_images.md), where all pixels of a grid share one short averaging window, each pixel of a mosaic is a temporal average over only a few tens of seconds (typically about 19 consecutive images, corresponding to 30 s), but the start of that averaging window differs from pixel to pixel.
The averaging start time is determined by data availability and hence by the platform track: a location is averaged while it lies within the part of the radar field of view that is suitable for the mosaic, and different locations are reached at different times as the platform passes by.
The mosaic therefore covers a much larger area than a single roughness image, and the pixel-wise averaging start time is provided in `start_time_of_observations`, in seconds after the group's `time`.
Like the roughness images, all mosaics belonging to one file (typically covering one hour of a platform trajectory) are stored as sibling NetCDF groups, one group per analysis period, named `time_<YYYYMMDDHHMMSS>` after the start time of that period, and each group carries its own time-bounded local Cartesian grid (see [Introduction](../../introduction/index.md)).
Within each group, `mean_sea_surface_roughness` gives the temporally averaged, still uncalibrated and dimensionless (`units = "1"`), radar backscatter intensity, with three ancillary variables: `number_of_observations` records how many Level 1b images contributed to each grid cell, `start_time_of_observations` records when the averaging of each grid cell started, and `scan_sectors` is a lookup table flagging which part of the radar scan relative to the target area (`preceding_target_area`, `inside_target_area`, `trailing_target_area`) the observations of each grid cell belong to.
Each group carries its own local, radar-centric projection (`crs`), consistent with the Level 1b grid definition, together with the coordinate variables `x` and `y`, which give the distance in meters east and north of the radar (see [Georeferencing](../../metadata_attributes/georeferencing.md#time-bounded-local-grids)).

## Minimal example
```
netcdf or_2025-01-15-11_sea_surface_roughness_mosaic {

// global attributes:
                :instrument = "Helmholtz-Zentrum Hereon coherent-on-receive marine X-band radar" ;
                :platform = "R/V Ocean Research" ;
                :title = "Marine X-band radar temporally averaged sea surface roughness images from R/V Ocean Research" ;
                :summary = "The sea surface roughness images are mosaics composed of approximately 375 consecutive radar backscatter intensity images, corresponding to 600.0 s. The images are corrected for ship motion and for the rapid radar backscatter intensity decay with range. Segments of the radar field of view that are obstructed by platform superstructures are disregarded. Each image pixel is a temporal average of approximately 19 consecutive radar backscatter intensity images. The averaging start time for each pixel varies across the image and is determined by the data availability and hence the ship track." ;
                :creator_email = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :history = "20250115T120500Z: File creation time" ;
                :processing_level = "L2a" ;

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
                crs:projected_crs_name = "WGS 84 / origin of coordinate system is radar location at measurement start time" ;
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
        float mean_sea_surface_roughness(y, x) ;
                mean_sea_surface_roughness:long_name = "temporally averaged radar backscatter intensity in uncalibrated analog-to-digital converter units" ;
                mean_sea_surface_roughness:units = "1" ;
                mean_sea_surface_roughness:grid_mapping = "crs" ;
                mean_sea_surface_roughness:ancillary_variables = "number_of_observations start_time_of_observations scan_sectors" ;
        int number_of_observations(y, x) ;
                number_of_observations:standard_name = "number_of_observations" ;
                number_of_observations:long_name = "number of measurements from which the radar backscatter intensity averages have been derived" ;
                number_of_observations:units = "1" ;
                number_of_observations:grid_mapping = "crs" ;
        float start_time_of_observations(y, x) ;
                start_time_of_observations:long_name = "start time of the radar backscatter intensity averages in seconds after the group time" ;
                start_time_of_observations:units = "s" ;
                start_time_of_observations:grid_mapping = "crs" ;
        byte scan_sectors(y, x) ;
                scan_sectors:long_name = "scan sector lookup table" ;
                scan_sectors:flag_values = 0b, 1b, 2b ;
                scan_sectors:flag_meanings = "preceding_target_area inside_target_area trailing_target_area" ;
                scan_sectors:_FillValue = -1b ;
                scan_sectors:grid_mapping = "crs" ;
  } // group time_20250115111001

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per mosaic (here, every 10 minutes) ...
}
```
