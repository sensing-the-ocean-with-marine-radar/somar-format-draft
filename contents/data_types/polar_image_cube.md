---
title: polar_image_cube (L1b)
layout: default
parent: SOMaR data types
nav_order: 3
---

# polar_image_cube (L1b)

Files of the data type `polar_image_cube` hold Level 1b polar image sequences: radar images that remain in the polar coordinates of the sensor but are mapped onto a regular range and azimuth axis, so that all images of a sequence share the same grid.
They are usually derived from [`polar_raw`](polar_raw.md) data, and each image is one complete antenna revolution, corresponding to one `polar_raw` sweep.
Images are formed from revolutions and are not defined for data recorded in pointing mode, which are stored as `polar_raw` and, averaged over pulses, as [`polar_pulse_averaged`](polar_pulse_averaged.md).
The annex gives a complete [example](../annex/level1b_polar.md#example).

## Image cube

The images are stored as a single three-dimensional cube in the root group: each time step is one complete antenna revolution, and the data variable, [`backscatter_amplitude`](product_variables.md#backscatter_amplitude) or [`backscatter_power`](product_variables.md#backscatter_power), has the dimensions `(time, azimuth, range)`.
The data variable is required, and a file holds exactly one of the two.
A file follows the definitions of `polar_raw` for the [relation to FM 301 and CfRadial](polar_raw.md#relation-to-fm-301-and-cfradial), the attributes of `range` (see [Coordinates and position](polar_raw.md#coordinates-and-position)), and the [data variable](polar_raw.md#data-variable).

Mapping a revolution onto the regular azimuth axis may itself average the rays within each azimuth bin (`azimuth_regularization = average`); rays averaged over consecutive pulses that keep their own azimuths are stored as `polar_pulse_averaged` instead.
The file holds the data variable and the following variables, all in the root group.

| Variable | Values | Description |
|---|---|---|
| `time`<br><small>[FM 301][fm301], Table 301-6a</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each revolution. |
| `azimuth`<br><small>[FM 301][fm301], Table 301-7a</small> | float `(azimuth)`; `degree` | Required. Regular azimuth axis, clockwise positive, relative to the radar's zero direction. |
| `range`<br><small>[FM 301][fm301], Table 301-6a</small> | float `(range)`; `m` | Required. Slant range to the center of each range bin. |
| `ray_time`<br><small>SOMaR</small> | float `(azimuth)`; `s` | Optional. Time of each ray after the start of its revolution (see [Product variables](product_variables.md#ray_time)). |
| `latitude`<br><small>[FM 301][fm301], Table 301-4a</small> | double, scalar, per revolution, or per ray; `degrees_north` | Required for a fixed platform; recommended for a moving platform. Latitude of the radar antenna (WGS 84): scalar from a fixed platform; from a moving platform, the recorded position with the dimension `time` per revolution or `(time, azimuth)` per ray. |
| `longitude`<br><small>[FM 301][fm301], Table 301-4a</small> | double, scalar, per revolution, or per ray; `degrees_east` | Required for a fixed platform; recommended for a moving platform. Longitude of the radar antenna (WGS 84), as `latitude`. |
| `altitude`<br><small>[FM 301][fm301], Table 301-4a</small> | double; `m` | Required. Height of the radar antenna above mean sea level. |
| `heading`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | float, per revolution or per ray; `degree` | Recommended for a moving platform. Heading of the platform relative to true north, with the dimension `time` per revolution or `(time, azimuth)` per ray. |
| `roll`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | float, per revolution or per ray; `degree` | Optional. Roll of the platform about its longitudinal axis, positive with the port side up, i.e. the starboard side down, with the standard name `platform_roll_starboard_down`. |
| `pitch`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | float, per revolution or per ray; `degree` | Optional. Pitch of the platform about its lateral axis, positive with the bow up, with the standard name `platform_pitch_fore_up`. |
{: .variable-table }

Where the parameters of the [`radar_parameters`](../metadata_attributes/radar_parameters.md) group vary, they are stored in the root group with the dimension `time` where they vary per revolution or `(time, azimuth)` where they vary per ray.

## Azimuth regularization

The regular azimuth axis and the resampling onto it are recorded in two attributes.

| Attribute | Values | Description |
|---|---|---|
| `azimuth_regularization`<br><small>SOMaR</small> | String; one of `nearest_neighbor`, `linear_interpolation`, `average` | Required. On the data variable: the method used to resample rays recorded at irregular azimuths onto the regular [`azimuth`](#azimuth) axis: selection of the closest ray, linear interpolation between the two adjacent rays, or the mean of all rays falling within each azimuth bin. Except for `nearest_neighbor`, the data variable also carries [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity), which states whether interpolation and averaging are done on power, amplitude, or the stored values. Should be accompanied by a [`comment`](../metadata_attributes/variable_attributes.md#comment) describing the method in words. |
| `rays_angle_resolution`<br><small>SOMaR</small> | Number; degree | Optional. On [`azimuth`](#azimuth): the spacing of the regular azimuth axis. Named after the FM 301 variable `rays_angle_resolution` (Table 301-8a), which gives the angular spacing of rays that are indexed to a regular grid; the accompanying FM 301 flag `rays_are_indexed` is implied to be `"true"` and is not stored. |
{: .attribute-table }

If the position and heading of a moving platform are given per ray instead of per revolution, the variables have the dimensions `(time, azimuth)`:

```
// excerpt: only the variables that differ from the example of a moving platform
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

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
