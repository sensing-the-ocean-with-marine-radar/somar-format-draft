---
title: Cartesian image sequences (L1b)
layout: default
parent: "Annex: Example products"
nav_order: 3
---

# L1b: Cartesian image sequences

{: .informative }
> This page is informative. The product type `radar_cartesian` is one of the [gridded products](../product_types/gridded.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../metadata_attributes/product_variables.md).

## Example

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
        float backscatter_power(time, y, x) ;
                backscatter_power:long_name = "radar backscatter power" ;
                backscatter_power:units = "1" ;
                backscatter_power:_FillValue = NaNf ;
                backscatter_power:cartesian_resampling = "linear_interpolation" ;
                backscatter_power:comment = "backscatter power (I^2 + Q^2) in uncalibrated analog-to-digital units, mapped from polar coordinates by bilinear interpolation of linear power" ; // recommended

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 14.99584 ; // recommended
                :geospatial_lat_min = 14.99466 ; // recommended
                :geospatial_lon_max = 145.86905 ; // recommended
                :geospatial_lon_min = 145.86733 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ; // highly recommended
                :platform_is_mobile = "true" ; // required: the platform moves
                :product_type = "radar_cartesian" ;
                :summary = "Marine X-band radar backscatter images recorded on board R/V Ocean Research, one per antenna revolution, mapped onto a regular Cartesian grid centered on the radar antenna at the start of each revolution." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:00:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar Cartesian images from R/V Ocean Research" ; // highly recommended
}
```

For a fixed platform, `longitude` and `latitude` are scalar.
