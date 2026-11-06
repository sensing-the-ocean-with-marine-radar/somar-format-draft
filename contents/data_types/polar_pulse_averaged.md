---
title: polar_pulse_averaged (L1b)
layout: default
parent: SOMaR data types
nav_order: 2
---

# polar_pulse_averaged (L1b)

Files of the data type `polar_pulse_averaged` hold Level 1b pulse-averaged data, derived from [`polar_raw`](polar_raw.md) data: each stored ray is the mean of a block of consecutive pulses of a sweep, and keeps its own time and azimuth.
They keep the sweeps of `polar_raw`, with the sampling in time reduced by the averaging, and each sweep is one revolution or one dwell.
Pulse averaging is mainly used in pointing mode, in which the antenna is held at a fixed direction, but is also allowed for a rotating antenna; rotating data whose revolutions are mapped onto a regular azimuth axis, which may itself average the rays within each azimuth bin, are stored as [`polar_image_cube`](polar_image_cube.md) instead.
The annex gives a complete [example](../annex/level1b_pointing.md#example).

A file has the following structure, with the groups ending in `/`, the main variables of each group, and alternatives separated by `|`; parentheses after variables give their dimensions, and a label ending in a colon, such as "moving platform:", names the files in which the variables after it occur. The sections below define each item.

```text
/                              latitude, longitude, altitude
├── radar_parameters/          optional
├── georeference_correction/   optional
└── sweep_<n>/                 time, time_bounds, range, azimuth, sweep_mode, fixed_angle,
    │                          n_samples, backscatter_amplitude | backscatter_power (time, range)
    └── georeference/          moving platform: latitude, longitude, heading, roll, pitch,
                                                per sweep, or per ray (time)
```

## Structure

A file is organized in sweeps as a [`polar_raw`](polar_raw.md#sweeps) file is, with the same root group, `sweep_<n>` groups, `georeference` subgroups, and optional groups, and follows the definitions of `polar_raw` for the [relation to FM 301 and CfRadial](polar_raw.md#relation-to-fm-301-and-cfradial), the attributes of `range` (see [Coordinates and position](polar_raw.md#coordinates-and-position)), the [data variable](polar_raw.md#data-variable), and the [radar parameters](polar_raw.md#radar-parameters).
A block never spans the boundary of a sweep, so the last ray of a sweep may be the mean of fewer pulses than the others.

The data variable, [`backscatter_amplitude`](product_variables.md#backscatter_amplitude) or [`backscatter_power`](product_variables.md#backscatter_power), is required, and a file holds exactly one of the two.
It carries `cell_methods = "time: mean"` and [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity), which states whether the pulses are averaged in power, in amplitude, or as stored.

## Root group and navigation

### Root group

The root group locates the radar antenna:

| Variable | Values | Description |
|---|---|---|
| `latitude`<br><small>[FM 301][fm301], Table 301-4a</small> | double; `degrees_north` | Required for a fixed platform; recommended for a moving platform. Latitude of the radar antenna (WGS 84); from a moving platform, the recorded position at the start of the file. |
| `longitude`<br><small>[FM 301][fm301], Table 301-4a</small> | double; `degrees_east` | Required for a fixed platform; recommended for a moving platform. Longitude of the radar antenna (WGS 84); from a moving platform, the recorded position at the start of the file. |
| `altitude`<br><small>[FM 301][fm301], Table 301-4a</small> | double; `m` | Required. Height of the radar antenna above mean sea level. |
{: .variable-table }

### Navigation

From a moving platform, the `georeference` subgroup of each sweep group records the position and heading of the platform per sweep or per ray, as in [`polar_raw`](polar_raw.md#moving-platforms):

| Variable | Values | Description |
|---|---|---|
| `latitude`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | double, per sweep or per ray; `degrees_north` | Recommended for a moving platform. Recorded latitude (WGS 84). |
| `longitude`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | double, per sweep or per ray; `degrees_east` | Recommended for a moving platform. Recorded longitude (WGS 84). |
| `heading`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | float, per sweep or per ray; `degree` | Recommended for a moving platform. Heading of the platform relative to true north, with the standard name `platform_orientation`. |
| `roll`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | float, per sweep or per ray; `degree` | Optional. Roll of the platform about its longitudinal axis, positive with the port side up, i.e. the starboard side down, with the standard name `platform_roll_starboard_down`. |
| `pitch`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | float, per sweep or per ray; `degree` | Optional. Pitch of the platform about its lateral axis, positive with the bow up, with the standard name `platform_pitch_fore_up`. |
{: .variable-table }

## Averaged sweep groups

An averaged sweep group holds the data variable and the following variables.

| Variable | Values | Description |
|---|---|---|
| `time`<br><small>[FM 301][fm301], Table 301-6a</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Mean time of the pulses averaged into each ray, as UNIX time. Carries `bounds = "time_bounds"` where `time_bounds` is present. |
| `time_bounds`<br><small>CF</small> | double `(time, nv)`; `seconds since 1970-01-01T00:00:00Z` | Optional. Time of the first and the last pulse averaged into each ray, along the dimension `nv` of size 2 (CF section 7.1). |
| `range`<br><small>[FM 301][fm301], Table 301-6a</small> | float `(range)`; `m` | Required. Slant range from the antenna to the center of each range bin. |
| `azimuth`<br><small>[FM 301][fm301], Table 301-7a</small> | float `(time)`; `degree` | Required. Circular mean of the recorded pointing directions of the averaged pulses, i.e. the direction of the mean of their unit vectors, so that a dwell near 0° is averaged correctly; clockwise positive, relative to the radar's zero direction (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)). |
| `sweep_mode`<br><small>[FM 301][fm301], Tables 301-7a, 301-15</small> | string; `"azimuth_surveillance"` or `"pointing"` | Required. Whether the sweep is a full revolution or a dwell at a fixed direction. |
| `fixed_angle`<br><small>[FM 301][fm301], Table 301-7a</small> | float; `degree` | Required if `sweep_mode` is `"pointing"`; omitted otherwise. Nominal pointing direction of the antenna, clockwise positive, in the same reference as `azimuth`. |
| `n_samples`<br><small>[FM 301][fm301], Table 301-8a</small> | int, or int `(time)` | Required. Total number of pulses averaged into each ray, including any averaging done by the radar itself: the `n_samples` of the `polar_raw` data times the number of their rays in each block. With the dimension `time` where it varies, such as at the end of a sweep. It is stored in each sweep group, as in FM 301, and not in the [`radar_parameters`](../metadata_attributes/radar_parameters.md) group. |
{: .variable-table }

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
