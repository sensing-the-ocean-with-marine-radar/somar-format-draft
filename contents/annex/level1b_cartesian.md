---
title: Cartesian image sequences (L1b)
layout: default
parent: "Annex: Example products"
nav_order: 4
---

# L1b: Cartesian image sequences

{: .informative }
> This page is informative. The product type `radar_cartesian` is one of the [gridded products](../product_types/gridded.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md). The [file contents](#file-contents) summarize these definitions for this product; where they differ, the definitions apply.

## File contents

**Layout.** The file holds an [image cube with moving origin](../product_types/gridded.md#image-cube-with-moving-origin) in the root group, with the data variable on `(time, y, x)`.

A file of this product holds the following items; each links to its definition, and the condition, where one is given, states when the tier applies.

| Item | Tier | Condition |
|---|---|---|
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`product_type`](../metadata_attributes/mandatory_global.md#product_type) `= "radar_cartesian"` | Required | |
| [`platform_is_mobile`](../metadata_attributes/optional_global.md#platform_is_mobile) `= "true"` | Required | moving platform |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| **Variables** | | |
| [`time`](../product_types/gridded.md#position-and-orientation-time), [`x`](../product_types/gridded.md#position-and-orientation-x), [`y`](../product_types/gridded.md#position-and-orientation-y) | Required | |
| [`longitude`](../product_types/gridded.md#position-and-orientation-longitude), [`latitude`](../product_types/gridded.md#position-and-orientation-latitude): `(time)` from a moving platform, scalar from a fixed platform | Required | |
| [`crs`](../product_types/gridded.md#position-and-orientation-crs) | Required | fixed platform |
| [`standard_name`](../product_types/gridded.md#position-and-orientation) `projection_x_coordinate` and `projection_y_coordinate` on `x` and `y` | Required | fixed platform |
| [`backscatter_amplitude`](../product_types/product_variables.md#backscatter_amplitude) or [`backscatter_power`](../product_types/product_variables.md#backscatter_power), exactly one | Required | |
| [`cartesian_resampling`](../product_types/gridded.md#cartesian_resampling) on the data variable | Required | |
| [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity) on the data variable | Required | `cartesian_resampling` other than `nearest_neighbor` |
| [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) `= "crs"` on the data variable | Required | fixed platform |
| [`comment`](../product_types/polar.md#data-variables) on the data variable, describing how the values were derived | Recommended | |
{: .contents-table }

## Example

A radar on a moving platform.

```
netcdf or_2025-01-15-11-00_radar_cartesian {
dimensions:
        time = 40 ;
        y = 1980 ;
        x = 1980 ;
variables:
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude(time) ;
                longitude:long_name = "longitude of the grid origin" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(time) ;
                latitude:long_name = "latitude of the grid origin" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double x(x) ;
                x:long_name = "eastward distance from the grid origin" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from the grid origin" ;
                y:units = "m" ;
        float backscatter_power(time, y, x) ;
                backscatter_power:long_name = "radar backscatter power" ;
                backscatter_power:units = "1" ;
                backscatter_power:_FillValue = NaNf ;
                backscatter_power:cartesian_resampling = "linear_interpolation" ;
                backscatter_power:averaged_quantity = "power" ;
                backscatter_power:comment = "backscatter power (I^2 + Q^2) in uncalibrated analog-to-digital units, mapped from polar coordinates by bilinear interpolation of linear power" ; // recommended

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 14.99584 ; // recommended
                :geospatial_lat_min = 14.99466 ; // recommended
                :geospatial_lon_max = 145.86905 ; // recommended
                :geospatial_lon_min = 145.86733 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ; // highly recommended
                :platform_is_mobile = "true" ;
                :product_type = "radar_cartesian" ;
                :summary = "Marine X-band radar backscatter images recorded on board R/V Ocean Research, one per antenna revolution, mapped onto a regular Cartesian grid centered on the radar antenna at the start of each revolution." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:00:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar Cartesian images from R/V Ocean Research" ; // highly recommended
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2025-01-15-11-00_radar_cartesian {
dimensions:
        time = 40 ;
        y = 1980 ;
        x = 1980 ;
variables:
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude(time) ;
                longitude:long_name = "longitude of the grid origin" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(time) ;
                latitude:long_name = "latitude of the grid origin" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double x(x) ;
                x:long_name = "eastward distance from the grid origin" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from the grid origin" ;
                y:units = "m" ;
        float backscatter_power(time, y, x) ;
                backscatter_power:long_name = "radar backscatter power" ;
                backscatter_power:units = "1" ;
                backscatter_power:_FillValue = NaNf ;
                backscatter_power:cartesian_resampling = "linear_interpolation" ;
                backscatter_power:averaged_quantity = "power" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :platform_is_mobile = "true" ;
                :product_type = "radar_cartesian" ;
}
```

## Example for a fixed platform

A radar on a fixed platform: [`longitude`](../product_types/gridded.md#position-and-orientation-longitude) and [`latitude`](../product_types/gridded.md#position-and-orientation-latitude) are scalar, and the file carries a [`crs`](../product_types/gridded.md#position-and-orientation-crs) centered on the radar antenna, with [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) on the data variable and the projection standard names on [`x`](../product_types/gridded.md#position-and-orientation-x) and [`y`](../product_types/gridded.md#position-and-orientation-y).

```
netcdf or_2023-08-31-17-00_radar_cartesian {
dimensions:
        time = 40 ;
        y = 1980 ;
        x = 1980 ;
variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 7.8853 ;
                crs:latitude_of_projection_origin = 54.1826 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude ;
                longitude:long_name = "longitude of the grid origin" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "latitude of the grid origin" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double x(x) ;
                x:long_name = "eastward distance from the grid origin" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from the grid origin" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        float backscatter_power(time, y, x) ;
                backscatter_power:long_name = "radar backscatter power" ;
                backscatter_power:units = "1" ;
                backscatter_power:_FillValue = NaNf ;
                backscatter_power:grid_mapping = "crs" ;
                backscatter_power:cartesian_resampling = "linear_interpolation" ;
                backscatter_power:averaged_quantity = "power" ;
                backscatter_power:comment = "backscatter power (I^2 + Q^2) in uncalibrated analog-to-digital units, mapped from polar coordinates by bilinear interpolation of linear power" ; // recommended

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 54.1826 ; // recommended
                :geospatial_lat_min = 54.1826 ; // recommended
                :geospatial_lon_max = 7.8853 ; // recommended
                :geospatial_lon_min = 7.8853 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ; // highly recommended
                :product_type = "radar_cartesian" ;
                :summary = "Marine X-band radar backscatter images from a fixed platform, one per antenna revolution, mapped onto a regular Cartesian grid centered on the radar antenna." ; // highly recommended
                :time_coverage_end = "2023-08-31T17:00:59Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar Cartesian images from a fixed platform" ; // highly recommended
data:
        longitude = 7.8853 ;
        latitude = 54.1826 ;
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2023-08-31-17-00_radar_cartesian {
dimensions:
        time = 40 ;
        y = 1980 ;
        x = 1980 ;
variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 7.8853 ;
                crs:latitude_of_projection_origin = 54.1826 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude ;
                longitude:long_name = "longitude of the grid origin" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "latitude of the grid origin" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double x(x) ;
                x:long_name = "eastward distance from the grid origin" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from the grid origin" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        float backscatter_power(time, y, x) ;
                backscatter_power:long_name = "radar backscatter power" ;
                backscatter_power:units = "1" ;
                backscatter_power:_FillValue = NaNf ;
                backscatter_power:grid_mapping = "crs" ;
                backscatter_power:cartesian_resampling = "linear_interpolation" ;
                backscatter_power:averaged_quantity = "power" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "radar_cartesian" ;
data:
        longitude = 7.8853 ;
        latitude = 54.1826 ;
}
```
