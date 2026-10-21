---
title: Polar products
layout: default
parent: SOMaR product types
nav_order: 1
---

# Polar products

Polar products store the radar measurement in the polar coordinates of the sensor, `range` and `azimuth`, with the radar antenna at the origin (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)).
They are the Level 1 products that keep the measurement in the geometry in which it was recorded, in the uncalibrated units of the instrument:

- **Level 1a "raw" data** (`radar_polar_raw`) are the lowest SOMaR level: the radar recording as delivered by the instrument (Level 0), converted from the manufacturer's container into NetCDF and otherwise unmodified. Every ray is kept, indexed by time and range, with no interpolation, pulse averaging, or calibration. The data are therefore still "raw", but no longer tied to the often proprietary containers of individual manufacturers, which makes them interoperable across radar systems.
- **Level 1b polar image sequences** (`radar_polar_regularized`) remain in the polar coordinates of the sensor but are mapped onto a regular range and azimuth axis, so that all images of a sequence share the same grid. They are usually derived from Level 1a data, and each image is one complete antenna revolution, corresponding to one Level 1a sweep.

Level 1a data are stored as [sweeps](#sweeps), Level 1b polar images as an [image cube](#image-cube).
What both forms share is described first; the products and their variables are listed under [Product types](#product-types).

## Relation to FM 301 and CfRadial

Radar data in polar coordinates already have an international standard, the WMO-CF Radial profile [FM 301][fm301] of the WMO Manual on Codes, which was developed for weather radars from the earlier [CfRadial format][cfradial].
Rather than define its own structure and vocabulary, SOMaR draws on these documents in the following order:

1. **FM 301** is followed wherever it defines what a marine radar needs: the organization of a file in sweeps, and the names, types, and attributes of the variables. Note that FM 301 refers to radar data in polar coordinates as "Level 2" data; in SOMaR they are Level 1a.
2. **CfRadial 2.1** (draft of 2019) is followed for the parameters of moving platforms and for corrections to the recorded azimuth and range. FM 301 does not support moving platforms and omits these parts of CfRadial.
3. **SOMaR** defines what neither document covers, such as the image cube of Level 1b, which has no equivalent in FM 301, since FM 301 keeps the individual rays of each sweep.

SOMaR departs from FM 301 in the following points:

- Units are written as UDUNITS symbols (`m`, `degree`, `s`) rather than `metres`, `degrees`, and `seconds`.
- `azimuth` is stored relative to the radar's zero direction rather than true north (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)).
- `altitude` carries the CF standard name `altitude` (height above the geoid, i.e. approximately mean sea level), which matches its FM 301 description; FM 301 Table 301-4b gives `height_above_reference_ellipsoid`.
- Variables that a horizontally scanning marine radar does not need are omitted, among them several that FM 301 makes mandatory: `elevation`, `sweep_number`, `follow_mode`, and `prt_mode` in the sweep groups (Table 301-7), and `volume_number`, `instrument_type`, and `platform_type` in the root group (Table 301-4). Whether the platform moves, and thus whether its position and heading are recorded for every sweep or ray, is stated by the global attribute `platform_is_mobile` instead; the global attributes `platform` and `source` describe the platform in words. The `standard_name` and `axis` attributes of `range` (Table 301-6) are not required.
- The root-group variables `time_coverage_start` and `time_coverage_end` (Table 301-4) are omitted. The times they hold, those of the first and last ray in the file, are given instead by the ACDD global attributes of the same names, which CfRadial 2.1 also defines as copies of these variables (Section 4.1).
- `fixed_angle` is present only in pointing sweeps, where it holds the nominal azimuth in the same reference as `azimuth`. FM 301 makes it mandatory in all sweeps and defines it as the elevation angle in most sweep modes (Table 301-7).

## Coordinates and position

`range` is the slant range from the antenna to the center of each range bin, and `azimuth` the antenna pointing direction, clockwise positive, as recorded by the radar relative to its zero direction; it is related to true north through the platform `heading` and the `azimuth_correction` (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)).
In both forms, the `range` variable may carry the following attributes.

| Attribute | Values | Description |
|---|---|---|
| `meters_between_gates`<br><small>[FM 301][fm301], Table 301-6</small> | Number; m | Optional. The spacing of the range bins, which also follows from the `range` values. |
| `meters_to_center_of_first_gate`<br><small>[FM 301][fm301], Table 301-6</small> | Number; m | Optional. The range to the center of the first range bin. |
| `spacing_is_constant`<br><small>[FM 301][fm301], Table 301-6</small> | String; `true` or `false` | Optional. Whether the range bins are equally spaced. |
{: .attribute-table }

The root group locates the radar antenna:

| Variable | Values | Description |
|---|---|---|
| `latitude`<br><small>[FM 301][fm301], Table 301-4</small> | double; `degrees_north` | Required for a fixed platform. Latitude of the radar antenna (WGS 84). For a moving platform, see [Moving platforms](#moving-platforms). |
| `longitude`<br><small>[FM 301][fm301], Table 301-4</small> | double; `degrees_east` | Required for a fixed platform. Longitude of the radar antenna (WGS 84). For a moving platform, see [Moving platforms](#moving-platforms). |
| `altitude`<br><small>[FM 301][fm301], Table 301-4</small> | double; `m` | Required. Height of the radar antenna above mean sea level, assumed constant for fixed and moving platforms; needed to convert slant range to ground range (see [Georeferencing](../georeferencing/index.md#applying-georeference-corrections)). |
{: .variable-table }

Whether the platform moves is stated by the global attribute [`platform_is_mobile`](../metadata_attributes/optional_global.md).
The positions and directions are stored as recorded, and the optional [`georeference_correction` group](../metadata_attributes/georeference_correction.md) in the root group gives the known offsets of azimuth, range, time, and antenna position.

## Data variables

The radar measurement is stored in one data variable, [`backscatter_amplitude` or `backscatter_power`](../metadata_attributes/product_variables.md), with the dimensions `(time, range)` in a sweep (FM 301, regulation 301.4.6 and Table 301-10) and `(time, azimuth, range)` in an image cube.
A file holds exactly one of the two.
Its `units` attribute is `"1"` or `"dB"`, as FM 301 also uses `dB` for logarithmic quantities, and in a sweep its `coordinates` attribute is `"azimuth range"`.
The `comment` attribute should describe how the values were derived from the radar signal (see the [example](../annex/level1a.md#example)).

{: .open_issue }
<a id="coherent-data"></a>Only backscatter amplitude and power are specified, for the polar products and for the [Cartesian images of Level 1b](gridded.md#image-cube-with-moving-origin). Coherent radars also record in-phase and quadrature (I/Q) data, phase, or radial Doppler velocity (FM 301 `VRAD`), for which no variable names are defined yet; they are to be added to the [product variables](../metadata_attributes/product_variables.md).

## Moving platforms

When `platform_is_mobile` is `"true"`, the position and heading of the platform should be recorded with the variable names and units of CfRadial 2.1 (Section 5.4), either per sweep or per ray (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)): in a `georeference` subgroup of each sweep group, scalar or with the dimension `time` (see [Sweeps](#sweeps)), or in the root group of an image cube, with the dimension `time` or `(time, azimuth)` (see [Image cube](#image-cube)).

| Variable | Values | Description |
|---|---|---|
| `latitude`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | double, per sweep or per ray; `degrees_north` | Recommended for a moving platform. Recorded latitude (WGS 84). |
| `longitude`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | double, per sweep or per ray; `degrees_east` | Recommended for a moving platform. Recorded longitude (WGS 84). |
| `heading`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | float, per sweep or per ray; `degree` | Recommended for a moving platform. Heading of the platform relative to true north. |
{: .variable-table }

Position and heading are recommended rather than required, since a recording system may not receive them in real time, or a producer may prefer to take them from a separate navigation data stream.
A file without them is not georeferenced: its azimuths remain relative to the radar's zero direction, and its rays cannot be located until navigation data are matched to them by `time`.
`platform_is_mobile` is still `"true"` in such a file, so that readers know that navigation is needed, and the navigation variables can be added to the file later.

Where navigation variables are present, their attributes [`source`](../metadata_attributes/variable_attributes.md#data-and-coordinate-variables) and [`sampling_frequency`](../metadata_attributes/variable_attributes.md#data-and-coordinate-variables) may name the instrument they are taken from, such as a GNSS receiver or a gyrocompass, and the frequency at which it sampled them.

## Radar parameters

Parameters describing the radar antenna, pulse, and scan are typically kept constant and stored in the optional group [`radar_parameters`](../metadata_attributes/radar_parameters.md) in the root group.
Where they vary, they are stored as variables instead: in the sweep groups, with the dimension `time` where they vary from ray to ray, or in the root group of an image cube, with the dimension `time` where they vary per revolution or `(time, azimuth)` where they vary per ray.

## Sweeps

Level 1a data are organized in sweeps, as in FM 301.
A sweep comprises the rays of one antenna revolution.
For a radar in pointing mode, whose antenna is held at a fixed direction, a sweep is one dwell: an unbroken sequence of rays at that direction, in line with FM 301, where a sweep is a subset of the data "over which certain fundamental conditions remain constant" (301.2.1.2), and CfRadial 2.1, where a pointing sweep is "a sequence of rays over some time period, at fixed azimuth and elevation" (Section 2).
A new sweep starts when the direction changes or the recording is interrupted, so a file from an antenna that stays at one direction throughout holds a single sweep.

- The **root group** holds the global attributes and the variables that apply to the whole file. From a moving platform, its scalar `latitude` and `longitude`, which FM 301 requires, are recommended and give the recorded position at the start of the file.
- Each sweep is stored in a group named **`sweep_<n>`**, where `<n>` is the number of the sweep, starting at 0 and increasing in the order of acquisition.
- For a moving platform, each sweep group should have a subgroup named **`georeference`** that holds the position and heading of the platform (see [Moving platforms](#moving-platforms)).
- The optional groups **`radar_parameters`** and **`georeference_correction`** are located in the root group.

### Sweep groups

The primary dimension of a sweep is `time`, with one entry per ray (e.g. 4500 entries for a 1.5 s sweep at 3000 Hz PRF).
The secondary dimension is `range`.
A sweep group holds the data variable and the following variables.

| Variable | Values | Description |
|---|---|---|
| `time`<br><small>[FM 301][fm301], Table 301-6</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Time of each ray, as UNIX time. |
| `range`<br><small>[FM 301][fm301], Table 301-6</small> | float `(range)`; `m` | Required. Slant range from the antenna to the center of each range bin. |
| `azimuth`<br><small>[FM 301][fm301], Table 301-7</small> | float `(time)`; `degree` | Required. Antenna pointing direction of each ray, clockwise positive, as recorded by the radar (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)). |
| `sweep_mode`<br><small>[FM 301][fm301], Tables 301-7, 301-15</small> | string; `"azimuth_surveillance"` or `"pointing"` | Optional. Whether the sweep is a full revolution or a dwell at a fixed direction. Assumed `"azimuth_surveillance"` if missing. |
| `fixed_angle`<br><small>[FM 301][fm301], Table 301-7</small> | float; `degree` | Required if `sweep_mode` is `"pointing"`, otherwise omitted. Nominal pointing direction of the antenna, clockwise positive, in the same reference as `azimuth`. The per-ray `azimuth` is still stored as recorded, since a fixed antenna may jitter or drift. |
{: .variable-table }

If the position and heading of a moving platform are given per ray instead of per sweep, the variables of the `georeference` subgroup have the dimension `time`:

```
// excerpt: only the variables that differ from the example of a moving platform
  group: georeference { // recommended
    variables:
        double latitude(time) ;
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of GPS antenna" ;
        double longitude(time) ;
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of GPS antenna" ;
        float heading(time) ;
                heading:units = "degree" ;
                heading:standard_name = "platform_orientation" ;
                heading:long_name = "heading of the platform relative to true north" ;
    } // group georeference
```

A radar in pointing mode stores the same sweep variables, with `sweep_mode` set to `"pointing"` and the nominal direction in `fixed_angle`:

```
// excerpt: only the variables that differ from the example
group: sweep_0 {
  dimensions:
        time = 1800000 ; // number of rays in the dwell, e.g. 10 min at 3000 Hz PRF
        range = 1000 ; // number of range gates
  variables:
        string sweep_mode ; // optional
                sweep_mode:long_name = "sweep scan mode" ;
        float fixed_angle ;
                fixed_angle:units = "degree" ;
                fixed_angle:long_name = "nominal antenna pointing direction" ;
                fixed_angle:comment = "clockwise positive, relative to the radar's zero direction, not north-oriented" ;
  data:
        sweep_mode = "pointing" ;
        fixed_angle = 45. ;
  } // group sweep_0
```

## Image cube

Level 1b polar images are stored as a single three-dimensional cube in the root group: each time step is one complete antenna revolution, and the data variable has the dimensions `(time, azimuth, range)`.
Images are formed from revolutions and are not defined for data recorded in pointing mode, which exist at Level 1a only.
In addition to the [position and heading](#moving-platforms), the file holds the data variable and the following variables.

| Variable | Values | Description |
|---|---|---|
| `time`<br><small>[FM 301][fm301], Table 301-6</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each revolution. |
| `azimuth`<br><small>[FM 301][fm301], Table 301-7</small> | float `(azimuth)`; `degree` | Required. Regular azimuth axis, clockwise positive, relative to the radar's zero direction. |
| `range`<br><small>[FM 301][fm301], Table 301-6</small> | float `(range)`; `m` | Required. Slant range to the center of each range bin. |
{: .variable-table }

The regular azimuth axis and the resampling onto it are recorded in two attributes.

| Attribute | Values | Description |
|---|---|---|
| `azimuth_regularization`<br><small>SOMaR</small> | String; one of `nearest_neighbor`, `linear_interpolation`, `average` | On the data variable: the method used to resample rays recorded at irregular azimuths onto the regular `azimuth` axis: selection of the closest ray, linear interpolation between the two adjacent rays, or the mean of all rays falling within each azimuth bin. Interpolation and averaging are done on linear power: amplitude (`backscatter_amplitude`) is squared, and values in `dB` are converted to linear units, beforehand, and the result is converted back to the quantity and unit of the data variable. If the signal cannot be linearized, such as a log-compressed video signal, they are done on the stored values instead. Should be accompanied by a `comment` describing the method in words, which must also say when the stored values were used. |
| `rays_angle_resolution`<br><small>SOMaR</small> | Number; degree | On `azimuth`: the spacing of the regular azimuth axis. Named after the FM 301 variable `rays_angle_resolution` (Table 301-8), which gives the angular spacing of rays that are indexed to a regular grid; the accompanying FM 301 flag `rays_are_indexed` is implied to be `"true"` and is not stored. |
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

## Product types

The following products are polar products.
For each, the table lists the data variables that it requires, recommends, or allows, in addition to the variables above; they are defined under [Product variables](../metadata_attributes/product_variables.md).

| Product | `product_type` | Variables |
|---|---|---|
| [Radar "raw" data](../annex/level1a.md) (L1a) | `radar_polar_raw` | **Required:** `backscatter_amplitude`, `backscatter_power` |
| [Polar image sequences](../annex/level1b_polar.md) (L1b) | `radar_polar_regularized` | **Required:** `backscatter_amplitude`, `backscatter_power`<br>**Optional:** `ray_time` |
{: .product-type-table }

Of `backscatter_amplitude` and `backscatter_power`, a file holds exactly one.
Level 1a data take the form of [sweeps](#sweeps), Level 1b polar images that of an [image cube](#image-cube).

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
