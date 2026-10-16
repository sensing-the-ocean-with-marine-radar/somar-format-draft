---
title: Polar image sequences (L1b)
layout: default
parent: Level 1 products
grand_parent: SOMaR product types
nav_order: 2
---

# L1b: Polar image sequences

Level 1b polar images (`radar_polar_regularized`, short `pol3d`, a three-dimensional cube in polar coordinates) are radar image sequences that remain in the polar coordinates of the sensor but are mapped onto a regular range and azimuth axis, so that all images of a sequence share the same grid.
They are usually derived from Level 1a data.
Each time step is one complete antenna revolution, corresponding to one sweep of the [Level 1a](level1a.md) data, and the data variable has the dimensions `(time, azimuth, range)` and holds uncalibrated amplitude or power.
The `range` and `azimuth` variables carry the same attributes as at [Level 1a](level1a.md#sweep-groups), which are taken from the WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes).
As at Level 1a, the azimuth is given relative to the radar's zero direction and is not necessarily north-oriented; it is related to true north through the platform `heading` and the `azimuth_correction` (see [Georeferencing](../../georeferencing/index.md#polar-sensor-coordinates)).
The image cube with the dimensions `(time, azimuth, range)` has no equivalent in FM 301, which keeps the individual rays of each sweep, and is specific to SOMaR.

The regular azimuth axis and the resampling onto it are recorded in two attributes.

| Attribute | Values | Description |
|---|---|---|
| `azimuth_regularization`<br><small>SOMaR</small> | String; one of `nearest_neighbor`, `linear_interpolation`, `average` | On the data variable: the method used to resample pulses recorded at irregular azimuths onto the regular `azimuth` axis: selection of the closest pulse, linear interpolation between the two adjacent pulses, or the mean of all pulses falling within each azimuth bin. Should be accompanied by a `comment` describing the method in words. |
| `rays_angle_resolution`<br><small>SOMaR</small> | Number; degree | On `azimuth`: the spacing of the regular azimuth axis. Named after the FM 301 variable `rays_angle_resolution`, which gives the angular spacing of rays that are indexed to a regular grid. |
{: .attribute-table }

`time` gives the start time of each revolution.
The optional variable `pulse_time`, with the dimension `azimuth`, gives the time of each azimuth bin in seconds after the start of its revolution, i.e. the time of the selected pulse, the correspondingly interpolated time, or the mean time of the averaged pulses. It is the same for all images, which assumes that the antenna rotates steadily.

## Position and heading

The scalar variable `altitude` in the root group is required for all platforms (fixed and moving) and gives the height of the radar antenna above mean sea level; it is assumed constant.
For a fixed platform, scalar `latitude` and `longitude` in the root group give the antenna position, as at [Level 1a](level1a.md#root-group).

For a moving platform, the position and heading of the platform are stored in the root group using the variable names and units of CfRadial 2.1 (Section 5.4). As at Level 1a, they can be given in one of two ways:

- **Per sweep.** The variables have the dimension `(time)` and give the values at the start of each revolution (image).
- **Per pulse.** The variables have the dimensions `(time, azimuth)` and give the values for every pulse (azimuth bin).

| Variable | Values | Description |
|---|---|---|
| `latitude`<br><small>[CfRadial 2.1](https://github.com/NCAR/CfRadial/tree/master/docs), Section 5.4</small> | double `(time)` or `(time, azimuth)`; `degrees_north` | Required. Recorded latitude (WGS 84). |
| `longitude`<br><small>[CfRadial 2.1](https://github.com/NCAR/CfRadial/tree/master/docs), Section 5.4</small> | double `(time)` or `(time, azimuth)`; `degrees_east` | Required. Recorded longitude (WGS 84). |
| `heading`<br><small>[CfRadial 2.1](https://github.com/NCAR/CfRadial/tree/master/docs), Section 5.4</small> | float `(time)` or `(time, azimuth)`; `degree` | Required. Heading of the platform relative to true north. |
{: .variable-table }

As at Level 1a, `latitude` and `longitude` are stored as recorded, and the optional [`georeference_correction` group](../../metadata_attributes/georeference_correction.md) gives the known offsets of azimuth, range, time, and antenna position.

## Radar parameters

Like Level 1a, constant technical parameters of the radar antenna, pulse, and scan can be stored in an optional root-level group named [`radar_parameters`](../../metadata_attributes/radar_parameters.md). When pulse or scan parameters (such as `prt` or `scan_rate`) vary over time, they are stored in the root group instead, with dimension `time` (varying per revolution) or `(time, azimuth)` (varying per pulse).

## Minimal example

A radar on a fixed platform.

```
netcdf or_2023-08-31-17-00_radar_polar_regularized {
dimensions:
        time = 41 ;
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
                azimuth:rays_angle_resolution = 0.25f ;
                azimuth:comment = "clockwise positive, relative to the radar's zero direction, not North-oriented" ;
        float range(range) ;
                range:units = "m" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ;
                range:meters_to_center_of_first_gate = 3.75f ;
                range:meters_between_gates = 7.5f ;
        float pulse_time(azimuth) ;
                pulse_time:units = "s" ;
                pulse_time:long_name = "time of each azimuth bin after the start of the revolution" ;
        float polar_amp(time, azimuth, range) ;
                polar_amp:long_name = "radar_backscatter_amplitude" ;
                polar_amp:units = "1" ;
                polar_amp:azimuth_regularization = "nearest_neighbor" ;
                polar_amp:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). Pulses recorded at irregular azimuths were regularized onto the azimuth grid by nearest-neighbor selection." ;

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

A radar on a ship, with position and heading recorded per sweep, along with the optional `radar_parameters` and `georeference_correction` groups.

```
netcdf or_2025-01-15-11-00_radar_polar_regularized {
dimensions:
        time = 41 ;
        azimuth = 1440 ;
        range = 1000 ;
variables:
        double altitude ;
                altitude:units = "m" ;
                altitude:standard_name = "altitude" ;
                altitude:long_name = "height of radar antenna above mean sea level" ;
        string platform_type ;
                platform_type:long_name = "platform type" ;
        double time(time) ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:calendar = "standard" ;
                time:standard_name = "time" ;
                time:long_name = "start time of radar measurement" ;
        double latitude(time) ;
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of GPS antenna at the start of the revolution" ;
        double longitude(time) ;
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of GPS antenna at the start of the revolution" ;
        float heading(time) ;
                heading:units = "degree" ;
                heading:standard_name = "platform_orientation" ;
                heading:long_name = "heading of the platform relative to true north at the start of the revolution" ;
        float azimuth(azimuth) ;
                azimuth:units = "degree" ;
                azimuth:long_name = "radar antenna pointing direction on regular grid" ;
                azimuth:rays_angle_resolution = 0.25f ;
                azimuth:comment = "clockwise positive, relative to the radar's zero direction, not North-oriented" ;
        float range(range) ;
                range:units = "m" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ;
                range:meters_to_center_of_first_gate = 3.75f ;
                range:meters_between_gates = 7.5f ;
        float pulse_time(azimuth) ;
                pulse_time:units = "s" ;
                pulse_time:long_name = "time of each azimuth bin after the start of the revolution" ;
        float polar_amp(time, azimuth, range) ;
                polar_amp:long_name = "radar_backscatter_amplitude" ;
                polar_amp:units = "1" ;
                polar_amp:azimuth_regularization = "nearest_neighbor" ;
                polar_amp:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). Pulses recorded at irregular azimuths were regularized onto the azimuth grid by nearest-neighbor selection." ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :platform_is_mobile = "true" ;
                :product_type = "radar_polar_regularized" ;
data:
        altitude = 18.5 ;
        platform_type = "ship" ;

group: radar_parameters {
  variables:
        float beam_width_h ;
                beam_width_h:units = "degree" ;
                beam_width_h:long_name = "horizontal antenna beam width" ;
        float beam_width_v ;
                beam_width_v:units = "degree" ;
                beam_width_v:long_name = "vertical antenna beam width" ;
        float frequency ;
                frequency:units = "s-1" ;
                frequency:long_name = "operating frequency of the radar" ;
        string polarization_mode ;
                polarization_mode:long_name = "antenna polarization mode" ;
        float pulse_width ;
                pulse_width:units = "s" ;
                pulse_width:long_name = "length of the transmitted pulse" ;
        float prt ;
                prt:units = "s" ;
                prt:long_name = "pulse repetition time" ;
        float scan_rate ;
                scan_rate:units = "degree s-1" ;
                scan_rate:long_name = "antenna rotation rate" ;
        int n_samples ;
                n_samples:long_name = "number of samples contributing to each stored pulse" ;
  data:
        beam_width_h = 0.95 ;
        beam_width_v = 20. ;
        frequency = 9.41e+09 ;
        polarization_mode = "vertical" ;
        pulse_width = 5.e-08 ;
        prt = 3.33e-04 ;
        scan_rate = 240. ;
        n_samples = 1 ;
  } // group radar_parameters

group: georeference_correction {
  variables:
        float azimuth_correction ;
                azimuth_correction:units = "degree" ;
                azimuth_correction:long_name = "correction to azimuth values" ;
        float range_correction ;
                range_correction:units = "m" ;
                range_correction:long_name = "correction to range values" ;
        double time_correction ;
                time_correction:units = "s" ;
                time_correction:long_name = "correction to time values" ;
        float position_offset_x ;
                position_offset_x:units = "m" ;
                position_offset_x:long_name = "position of radar antenna relative to GPS antenna, positive to starboard" ;
        float position_offset_y ;
                position_offset_y:units = "m" ;
                position_offset_y:long_name = "position of radar antenna relative to GPS antenna, positive toward the bow" ;
  data:
        azimuth_correction = -1.3 ;
        range_correction = -22.5 ;
        time_correction = 0.35 ;
        position_offset_x = 2.4 ;
        position_offset_y = -11.8 ;
  } // group georeference_correction
}
```

If the position and heading are given per pulse instead, the variables have the dimensions `(time, azimuth)`:

```
        double latitude(time, azimuth) ;
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of GPS antenna" ;
        double longitude(time, azimuth) ;
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of GPS antenna" ;
        float heading(time, azimuth) ;
                heading:units = "degree" ;
                heading:standard_name = "platform_orientation" ;
                heading:long_name = "heading of the platform relative to true north" ;
```
