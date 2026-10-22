---
title: Polar image sequences (L1b)
layout: default
parent: "Annex: Example products"
nav_order: 2
---

# L1b: Polar image sequences

{: .informative }
> This page is informative. The product type `radar_polar_regularized` is one of the [polar products](../product_types/polar.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md). The [file contents](#file-contents) summarize these definitions for this product; where they differ, the definitions apply.

## File contents

**Layout.** The file holds an [image cube](../product_types/polar.md#image-cube) in the root group, with the data variable on `(time, azimuth, range)`.

A file of this product holds the following items; each links to its definition, and the condition, where one is given, states when the tier applies.

| Item | Tier | Condition |
|---|---|---|
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`product_type`](../metadata_attributes/mandatory_global.md#product_type) `= "radar_polar_regularized"` | Required | |
| [`platform_is_mobile`](../metadata_attributes/optional_global.md#platform_is_mobile) `= "true"` | Required | moving platform |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| **Root group** | | |
| [`latitude`](../product_types/polar.md#coordinates-and-position-latitude), [`longitude`](../product_types/polar.md#coordinates-and-position-longitude) | Required | fixed platform |
| [`altitude`](../product_types/polar.md#altitude) | Required | |
| [`latitude`](../product_types/polar.md#moving-platforms-latitude), [`longitude`](../product_types/polar.md#moving-platforms-longitude), [`heading`](../product_types/polar.md#heading), on `(time)` or `(time, azimuth)` | Recommended | moving platform |
| [`source`](../metadata_attributes/variable_attributes.md#source), [`sampling_frequency`](../metadata_attributes/variable_attributes.md#sampling_frequency) on the navigation variables | Optional | moving platform |
| [`time`](../product_types/polar.md#image-cube-time), [`azimuth`](../product_types/polar.md#image-cube-azimuth), [`range`](../product_types/polar.md#image-cube-range) | Required | |
| [`rays_angle_resolution`](../product_types/polar.md#rays_angle_resolution) on `azimuth` | Optional | |
| [`meters_between_gates`](../product_types/polar.md#meters_between_gates), [`meters_to_center_of_first_gate`](../product_types/polar.md#meters_to_center_of_first_gate), [`spacing_is_constant`](../product_types/polar.md#spacing_is_constant) on `range` | Optional | |
| [`ray_time`](../product_types/product_variables.md#ray_time) | Optional | |
| [`backscatter_amplitude`](../product_types/product_variables.md#backscatter_amplitude) or [`backscatter_power`](../product_types/product_variables.md#backscatter_power), exactly one | Required | |
| [`azimuth_regularization`](../product_types/polar.md#azimuth_regularization) on the data variable | Required | |
| [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity) on the data variable | Required | `azimuth_regularization` other than `nearest_neighbor` |
| [`comment`](../product_types/polar.md#data-variables) on the data variable, describing how the values were derived | Recommended | |
| [`radar_parameters`](../metadata_attributes/radar_parameters.md), [`georeference_correction`](../metadata_attributes/georeference_correction.md) groups | Optional | |
{: .contents-table }

## Example

A radar on a fixed platform.

```
netcdf or_2023-08-31-17-00_radar_polar_regularized {
dimensions:
        time = 40 ;
        azimuth = 1440 ;
        range = 1000 ;
variables:
        double latitude ;
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of radar antenna" ;
        double longitude ;
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of radar antenna" ;
        double altitude ;
                altitude:units = "m" ;
                altitude:standard_name = "altitude" ;
                altitude:long_name = "height of radar antenna above mean sea level" ;
        double time(time) ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:calendar = "standard" ;
                time:standard_name = "time" ;
                time:long_name = "start time of radar measurement" ;
        float azimuth(azimuth) ;
                azimuth:units = "degree" ;
                azimuth:long_name = "radar antenna pointing direction on regular grid" ;
                azimuth:rays_angle_resolution = 0.25f ; // optional
                azimuth:comment = "clockwise positive, relative to the radar's zero direction, not north-oriented" ;
        float range(range) ;
                range:units = "m" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ; // optional
                range:meters_to_center_of_first_gate = 3.75f ; // optional
                range:meters_between_gates = 7.5f ; // optional
        float ray_time(azimuth) ; // optional
                ray_time:units = "s" ;
                ray_time:long_name = "time of each ray after the start of the revolution" ;
        float backscatter_amplitude(time, azimuth, range) ;
                backscatter_amplitude:long_name = "radar backscatter amplitude" ;
                backscatter_amplitude:units = "1" ;
                backscatter_amplitude:azimuth_regularization = "nearest_neighbor" ;
                backscatter_amplitude:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). Rays recorded at irregular azimuths were regularized onto the azimuth grid by nearest-neighbor selection." ; // recommended

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 54.1826 ; // recommended
                :geospatial_lat_min = 54.1826 ; // recommended
                :geospatial_lon_max = 7.8853 ; // recommended
                :geospatial_lon_min = 7.8853 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ; // highly recommended
                :product_type = "radar_polar_regularized" ;
                :summary = "Marine X-band radar backscatter images from a fixed platform, mapped onto regular range and azimuth axes in the polar coordinates of the radar." ; // highly recommended
                :time_coverage_end = "2023-08-31T17:00:59Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar polar images from a fixed platform" ; // highly recommended
data:
        latitude = 54.1826 ;
        longitude = 7.8853 ;
        altitude = 43. ;
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2023-08-31-17-00_radar_polar_regularized {
dimensions:
        time = 40 ;
        azimuth = 1440 ;
        range = 1000 ;
variables:
        double latitude ;
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of radar antenna" ;
        double longitude ;
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of radar antenna" ;
        double altitude ;
                altitude:units = "m" ;
                altitude:standard_name = "altitude" ;
                altitude:long_name = "height of radar antenna above mean sea level" ;
        double time(time) ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:calendar = "standard" ;
                time:standard_name = "time" ;
                time:long_name = "start time of radar measurement" ;
        float azimuth(azimuth) ;
                azimuth:units = "degree" ;
                azimuth:long_name = "radar antenna pointing direction on regular grid" ;
                azimuth:comment = "clockwise positive, relative to the radar's zero direction, not north-oriented" ;
        float range(range) ;
                range:units = "m" ;
                range:long_name = "range_to_measurement_volume" ;
        float backscatter_amplitude(time, azimuth, range) ;
                backscatter_amplitude:long_name = "radar backscatter amplitude" ;
                backscatter_amplitude:units = "1" ;
                backscatter_amplitude:azimuth_regularization = "nearest_neighbor" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "radar_polar_regularized" ;
data:
        latitude = 54.1826 ;
        longitude = 7.8853 ;
        altitude = 43. ;
}
```

## Example for a moving platform

A radar on a ship, with position and heading recorded per sweep, along with the optional [`radar_parameters`](../metadata_attributes/radar_parameters.md#example) and [`georeference_correction`](../metadata_attributes/georeference_correction.md#example) groups, whose contents are shown on their own pages.

```
netcdf or_2025-01-15-11-00_radar_polar_regularized {
dimensions:
        time = 40 ;
        azimuth = 1440 ;
        range = 1000 ;
variables:
        double altitude ;
                altitude:units = "m" ;
                altitude:standard_name = "altitude" ;
                altitude:long_name = "height of radar antenna above mean sea level" ;
        double time(time) ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:calendar = "standard" ;
                time:standard_name = "time" ;
                time:long_name = "start time of radar measurement" ;
        double latitude(time) ; // recommended
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of GPS antenna at the start of the revolution" ;
        double longitude(time) ; // recommended
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of GPS antenna at the start of the revolution" ;
        float heading(time) ; // recommended
                heading:units = "degree" ;
                heading:standard_name = "platform_orientation" ;
                heading:long_name = "heading of the platform relative to true north at the start of the revolution" ;
        float azimuth(azimuth) ;
                azimuth:units = "degree" ;
                azimuth:long_name = "radar antenna pointing direction on regular grid" ;
                azimuth:rays_angle_resolution = 0.25f ; // optional
                azimuth:comment = "clockwise positive, relative to the bow of the ship, not north-oriented" ;
        float range(range) ;
                range:units = "m" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ; // optional
                range:meters_to_center_of_first_gate = 3.75f ; // optional
                range:meters_between_gates = 7.5f ; // optional
        float ray_time(azimuth) ; // optional
                ray_time:units = "s" ;
                ray_time:long_name = "time of each ray after the start of the revolution" ;
        float backscatter_amplitude(time, azimuth, range) ;
                backscatter_amplitude:long_name = "radar backscatter amplitude" ;
                backscatter_amplitude:units = "1" ;
                backscatter_amplitude:azimuth_regularization = "nearest_neighbor" ;
                backscatter_amplitude:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). Rays recorded at irregular azimuths were regularized onto the azimuth grid by nearest-neighbor selection." ; // recommended

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 14.9958976192 ; // recommended
                :geospatial_lat_min = 14.99471 ; // recommended
                :geospatial_lon_max = 145.86898 ; // recommended
                :geospatial_lon_min = 145.8672647679 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ; // highly recommended
                :platform_is_mobile = "true" ;
                :product_type = "radar_polar_regularized" ;
                :summary = "Marine X-band radar backscatter images recorded on board R/V Ocean Research, mapped onto regular range and azimuth axes in the polar coordinates of the radar." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:00:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar polar images from R/V Ocean Research" ; // highly recommended
data:
        altitude = 18.5 ;

group: radar_parameters { ... } // optional; as in the example under Radar parameters
group: georeference_correction { ... } // optional; as in the example under Georeference correction parameters
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2025-01-15-11-00_radar_polar_regularized {
dimensions:
        time = 40 ;
        azimuth = 1440 ;
        range = 1000 ;
variables:
        double altitude ;
                altitude:units = "m" ;
                altitude:standard_name = "altitude" ;
                altitude:long_name = "height of radar antenna above mean sea level" ;
        double time(time) ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:calendar = "standard" ;
                time:standard_name = "time" ;
                time:long_name = "start time of radar measurement" ;
        float azimuth(azimuth) ;
                azimuth:units = "degree" ;
                azimuth:long_name = "radar antenna pointing direction on regular grid" ;
                azimuth:comment = "clockwise positive, relative to the bow of the ship, not north-oriented" ;
        float range(range) ;
                range:units = "m" ;
                range:long_name = "range_to_measurement_volume" ;
        float backscatter_amplitude(time, azimuth, range) ;
                backscatter_amplitude:long_name = "radar backscatter amplitude" ;
                backscatter_amplitude:units = "1" ;
                backscatter_amplitude:azimuth_regularization = "nearest_neighbor" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :platform_is_mobile = "true" ;
                :product_type = "radar_polar_regularized" ;
data:
        altitude = 18.5 ;

}
```
