---
title: Pulse-averaged data (polar_pulse_averaged)
layout: default
parent: "Annex: Examples"
nav_order: 2
---

# L1b: Pulse-averaged data (`polar_pulse_averaged`)

{: .informative }
> An example of the data type [`polar_pulse_averaged`](../data_types/polar_pulse_averaged.md), which defines its structure and variables (see [Annex: Examples](index.md)).

## File contents

**Layout.** The file holds the [averaged sweeps](../data_types/polar_pulse_averaged.md): one `sweep_<n>` group per revolution or dwell, numbered from 0 in the order of acquisition.

| Item | Tier | Condition |
|---|---|---|
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`data_type`](../metadata_attributes/mandatory_global.md#data_type) `= "polar_pulse_averaged"` | Required | |
| [`platform_is_mobile`](../metadata_attributes/mandatory_global.md#platform_is_mobile) `= "true"` | Required | moving platform |
| [`platform_is_mobile`](../metadata_attributes/mandatory_global.md#platform_is_mobile) `= "false"` | Required | fixed platform |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| **Root group** | | |
| [`latitude`](../data_types/polar_pulse_averaged.md#root-group-latitude), [`longitude`](../data_types/polar_pulse_averaged.md#root-group-longitude) | Required | fixed platform |
| [`latitude`](../data_types/polar_pulse_averaged.md#root-group-latitude), [`longitude`](../data_types/polar_pulse_averaged.md#root-group-longitude) | Recommended | moving platform |
| [`altitude`](../data_types/polar_pulse_averaged.md#altitude) | Required | |
| [`radar_parameters`](../metadata_attributes/radar_parameters.md), [`georeference_correction`](../metadata_attributes/georeference_correction.md) groups | Optional | |
| **Each `sweep_<n>` group** | | |
| [`time`](../data_types/polar_pulse_averaged.md#time), [`range`](../data_types/polar_pulse_averaged.md#range), [`azimuth`](../data_types/polar_pulse_averaged.md#azimuth) | Required | |
| [`time_bounds`](../data_types/polar_pulse_averaged.md#time_bounds), with [`bounds`](../data_types/polar_pulse_averaged.md#time) `= "time_bounds"` on `time` | Optional | |
| [`meters_between_gates`](../data_types/polar_raw.md#meters_between_gates), [`meters_to_center_of_first_gate`](../data_types/polar_raw.md#meters_to_center_of_first_gate), [`spacing_is_constant`](../data_types/polar_raw.md#spacing_is_constant) on `range` | Optional | |
| [`sweep_mode`](../data_types/polar_pulse_averaged.md#sweep_mode), [`n_samples`](../data_types/polar_pulse_averaged.md#n_samples) | Required | |
| [`fixed_angle`](../data_types/polar_pulse_averaged.md#fixed_angle) | Required | `sweep_mode = "pointing"` |
| [`backscatter_amplitude`](../data_types/product_variables.md#backscatter_amplitude) or [`backscatter_power`](../data_types/product_variables.md#backscatter_power), exactly one | Required | |
| [`coordinates`](../data_types/polar_pulse_averaged.md#structure) `= "azimuth range"` on the data variable | Required | |
| [`cell_methods`](../data_types/polar_pulse_averaged.md) `= "time: mean"` and [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity) on the data variable | Required | |
| [`comment`](../data_types/polar_pulse_averaged.md#structure) on the data variable, describing how the values were derived | Recommended | |
| [`georeference`](../data_types/polar_pulse_averaged.md#navigation) subgroup, with [`latitude`](../data_types/polar_pulse_averaged.md#navigation-latitude), [`longitude`](../data_types/polar_pulse_averaged.md#navigation-longitude), and [`heading`](../data_types/polar_pulse_averaged.md#heading) | Recommended | moving platform |
| [`roll`](../data_types/polar_pulse_averaged.md#roll), [`pitch`](../data_types/polar_pulse_averaged.md#pitch) in the `georeference` subgroup | Optional | moving platform |
| [`source`](../metadata_attributes/variable_attributes.md#source), [`sampling_frequency`](../metadata_attributes/variable_attributes.md#sampling_frequency) on the navigation variables | Optional | moving platform |
{: .contents-table }

## Example

A radar on a ship, with the antenna held at a fixed direction for ten minutes and every eight consecutive pulses averaged into one ray.
The position and heading of the ship are given at the start of the dwell, and the [`georeference_correction`](../metadata_attributes/georeference_correction.md#example) group, whose contents are shown on its own page, is included.

```
netcdf or_2025-01-15-11-00_polar_pulse_averaged {
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
                :data_type = "polar_pulse_averaged" ;
                :geospatial_lat_max = 14.9958976192 ; // recommended
                :geospatial_lat_min = 14.99471 ; // recommended
                :geospatial_lon_max = 145.86898 ; // recommended
                :geospatial_lon_min = 145.8672647679 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER" ; // highly recommended
                :platform_is_mobile = "true" ;
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
        float backscatter_amplitude(time, range) ;
                backscatter_amplitude:_FillValue = NaNf ;
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

// ... a longer file holds further sweep_<n> groups of the same layout, one per dwell ...

group: georeference_correction { ... } // optional; as in the example under Georeference correction parameters
}
```

