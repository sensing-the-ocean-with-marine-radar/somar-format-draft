---
title: Radar "raw" data (L1a)
layout: default
parent: "Level 1: Radar data"
grand_parent: SOMaR product types
nav_order: 1
---

# L1a: "raw" radar data

Level 1a polar radar "raw" data (`radar_polar_raw`) are the lowest SOMaR level: the radar recording as delivered by the instrument (Level 0), converted from the manufacturer's container into NetCDF and otherwise unmodified.
Every ray is kept, indexed by time and range, with no interpolation, pulse averaging, or calibration.
The data are therefore still "raw", but no longer tied to the often proprietary containers of individual manufacturers, which makes them interoperable across radar systems.

## Relation to FM 301 and CfRadial

Radar data in polar coordinates already have an international standard, the WMO-CF Radial profile [FM 301][fm301] of the WMO Manual on Codes, which was developed for weather radars from the earlier [CfRadial format][cfradial].
Rather than define its own structure and vocabulary, SOMaR Level 1a draws on these documents in the following order:

1. **FM 301** is followed wherever it defines what a marine radar needs: the organization of a file in sweeps, and the names, types, and attributes of the variables. Note that FM 301 refers to radar data in polar coordinates as "Level 2" data; in SOMaR they are Level 1a.
2. **CfRadial 2.1** (draft of 2019) is followed for the parameters of moving platforms and for corrections to the recorded azimuth and range. FM 301 does not support moving platforms and omits these parts of CfRadial.
3. **SOMaR** defines what neither document covers.

SOMaR departs from FM 301 in the following points:

- Units are written as UDUNITS symbols (`m`, `degree`, `s`) rather than `metres`, `degrees`, and `seconds`.
- `azimuth` is stored relative to the radar's zero direction rather than true north (see [Georeferencing](../../georeferencing/index.md#polar-sensor-coordinates)).
- `altitude` carries the CF standard name `altitude` (height above the geoid, i.e. approximately mean sea level), which matches its FM 301 description; FM 301 Table 301-4b gives `height_above_reference_ellipsoid`.
- Variables that a horizontally scanning marine radar does not need are omitted, among them several that FM 301 makes mandatory: `elevation`, `sweep_number`, `follow_mode`, and `prt_mode` in the sweep groups (Table 301-7), and `volume_number`, `instrument_type`, and `platform_type` in the root group (Table 301-4). Whether the platform moves, and thus whether its position and heading are recorded for every sweep or ray, is stated by the global attribute `platform_is_mobile` instead; the global attributes `platform` and `source` describe the platform in words. The `standard_name` and `axis` attributes of `range` (Table 301-6) are not required.
- The root-group variables `time_coverage_start` and `time_coverage_end` (Table 301-4) are omitted. The times they hold, those of the first and last ray in the file, are given instead by the ACDD global attributes of the same names, which CfRadial 2.1 also defines as copies of these variables (Section 4.1).
- `fixed_angle` is present only in pointing sweeps, where it holds the nominal azimuth in the same reference as `azimuth`. FM 301 makes it mandatory in all sweeps and defines it as the elevation angle in most sweep modes (Table 301-7).

## File structure

A Level 1a file is organized in sweeps, as in FM 301.
A sweep comprises the rays of one antenna revolution.
For a radar in pointing mode, whose antenna is held at a fixed direction, a sweep is one dwell: an unbroken sequence of rays at that direction, in line with FM 301, where a sweep is a subset of the data "over which certain fundamental conditions remain constant" (301.2.1.2), and CfRadial 2.1, where a pointing sweep is "a sequence of rays over some time period, at fixed azimuth and elevation" (Section 2).
A new sweep starts when the direction changes or the recording is interrupted, so a file from an antenna that stays at one direction throughout holds a single sweep.

- The **root group** holds the global attributes and the variables that apply to the whole file.
- Each sweep is stored in a group named **`sweep_<n>`**, where `<n>` is the number of the sweep, starting at 0 and increasing in the order of acquisition.
- For a moving platform, each sweep group has a subgroup named **`georeference`**.
- The optional group **`radar_parameters`** is described under [Radar parameters](../../metadata_attributes/radar_parameters.md); the optional group **`georeference_correction`** is described under [Georeference correction parameters](../../metadata_attributes/georeference_correction.md). Both are located in the root group.

## Root group

| Variable | Values | Description |
|---|---|---|
| `latitude`<br><small>[FM 301][fm301], Table 301-4</small> | double; `degrees_north` | Required for a fixed platform, recommended for a moving one (see [Moving platforms](#moving-platforms)). Latitude of the radar antenna (WGS 84). For a moving platform, the recorded latitude at the start of the file (see [Georeferencing](../../georeferencing/index.md#polar-sensor-coordinates)). |
| `longitude`<br><small>[FM 301][fm301], Table 301-4</small> | double; `degrees_east` | Required for a fixed platform, recommended for a moving one (see [Moving platforms](#moving-platforms)). Longitude of the radar antenna (WGS 84). For a moving platform, the recorded longitude at the start of the file (see [Georeferencing](../../georeferencing/index.md#polar-sensor-coordinates)). |
| `altitude`<br><small>[FM 301][fm301], Table 301-4</small> | double; `m` | Required. Height of the radar antenna above mean sea level; needed to convert slant range to ground range (see [Georeferencing](../../georeferencing/index.md#applying-georeference-corrections)). |
{: .variable-table }

Whether the platform moves is stated by the global attribute [`platform_is_mobile`](../../metadata_attributes/optional_global.md).

## Sweep groups

The primary dimension of a sweep is `time`, with one entry per ray (e.g. 4500 entries for a 1.5 s sweep at 3000 Hz PRF).
The secondary dimension is `range`.
A sweep group holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `time`<br><small>[FM 301][fm301], Table 301-6</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Time of each ray, as UNIX time. |
| `range`<br><small>[FM 301][fm301], Table 301-6</small> | float `(range)`; `m` | Required. Slant range from the antenna to the center of each range bin. |
| `azimuth`<br><small>[FM 301][fm301], Table 301-7</small> | float `(time)`; `degree` | Required. Antenna pointing direction of each ray, clockwise positive, as recorded by the radar (see [Georeferencing](../../georeferencing/index.md#polar-sensor-coordinates)). |
| `sweep_mode`<br><small>[FM 301][fm301], Tables 301-7, 301-15</small> | string; `"azimuth_surveillance"` or `"pointing"` | Optional. Whether the sweep is a full revolution or a dwell at a fixed direction. Assumed `"azimuth_surveillance"` if missing. |
| `fixed_angle`<br><small>[FM 301][fm301], Table 301-7</small> | float; `degree` | Required if `sweep_mode` is `"pointing"`, otherwise omitted. Nominal pointing direction of the antenna, clockwise positive, in the same reference as `azimuth`. The per-ray `azimuth` is still stored as recorded, since a fixed antenna may jitter or drift. |
{: .variable-table }

The `range` variable carries the following attributes.

| Attribute | Values | Description |
|---|---|---|
| `meters_between_gates`<br><small>[FM 301][fm301], Table 301-6</small> | Number; m | Optional. The spacing of the range bins, which also follows from the `range` values. |
| `meters_to_center_of_first_gate`<br><small>[FM 301][fm301], Table 301-6</small> | Number; m | Optional. The range to the center of the first range bin. |
| `spacing_is_constant`<br><small>[FM 301][fm301], Table 301-6</small> | String; `true` or `false` | Optional. Whether the range bins are equally spaced. |
{: .attribute-table }

Parameters describing the radar, pulse, and scan are typically kept constant and stored in the `radar_parameters` group in the root group (see [Radar parameters](../../metadata_attributes/radar_parameters.md)). Where they vary from sweep to sweep or from ray to ray, they are stored as variables in the sweep groups instead; where they vary from ray to ray, they carry the dimension `time`.

### Data variables

The radar measurement is stored in each sweep group in a variable with the dimensions `(time, range)` (FM 301, regulation 301.4.6 and Table 301-10).
Its name is fixed by SOMaR and are the same at Level 1b ([polar](level1b_polar.md) and [Cartesian](level1b_cartesian.md)), so that the name identifies the quantity.
A file holds exactly one of the following variables; since power is the square of amplitude, storing both would duplicate the data.

| Variable | Values | Description |
|---|---|---|
| `backscatter_amplitude`<br><small>SOMaR</small> | `(time, range)`; `1` or `dB` | Backscatter amplitude, e.g. the square root of (I^2 + Q^2) or the video signal of the radar, in uncalibrated analog-to-digital converter units. |
| `backscatter_power`<br><small>SOMaR</small> | `(time, range)`; `1` or `dB` | Backscatter power, e.g. (I^2 + Q^2), in uncalibrated analog-to-digital converter units. |
{: .variable-table }

The FM 301 field names (Table 301-10) are not used, since they denote calibrated moments of weather radars.
The data are stored in the units of the radar's analog-to-digital converters, using the attributes `scale_factor`, `add_offset`, and `_FillValue`.
The `coordinates` attribute is set to `"azimuth range"`.
The `units` attribute must be `"1"` or `"dB"` to indicate linear or logarithmic dimensionless units, as FM 301 also uses `dB` for logarithmic quantities.
The `comment` attribute should describe how the values were derived from the radar signal (see the [example](#example)).

{: .open_issue }
<a id="coherent-data"></a>Only backscatter amplitude and power are specified, here and at Level 1b ([polar](level1b_polar.md) and [Cartesian](level1b_cartesian.md)). Coherent radars also record in-phase and quadrature (I/Q) data, phase, or radial Doppler velocity (FM 301 `VRAD`), for which no variable names are defined yet at either level; they are to be added to the table above.

## Moving platforms

When `platform_is_mobile` is `"true"`, each sweep group should have a subgroup named `georeference` that holds the position and heading of the platform (CfRadial 2.1, Section 5.4), given either per sweep (scalar) or per ray (dimension `time`); see [Georeferencing](../../georeferencing/index.md#polar-sensor-coordinates).

| Variable | Values | Description |
|---|---|---|
| `latitude`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | double; `degrees_north` | Recommended for a moving platform. Recorded latitude (WGS 84). |
| `longitude`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | double; `degrees_east` | Recommended for a moving platform. Recorded longitude (WGS 84). |
| `heading`<br><small>[CfRadial 2.1][cfradial], Section 5.4</small> | float; `degree` | Recommended for a moving platform. Heading of the platform relative to true north. |
{: .variable-table }

Position and heading are recommended rather than required, since a recording system may not receive them in real time, or a producer may prefer to take them from a separate navigation data stream.
A file without them is not georeferenced: its azimuths remain relative to the radar's zero direction, and its rays cannot be located until navigation data are matched to them by `time`.
`platform_is_mobile` is still `"true"` in such a file, so that readers know that navigation is needed, and the navigation variables can be added to the file later.

Where navigation variables are present, their attributes [`source`](../../metadata_attributes/variable_attributes.md#data-and-coordinate-variables) and [`sampling_frequency`](../../metadata_attributes/variable_attributes.md#data-and-coordinate-variables) may name the instrument they are taken from, such as a GNSS receiver or a gyrocompass, and the frequency at which it sampled them.

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

A radar on a ship, with the position and heading of the ship at the start of each sweep, the instruments they are taken from, and the [`radar_parameters`](../../metadata_attributes/radar_parameters.md#example) and [`georeference_correction`](../../metadata_attributes/georeference_correction.md#example) groups, whose contents are shown on their own pages.

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
                latitude:source = "GNSS receiver" ; // optional
                latitude:sampling_frequency = 10. ; // optional
        double longitude ;
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of GPS antenna at the start of the sweep" ;
                longitude:source = "GNSS receiver" ; // optional
                longitude:sampling_frequency = 10. ; // optional
        float heading ;
                heading:units = "degree" ;
                heading:standard_name = "platform_orientation" ;
                heading:long_name = "heading of the platform relative to true north at the start of the sweep" ;
                heading:source = "gyrocompass" ; // optional
                heading:sampling_frequency = 1. ; // optional
    } // group georeference
  } // group sweep_0

// ... additional sweep_<n> groups follow the same layout, one per sweep ...

group: radar_parameters { ... } // optional; as in the example under Radar parameters
group: georeference_correction { ... } // optional; as in the example under Georeference correction parameters
}
```

If the position and heading are given per ray instead, the variables of the `georeference` subgroup have the dimension `time`:

```
// excerpt: only the variables that differ
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

## Example for pointing mode

A radar in pointing mode stores the same sweep variables, with `sweep_mode` set to `"pointing"` and the nominal direction in `fixed_angle`:

```
// excerpt: only the variables that differ
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

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
