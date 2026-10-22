---
title: Pulse-averaged pointing data (L1b)
layout: default
parent: "Annex: Example products"
nav_order: 3
---

# L1b: Pulse-averaged pointing data

{: .informative }
> This page is informative. The product type `radar_polar_averaged` is one of the [polar products](../product_types/polar.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md).

## Example

A radar on a ship, with the antenna held at a fixed direction for ten minutes and every eight consecutive pulses averaged into one ray.
The position and heading of the ship are given at the start of the dwell, and the [`georeference_correction`](../metadata_attributes/georeference_correction.md#example) group, whose contents are shown on its own page, is included.

```
netcdf or_2025-01-15-11-00_radar_polar_averaged {
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
                :platform_is_mobile = "true" ;
                :product_type = "radar_polar_averaged" ;
                :summary = "Marine X-band radar backscatter recorded in pointing mode on board R/V Ocean Research, with the amplitude of every eight consecutive pulses averaged into one ray." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:09:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar pulse-averaged pointing data from R/V Ocean Research" ; // highly recommended
data:
        latitude = 14.9958976192 ;
        longitude = 145.8672647679 ;
        altitude = 18.5 ;

group: sweep_0 {
  dimensions:
        time = 225000 ; // number of rays in the dwell, e.g. 10 min at 3000 Hz PRF averaged over 8 pulses
        range = 1000 ; // number of range gates
        nv = 2 ;
  variables:
        double time(time) ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:calendar = "standard" ;
                time:standard_name = "time" ;
                time:long_name = "mean time of the averaged pulses" ;
                time:bounds = "time_bounds" ; // optional
        double time_bounds(time, nv) ; // optional
                time_bounds:units = "seconds since 1970-01-01T00:00:00Z" ;
                time_bounds:calendar = "standard" ;
                time_bounds:long_name = "time of the first and last averaged pulse" ;
        float range(range) ;
                range:units = "m" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ; // optional
                range:meters_to_center_of_first_gate = 3.75f ; // optional
                range:meters_between_gates = 7.5f ; // optional
        float azimuth(time) ;
                azimuth:units = "degree" ;
                azimuth:long_name = "mean radar antenna pointing direction of the averaged pulses" ;
                azimuth:comment = "clockwise positive, relative to the bow of the ship, not north-oriented" ;
        string sweep_mode ;
                sweep_mode:long_name = "sweep scan mode" ;
        float fixed_angle ;
                fixed_angle:units = "degree" ;
                fixed_angle:long_name = "nominal antenna pointing direction" ;
                fixed_angle:comment = "clockwise positive, relative to the bow of the ship, not north-oriented" ;
        int n_samples ;
                n_samples:long_name = "number of pulses averaged into each ray" ;
        ushort backscatter_amplitude(time, range) ;
                backscatter_amplitude:scale_factor = 0.176738930567883 ;
                backscatter_amplitude:add_offset = 0. ;
                backscatter_amplitude:_FillValue = 65535US ;
                backscatter_amplitude:long_name = "radar backscatter amplitude" ;
                backscatter_amplitude:units = "1" ;
                backscatter_amplitude:coordinates = "azimuth range" ;
                backscatter_amplitude:cell_methods = "time: mean" ;
                backscatter_amplitude:averaged_quantity = "amplitude" ;
                backscatter_amplitude:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU), averaged over n_samples consecutive pulses. I and Q are the in-phase and quadrature channels both measured in counts of the analog-to-digital converter (ADC)." ; // recommended
  data:
        sweep_mode = "pointing" ;
        fixed_angle = 45. ;
        n_samples = 8 ;

  group: georeference { // recommended
    variables:
        double latitude ;
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of GPS antenna at the start of the sweep" ;
        double longitude ;
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of GPS antenna at the start of the sweep" ;
        float heading ;
                heading:units = "degree" ;
                heading:standard_name = "platform_orientation" ;
                heading:long_name = "heading of the platform relative to true north at the start of the sweep" ;
    } // group georeference
  } // group sweep_0

// ... additional sweep_<n> groups follow the same layout, one per dwell ...

group: georeference_correction { ... } // optional; as in the example under Georeference correction parameters
}
```
