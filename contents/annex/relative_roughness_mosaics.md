---
title: Relative roughness image mosaics (L2a)
layout: default
parent: "Annex: Example products"
nav_order: 6
---

# L2a: Relative roughness image mosaics

{: .informative }
> This page is informative. The product type `relative_roughness_mosaic` is one of the [gridded products](../product_types/gridded.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md). The [file contents](#file-contents) summarize these definitions for this product; where they differ, the definitions apply.

Relative roughness image mosaics (`relative_roughness_mosaic`) provide temporally averaged relative sea surface roughness on a single, larger local Cartesian grid per measurement period (typically ten minutes), assembled from a sequence of Level 1b Cartesian backscatter images acquired while the platform moves along its trajectory.
In contrast to [relative roughness images](relative_roughness_images.md), where all pixels of a grid share one short averaging window, each pixel of a mosaic is a temporal average over a short time window (typically tens of seconds), but the start of that averaging window differs from pixel to pixel.
The averaging start time is determined by data availability and hence by the platform track: a location is averaged while it lies within the part of the radar field of view that is suitable for the mosaic, and different locations are reached at different times as the platform passes by.
The mosaic therefore extends along the platform track beyond the footprint of a single relative roughness image, and the pixel-wise averaging start time is provided in [`start_time_of_observations`](../product_types/product_variables.md#start_time_of_observations), in seconds after the group's [`time`](../product_types/gridded.md#variables-time).
Like the relative roughness images, all mosaics of one file, typically covering one hour of a platform trajectory, are stored as sibling groups, one per measurement period, each on its own local grid.
Within each group, [`relative_roughness`](../product_types/product_variables.md#relative_roughness) gives the averaged, still uncalibrated radar backscatter power, with three ancillary variables: [`number_of_observations`](../product_types/product_variables.md#number_of_observations) records how many Level 1b images contributed to each grid cell, `start_time_of_observations` when the averaging of each grid cell started, and [`scan_sectors`](../product_types/product_variables.md#scan_sectors) which part of the radar scan, relative to the target area, the observations of each grid cell belong to.

## File contents

**Layout.** The file holds one [time-bounded grid](../product_types/gridded.md#time-bounded-grids) per measurement period, each in a `time_<YYYYMMDDHHMMSS>` group, on the [local grid](../product_types/gridded.md#local-grid) `(y, x)`.

A file of this product holds the following items; each links to its definition, and the condition, where one is given, states when the tier applies.

| Item | Tier | Condition |
|---|---|---|
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`product_type`](../metadata_attributes/mandatory_global.md#product_type) `= "relative_roughness_mosaic"` | Required | |
| [`platform_is_mobile`](../metadata_attributes/optional_global.md#platform_is_mobile) `= "true"` | Required | |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| [`averaging_duration`](../metadata_attributes/processing_parameters.md#averaging_duration), [`measurement_duration`](../metadata_attributes/processing_parameters.md#measurement_duration) | Recommended | |
| **Variables of each grid** | | |
| [`time`](../product_types/gridded.md#variables-time) | Required | |
| [`time_iso_8601`](../metadata_attributes/variable_attributes.md#time_iso_8601) on `time` | Optional | |
| [`time_bounds`](../product_types/gridded.md#time_bounds) | Optional | |
| [`x`](../product_types/gridded.md#variables-x), [`y`](../product_types/gridded.md#variables-y), [`crs`](../product_types/gridded.md#variables-crs) | Required | |
| [`relative_roughness`](../product_types/product_variables.md#relative_roughness) | Required | |
| [`cell_methods`](../metadata_attributes/variable_attributes.md#cell_methods) `= "time: mean"`, [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity), and [`coordinates`](../metadata_attributes/variable_attributes.md#coordinates) `= "time"` on `relative_roughness` | Required | |
| [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) `= "crs"` on the data variables | Required | |
| [`start_time_of_observations`](../product_types/product_variables.md#start_time_of_observations) | Required | |
| [`number_of_observations`](../product_types/product_variables.md#number_of_observations), [`scan_sectors`](../product_types/product_variables.md#scan_sectors) | Optional | |
{: .contents-table }

## Example

```
netcdf or_2025-01-15-11_relative_roughness_mosaic {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 14.98322 ; // recommended
                :geospatial_lat_min = 14.9549 ; // recommended
                :geospatial_lon_max = 145.93682 ; // recommended
                :geospatial_lon_min = 145.88642 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ; // highly recommended
                :platform_is_mobile = "true" ;
                :product_type = "relative_roughness_mosaic" ;
                :summary = "Sea surface roughness mosaics from a marine X-band radar on board R/V Ocean Research, assembled from 30 s averages of Cartesian backscatter images over 10 min measurement periods." ; // highly recommended
                :time_coverage_end = "2025-01-15T12:00:01.357666Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:10:01.357666Z" ; // recommended
                :title = "Marine X-band radar sea surface relative roughness image mosaics from R/V Ocean Research" ; // highly recommended
                :averaging_duration = 30. ; // recommended
                :measurement_duration = 600. ; // recommended

group: time_20250115111001 {
  dimensions:
        y = 1000 ;
        x = 1500 ;
  variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 145.886424800978 ;
                crs:latitude_of_projection_origin = 14.9832181178649 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T11:10:01.357666Z" ; // optional
        double x(x) ;
                x:long_name = "eastward distance from radar position at measurement start time" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from radar position at measurement start time" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        float relative_roughness(y, x) ;
                relative_roughness:long_name = "temporally averaged radar backscatter power in uncalibrated analog-to-digital converter units" ;
                relative_roughness:units = "1" ;
                relative_roughness:grid_mapping = "crs" ;
                relative_roughness:coordinates = "time" ;
                relative_roughness:cell_methods = "time: mean" ;
                relative_roughness:averaged_quantity = "power" ;
                relative_roughness:ancillary_variables = "number_of_observations start_time_of_observations scan_sectors" ;
        int number_of_observations(y, x) ; // optional
                number_of_observations:standard_name = "number_of_observations" ;
                number_of_observations:long_name = "number of measurements from which the radar backscatter power averages have been derived" ;
                number_of_observations:units = "1" ;
                number_of_observations:grid_mapping = "crs" ;
        float start_time_of_observations(y, x) ;
                start_time_of_observations:long_name = "start time of the radar backscatter power averages in seconds after the group time" ;
                start_time_of_observations:units = "s" ;
                start_time_of_observations:grid_mapping = "crs" ;
        byte scan_sectors(y, x) ; // optional
                scan_sectors:long_name = "part of the radar scan relative to the target area" ;
                scan_sectors:flag_values = 0b, 1b, 2b ;
                scan_sectors:flag_meanings = "preceding_target_area inside_target_area trailing_target_area" ;
                scan_sectors:_FillValue = -1b ;
                scan_sectors:grid_mapping = "crs" ;
  } // group time_20250115111001

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per mosaic (here, every 10 minutes from 11:10 to 11:50) ...
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2025-01-15-11_relative_roughness_mosaic {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :platform_is_mobile = "true" ;
                :product_type = "relative_roughness_mosaic" ;

group: time_20250115111001 {
  dimensions:
        y = 1000 ;
        x = 1500 ;
  variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 145.886424800978 ;
                crs:latitude_of_projection_origin = 14.9832181178649 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double x(x) ;
                x:long_name = "eastward distance from radar position at measurement start time" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from radar position at measurement start time" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        float relative_roughness(y, x) ;
                relative_roughness:long_name = "temporally averaged radar backscatter power in uncalibrated analog-to-digital converter units" ;
                relative_roughness:units = "1" ;
                relative_roughness:grid_mapping = "crs" ;
                relative_roughness:coordinates = "time" ;
                relative_roughness:cell_methods = "time: mean" ;
                relative_roughness:averaged_quantity = "power" ;
                relative_roughness:ancillary_variables = "start_time_of_observations" ;
        float start_time_of_observations(y, x) ;
                start_time_of_observations:long_name = "start time of the radar backscatter power averages in seconds after the group time" ;
                start_time_of_observations:units = "s" ;
                start_time_of_observations:grid_mapping = "crs" ;
  } // group time_20250115111001

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per mosaic (here, every 10 minutes from 11:10 to 11:50) ...
}
```
