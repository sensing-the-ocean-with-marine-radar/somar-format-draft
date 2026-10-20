---
title: Polar image sequences (L1b)
layout: default
parent: "Level 1: Radar data"
grand_parent: SOMaR product types
nav_order: 2
---

# L1b: Polar image sequences

Level 1b polar images (`radar_polar_regularized`, a three-dimensional cube in polar coordinates) are radar image sequences that remain in the polar coordinates of the sensor but are mapped onto a regular range and azimuth axis, so that all images of a sequence share the same grid.
They are usually derived from Level 1a data.
Each time step is one complete antenna revolution, corresponding to one sweep of the [Level 1a](level1a.md) data, and the data variable, `backscatter_amplitude` or `backscatter_power`, has the dimensions `(time, azimuth, range)` and holds uncalibrated amplitude or power.
The `range` and `azimuth` variables carry the same attributes as at [Level 1a](level1a.md#sweep-groups), which are taken from the WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes).
As at Level 1a, the azimuth is given relative to the radar's zero direction and is not necessarily north-oriented; it is related to true north through the platform `heading` and the `azimuth_correction` (see [Georeferencing](../../georeferencing/index.md#polar-sensor-coordinates)).
The image cube with the dimensions `(time, azimuth, range)` has no equivalent in FM 301, which keeps the individual rays of each sweep, and is specific to SOMaR.

## Variables

In addition to the [position and heading](#position-and-heading), the file holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `time`<br><small>[FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes), Table 301-6</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each revolution. |
| `azimuth`<br><small>[FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes), Table 301-7</small> | float `(azimuth)`; `degree` | Required. Regular azimuth axis, clockwise positive, relative to the radar's zero direction. |
| `range`<br><small>[FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes), Table 301-6</small> | float `(range)`; `m` | Required. Slant range to the center of each range bin. |
| `ray_time`<br><small>SOMaR</small> | float `(azimuth)`; `s` | Optional. Time of each ray after the start of its revolution, i.e. the time of the selected Level 1a ray, the correspondingly interpolated time, or the mean time of the averaged rays. It is the same for all images, which assumes that the antenna rotates steadily. |
| `backscatter_amplitude`, `backscatter_power`<br><small>SOMaR</small> | `(time, azimuth, range)`; `1` or `dB` | Exactly one is required. Uncalibrated backscatter amplitude or power, with the names and attributes described at [Level 1a](level1a.md#data-variables). |
{: .variable-table }

The regular azimuth axis and the resampling onto it are recorded in two attributes.

| Attribute | Values | Description |
|---|---|---|
| `azimuth_regularization`<br><small>SOMaR</small> | String; one of `nearest_neighbor`, `linear_interpolation`, `average` | On the data variable: the method used to resample rays recorded at irregular azimuths onto the regular `azimuth` axis: selection of the closest ray, linear interpolation between the two adjacent rays, or the mean of all rays falling within each azimuth bin. Interpolation and averaging are done on linear power: amplitude (`backscatter_amplitude`) is squared, and values in `dB` are converted to linear units, beforehand, and the result is converted back to the quantity and unit of the data variable. If the signal cannot be linearized, such as a log-compressed video signal, they are done on the stored values instead. Should be accompanied by a `comment` describing the method in words, which must also say when the stored values were used. |
| `rays_angle_resolution`<br><small>SOMaR</small> | Number; degree | On `azimuth`: the spacing of the regular azimuth axis. Named after the FM 301 variable `rays_angle_resolution` (Table 301-8), which gives the angular spacing of rays that are indexed to a regular grid; the accompanying FM 301 flag `rays_are_indexed` is implied to be `"true"` and is not stored. |
{: .attribute-table }

{: .open_issue }
Only backscatter amplitude and power are specified. Variables for the data of coherent radars, such as phase or radial Doppler velocity, are not yet defined (see [Level 1a](level1a.md#coherent-data)).

## Position and heading

The scalar variables `altitude` and `platform_type` in the root group are required for all platforms (fixed and moving), as at [Level 1a](level1a.md#root-group); `altitude` gives the height of the radar antenna above mean sea level and is assumed constant.
For a fixed platform, scalar `latitude` and `longitude` in the root group give the antenna position, as at [Level 1a](level1a.md#root-group).

For a moving platform, the position and heading of the platform are stored in the root group using the variable names and units of CfRadial 2.1 (Section 5.4). As at Level 1a, they can be given in one of two ways:

- **Per sweep.** The variables have the dimension `(time)` and give the values at the start of each revolution (image).
- **Per ray.** The variables have the dimensions `(time, azimuth)` and give the values for every ray (azimuth bin).

| Variable | Values | Description |
|---|---|---|
| `latitude`<br><small>[CfRadial 2.1](https://github.com/NCAR/CfRadial/tree/master/docs), Section 5.4</small> | double `(time)` or `(time, azimuth)`; `degrees_north` | Required. Recorded latitude (WGS 84). |
| `longitude`<br><small>[CfRadial 2.1](https://github.com/NCAR/CfRadial/tree/master/docs), Section 5.4</small> | double `(time)` or `(time, azimuth)`; `degrees_east` | Required. Recorded longitude (WGS 84). |
| `heading`<br><small>[CfRadial 2.1](https://github.com/NCAR/CfRadial/tree/master/docs), Section 5.4</small> | float `(time)` or `(time, azimuth)`; `degree` | Required. Heading of the platform relative to true north. |
{: .variable-table }

As at Level 1a, `latitude` and `longitude` are stored as recorded, and the optional [`georeference_correction` group](../../metadata_attributes/georeference_correction.md) gives the known offsets of azimuth, range, time, and antenna position.

## Radar parameters

Like Level 1a, constant technical parameters of the radar antenna, pulse, and scan can be stored in an optional root-level group named [`radar_parameters`](../../metadata_attributes/radar_parameters.md). When pulse or scan parameters (such as `prt` or `scan_rate`) vary over time, they are stored in the root group instead, with dimension `time` (varying per revolution) or `(time, azimuth)` (varying per ray).

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
        string platform_type ;
                platform_type:long_name = "platform type" ;
        double time(time) ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:calendar = "standard" ;
                time:standard_name = "time" ;
                time:long_name = "start time of radar measurement" ;
        float azimuth(azimuth) ;
                azimuth:units = "degree" ;
                azimuth:long_name = "radar antenna pointing direction on regular grid" ;
                azimuth:rays_angle_resolution = 0.25f ;
                azimuth:comment = "clockwise positive, relative to the radar's zero direction, not north-oriented" ;
        float range(range) ;
                range:units = "m" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ;
                range:meters_to_center_of_first_gate = 3.75f ;
                range:meters_between_gates = 7.5f ;
        float ray_time(azimuth) ;
                ray_time:units = "s" ;
                ray_time:long_name = "time of each ray after the start of the revolution" ;
        float backscatter_amplitude(time, azimuth, range) ;
                backscatter_amplitude:long_name = "radar backscatter amplitude" ;
                backscatter_amplitude:units = "1" ;
                backscatter_amplitude:azimuth_regularization = "nearest_neighbor" ;
                backscatter_amplitude:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). Rays recorded at irregular azimuths were regularized onto the azimuth grid by nearest-neighbor selection." ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 54.1826 ;
                :geospatial_lat_min = 54.1826 ;
                :geospatial_lon_max = 7.8853 ;
                :geospatial_lon_min = 7.8853 ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ;
                :product_type = "radar_polar_regularized" ;
                :summary = "Marine X-band radar backscatter images from a fixed platform, mapped onto regular range and azimuth axes in the polar coordinates of the radar." ;
                :time_coverage_end = "2023-08-31T17:00:59Z" ;
                :time_coverage_start = "2023-08-31T17:00:00Z" ;
                :title = "Marine X-band radar polar images from a fixed platform" ;
data:
        latitude = 54.1826 ;
        longitude = 7.8853 ;
        altitude = 43. ;
        platform_type = "fixed" ;
}
```

## Example for a moving platform

A radar on a ship, with position and heading recorded per sweep, along with the optional [`radar_parameters`](../../metadata_attributes/radar_parameters.md#example) and [`georeference_correction`](../../metadata_attributes/georeference_correction.md#example) groups, whose contents are shown on their own pages.

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
                azimuth:comment = "clockwise positive, relative to the radar's zero direction, not north-oriented" ;
        float range(range) ;
                range:units = "m" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ;
                range:meters_to_center_of_first_gate = 3.75f ;
                range:meters_between_gates = 7.5f ;
        float ray_time(azimuth) ;
                ray_time:units = "s" ;
                ray_time:long_name = "time of each ray after the start of the revolution" ;
        float backscatter_amplitude(time, azimuth, range) ;
                backscatter_amplitude:long_name = "radar backscatter amplitude" ;
                backscatter_amplitude:units = "1" ;
                backscatter_amplitude:azimuth_regularization = "nearest_neighbor" ;
                backscatter_amplitude:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). Rays recorded at irregular azimuths were regularized onto the azimuth grid by nearest-neighbor selection." ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 14.9958976192 ;
                :geospatial_lat_min = 14.99471 ;
                :geospatial_lon_max = 145.86898 ;
                :geospatial_lon_min = 145.8672647679 ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ;
                :platform_is_mobile = "true" ;
                :product_type = "radar_polar_regularized" ;
                :summary = "Marine X-band radar backscatter images recorded on board R/V Ocean Research, mapped onto regular range and azimuth axes in the polar coordinates of the radar." ;
                :time_coverage_end = "2025-01-15T11:00:59Z" ;
                :time_coverage_start = "2025-01-15T11:00:00Z" ;
                :title = "Marine X-band radar polar images from R/V Ocean Research" ;
data:
        altitude = 18.5 ;
        platform_type = "ship" ;

group: radar_parameters { ... } // as in the example under Radar parameters
group: georeference_correction { ... } // as in the example under Georeference correction parameters
}
```

If the position and heading are given per ray instead, the variables have the dimensions `(time, azimuth)`:

```
// excerpt: only the variables that differ
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
