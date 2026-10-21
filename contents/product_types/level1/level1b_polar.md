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

The scalar variable `altitude` in the root group is required for all platforms (fixed and moving), as at [Level 1a](level1a.md#root-group); it gives the height of the radar antenna above mean sea level and is assumed constant.
For a fixed platform, scalar `latitude` and `longitude` in the root group give the antenna position, as at [Level 1a](level1a.md#root-group).

For a moving platform, the position and heading of the platform should be stored in the root group using the variable names and units of CfRadial 2.1 (Section 5.4). As at Level 1a, they can be given in one of two ways:

- **Per sweep.** The variables have the dimension `(time)` and give the values at the start of each revolution (image).
- **Per ray.** The variables have the dimensions `(time, azimuth)` and give the values for every ray (azimuth bin).

| Variable | Values | Description |
|---|---|---|
| `latitude`<br><small>[CfRadial 2.1](https://github.com/NCAR/CfRadial/tree/master/docs), Section 5.4</small> | double `(time)` or `(time, azimuth)`; `degrees_north` | Recommended for a moving platform. Recorded latitude (WGS 84). |
| `longitude`<br><small>[CfRadial 2.1](https://github.com/NCAR/CfRadial/tree/master/docs), Section 5.4</small> | double `(time)` or `(time, azimuth)`; `degrees_east` | Recommended for a moving platform. Recorded longitude (WGS 84). |
| `heading`<br><small>[CfRadial 2.1](https://github.com/NCAR/CfRadial/tree/master/docs), Section 5.4</small> | float `(time)` or `(time, azimuth)`; `degree` | Recommended for a moving platform. Heading of the platform relative to true north. |
{: .variable-table }

As at [Level 1a](level1a.md#moving-platforms), position and heading are recommended rather than required, since they may not be available when the file is written or may be taken from a separate navigation data stream; a file without them is not georeferenced until navigation data are matched to its images by `time`, and the attributes `source` and `sampling_frequency` may describe the navigation variables where they are present.

As at Level 1a, `latitude` and `longitude` are stored as recorded, and the optional [`georeference_correction` group](../../metadata_attributes/georeference_correction.md) gives the known offsets of azimuth, range, time, and antenna position.

## Radar parameters

Like Level 1a, constant technical parameters of the radar antenna, pulse, and scan can be stored in an optional root-level group named [`radar_parameters`](../../metadata_attributes/radar_parameters.md). When pulse or scan parameters (such as `prt` or `scan_rate`) vary over time, they are stored in the root group instead, with dimension `time` (varying per revolution) or `(time, azimuth)` (varying per ray).

## Examples

Complete example files, from a radar on a fixed platform and from one on a ship, are given in the annex under [Polar image sequences (L1b)](../../annex/level1b_polar.md).

### Navigation per ray

If the position and heading of a moving platform are given per ray instead of per sweep, the variables have the dimensions `(time, azimuth)`:

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
