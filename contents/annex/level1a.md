---
title: Radar "raw" data (L1a)
layout: default
parent: "Annex: Example products"
nav_order: 1
---

# L1a: "raw" radar data

{: .informative }
> This page is informative. The product type `radar_polar_raw` is one of the [polar products](../product_types/polar.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../metadata_attributes/product_variables.md).

## Example

A radar on a fixed platform.

```
netcdf or_2023-08-31-17-00_radar_polar_raw {
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

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 54.1826 ; // recommended
                :geospatial_lat_min = 54.1826 ; // recommended
                :geospatial_lon_max = 7.8853 ; // recommended
                :geospatial_lon_min = 7.8853 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER" ; // highly recommended
                :product_type = "radar_polar_raw" ;
                :summary = "Raw marine X-band radar backscatter from a fixed platform, converted from the manufacturer's format into NetCDF with every ray kept and no interpolation or calibration." ; // highly recommended
                :time_coverage_end = "2023-08-31T17:00:59Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar raw data from a fixed platform" ; // highly recommended
data:
        latitude = 54.1826 ;
        longitude = 7.8853 ;
        altitude = 43. ;

group: sweep_0 {
  dimensions:
        time = 4500 ; // number of rays in the sweep
        range = 1000 ; // number of range gates
  variables:
        double time(time) ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:calendar = "standard" ;
                time:standard_name = "time" ;
                time:long_name = "time of ray" ;
        float range(range) ;
                range:units = "m" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ; // optional
                range:meters_to_center_of_first_gate = 3.75f ; // optional
                range:meters_between_gates = 7.5f ; // optional
        float azimuth(time) ;
                azimuth:units = "degree" ;
                azimuth:long_name = "radar antenna pointing direction" ;
                azimuth:comment = "clockwise positive, relative to the radar's zero direction, not north-oriented" ;
        ushort backscatter_amplitude(time, range) ;
                backscatter_amplitude:scale_factor = 0.176738930567883 ;
                backscatter_amplitude:add_offset = 0. ;
                backscatter_amplitude:_FillValue = 65535US ;
                backscatter_amplitude:long_name = "radar backscatter amplitude" ;
                backscatter_amplitude:units = "1" ;
                backscatter_amplitude:coordinates = "azimuth range" ;
                backscatter_amplitude:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). I and Q are the in-phase and quadrature channels both measured in counts of the analog-to-digital converter (ADC)." ; // recommended
  } // group sweep_0

// ... additional sweep_<n> groups follow the same layout, one per sweep ...
}
```

## Example for a moving platform

A radar on a ship, with the position and heading of the ship at the start of each sweep, the instrument they are taken from, and the [`radar_parameters`](../metadata_attributes/radar_parameters.md#example) and [`georeference_correction`](../metadata_attributes/georeference_correction.md#example) groups, whose contents are shown on their own pages.

```
netcdf or_2025-01-15-11-00_radar_polar_raw {
variables:
        double latitude ; // recommended
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of GPS antenna at the start of the file" ;
        double longitude ; // recommended
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of GPS antenna at the start of the file" ;
        double altitude ;
                altitude:units = "m" ;
                altitude:standard_name = "altitude" ;
                altitude:long_name = "height of radar antenna above mean sea level" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 14.9958976192 ; // recommended
                :geospatial_lat_min = 14.99471 ; // recommended
                :geospatial_lon_max = 145.86898 ; // recommended
                :geospatial_lon_min = 145.8672647679 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER" ; // highly recommended
                :platform_is_mobile = "true" ; // required: the platform moves
                :product_type = "radar_polar_raw" ;
                :summary = "Raw marine X-band radar backscatter recorded on board R/V Ocean Research, converted from the manufacturer's format into NetCDF with every ray kept and no interpolation or calibration." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:00:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar raw data from R/V Ocean Research" ; // highly recommended
data:
        latitude = 14.9958976192 ;
        longitude = 145.8672647679 ;
        altitude = 18.5 ;

group: sweep_0 {
  dimensions:
        time = 4500 ; // number of rays in the sweep
        range = 1000 ; // number of range gates
  variables:
        double time(time) ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:calendar = "standard" ;
                time:standard_name = "time" ;
                time:long_name = "time of ray" ;
        float range(range) ;
                range:units = "m" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ; // optional
                range:meters_to_center_of_first_gate = 3.75f ; // optional
                range:meters_between_gates = 7.5f ; // optional
        float azimuth(time) ;
                azimuth:units = "degree" ;
                azimuth:long_name = "radar antenna pointing direction" ;
                azimuth:comment = "clockwise positive, relative to the bow of the ship, not north-oriented" ;
        string sweep_mode ; // optional
                sweep_mode:long_name = "sweep scan mode" ;
        ushort backscatter_amplitude(time, range) ;
                backscatter_amplitude:scale_factor = 0.176738930567883 ;
                backscatter_amplitude:add_offset = 0. ;
                backscatter_amplitude:_FillValue = 65535US ;
                backscatter_amplitude:long_name = "radar backscatter amplitude" ;
                backscatter_amplitude:units = "1" ;
                backscatter_amplitude:coordinates = "azimuth range" ;
                backscatter_amplitude:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). I and Q are the in-phase and quadrature channels both measured in counts of the analog-to-digital converter (ADC)." ; // recommended
  data:
        sweep_mode = "azimuth_surveillance" ;

  group: georeference { // recommended
    variables:
        double latitude ;
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of GPS antenna at the start of the sweep" ;
                latitude:source = "Kongsberg Seapath 380 GNSS-aided inertial navigation system (position, heading, and attitude)" ; // optional
                latitude:sampling_frequency = 10. ; // optional
        double longitude ;
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of GPS antenna at the start of the sweep" ;
                longitude:source = "Kongsberg Seapath 380 GNSS-aided inertial navigation system (position, heading, and attitude)" ; // optional
                longitude:sampling_frequency = 10. ; // optional
        float heading ;
                heading:units = "degree" ;
                heading:standard_name = "platform_orientation" ;
                heading:long_name = "heading of the platform relative to true north at the start of the sweep" ;
                heading:source = "Kongsberg Seapath 380 GNSS-aided inertial navigation system (position, heading, and attitude)" ; // optional
                heading:sampling_frequency = 10. ; // optional
    } // group georeference
  } // group sweep_0

// ... additional sweep_<n> groups follow the same layout, one per sweep ...

group: radar_parameters { ... } // optional; as in the example under Radar parameters
group: georeference_correction { ... } // optional; as in the example under Georeference correction parameters
}
```
