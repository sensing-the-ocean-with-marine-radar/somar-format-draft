---
title: Radar "raw" data (L1a)
layout: default
parent: Level 1 data
nav_order: 1
---

# L1a: "raw" radar data

Here we refer to Level 1a data, the lowest SOMaR level: the unmodified radar recording, converted from the manufacturer's container into NetCDF.
Every pulse is kept, indexed by time and range, with no interpolation, averaging, or calibration.

A SOMaR NetCDF file at Level 1a originates directly from the data recorded by the radar system used (Level 0).
It can therefore still be considered "raw" radar data, but stored as NetCDF rather than in the often proprietary radar data containers used by different manufacturers.
This ensures interoperability even when different radar systems are used.
No changes to the data, other than this format conversion, are allowed.
In particular, Level 1a products should contain all pulses without any interpolation or pulse averaging.

## Relation to FM 301 and CfRadial

Radar data in polar coordinates already have an international standard, the WMO-CF Radial profile [FM 301][fm301] of the WMO Manual on Codes, which was developed for weather radars from the earlier [CfRadial format][cfradial].
Rather than define its own structure and vocabulary, SOMaR Level 1a draws on these documents in the following order:

1. **FM 301** is followed wherever it defines what a marine radar needs: the organization of a file in sweeps, and the names, types, units, and attributes of the variables. To keep the format simple, Level 1a leaves out everything in FM 301 that is of no use for a marine radar. A Level 1a file is therefore not a conforming FM 301 file. Note that FM 301 refers to radar data in polar coordinates as "Level 2" data; in SOMaR they are Level 1a.
2. **CfRadial 2.1** (draft of 2019) is followed for the parameters of moving platforms and for corrections to the recorded azimuth and range. FM 301 does not support moving platforms and omits these parts of CfRadial.
3. **SOMaR** defines what neither document covers.

## File structure

A Level 1a file is organized in sweeps, as in FM 301.
A sweep comprises the pulses of one antenna revolution or, for a radar that scans a sector, of one pass over the sector.

- The **root group** holds the global attributes and the variables that apply to the whole file.
- Each sweep is stored in a group named **`sweep_<n>`**, where `<n>` is the number of the sweep, starting at 0 and increasing in the order of acquisition.
- For a moving platform, each sweep group has a subgroup named **`georeference`**.
- The optional groups **`radar_parameters`**, **`radar_calibration`**, and **`georeference_correction`** are located in the root group and described under [Radar parameters](../../metadata_attributes/radar_parameters.md).

## Root group

| Variable | Dimension | Type | Units | Defined by | Description |
|---|---|---|---|---|---|
| `latitude` | none | double | `degrees_north` | FM 301, Table 301-4 | Latitude of the radar antenna (WGS 84). For a moving platform, the latitude at the start of the file. |
| `longitude` | none | double | `degrees_east` | FM 301, Table 301-4 | Longitude of the radar antenna (WGS 84). For a moving platform, the longitude at the start of the file. |
| `altitude` | none | double | `metres` | FM 301, Table 301-4 | Height of the radar antenna above mean sea level. Needed to convert slant range to ground range. |
| `platform_type` | none | string | | FM 301, Tables 301-4 and 301-15 | `"fixed"` or `"ship"`. |

The global attribute `platform_is_mobile` states whether the platform moves (see [Moving platforms](#moving-platforms)).

## Sweep groups

The primary dimension of a sweep is `time`, with one entry per radar pulse; the secondary dimension is `range`.
The following variables are required in every sweep group.

| Variable | Dimension | Type | Units | Defined by | Description |
|---|---|---|---|---|---|
| `time` | `(time)` | double | `seconds since <reference time>` | FM 301, Table 301-6 | Time of each pulse. Should be given as UNIX time (`seconds since 1970-01-01T00:00:00Z`). |
| `range` | `(range)` | float | `metres` | FM 301, Table 301-6 | Slant range from the antenna to the center of each range bin. Carries the attributes `spacing_is_constant`, `meters_to_center_of_first_gate`, and `meters_between_gates`. |
| `azimuth` | `(time)` | float | `degrees` | FM 301, Table 301-7 | Antenna pointing direction of each pulse, clockwise positive, as recorded by the radar (see [Azimuth reference](#azimuth-reference)). |

The following variables are optional.

| Variable | Dimension | Type | Units | Defined by | Description |
|---|---|---|---|---|---|
| `sweep_mode` | none | string | | FM 301, Tables 301-7 and 301-15 | `"azimuth_surveillance"` for a full revolution or `"sector"` for a sector scan. Assumed `"azimuth_surveillance"` if missing. |
| `frequency` | `(frequency)` | float | `s-1` | FM 301, Table 301-6 | Operating frequency of the radar. |
| `polarization_mode` | none | string | | FM 301, Tables 301-8 and 301-15 | `"horizontal"` (HH) or `"vertical"` (VV). |
| `pulse_width` | `(time)` | float | `seconds` | FM 301, Table 301-8 | Length of the transmitted pulse. |
| `prt` | `(time)` | float | `seconds` | FM 301, Table 301-8 | Pulse repetition time. |
| `scan_rate` | `(time)` | float | `degrees/s` | FM 301, Table 301-8 | Antenna rotation rate. |
| `n_samples` | `(time)` | int | | FM 301, Table 301-8 | Number of samples contributing to each stored pulse. 1 at Level 1a unless the radar itself averages pulses. |

### Data variables

The radar measurement is stored in one or more variables with the dimensions `(time, range)` (FM 301, regulation 301.4.6 and Table 301-10).
The data are stored in the units of the radar's analog-to-digital converters, using the attributes `scale_factor`, `add_offset`, and `_FillValue`.
The `coordinates` attribute is set to `"azimuth range"`.
The `units` attribute must be `"1"` or `"dB"` to indicate linear or logarithmic dimensionless units, as FM 301 also uses `dB` for logarithmic quantities, and the `comment` attribute should state clearly whether the values refer to amplitude or power.
Where a radar provides one of the quantities that FM 301 lists in Table 301-9, such as the Doppler velocity measured by a coherent radar, the variable name given there should be used.

## Moving platforms

FM 301 requires the global attribute `platform_is_mobile` to be `"false"`.
SOMaR also allows `"true"`, for a radar on a ship; the attribute is assumed to be `"false"` if missing.

If `platform_is_mobile` is `"true"`, each sweep group has a subgroup named `georeference` that holds the position and attitude of the platform, with the variables defined in section 5.4 of CfRadial 2.1.
The variables can be given in one of two ways, which must be the same for all variables of the subgroup:

- **Per sweep.** The variables are scalar and give the values at the start of the sweep, i.e. at the time of its first pulse. This is the simpler option, and it matches the [Level 1b Cartesian images](level1b.md#cartesian-image-sequences-cart3d), whose grid origin is the radar position at the start of each revolution. It is a SOMaR addition; CfRadial defines the variables per pulse only.
- **Per pulse.** The variables have the dimension `(time)` of the sweep and give the values for every pulse, as in CfRadial. This option keeps the full resolution of the navigation data.

| Variable | Dimension | Type | Units | Description |
|---|---|---|---|---|
| `latitude` | none or `(time)` | double | `degrees_north` | Required. Latitude of the radar antenna (WGS 84). |
| `longitude` | none or `(time)` | double | `degrees_east` | Required. Longitude of the radar antenna (WGS 84). |
| `heading` | none or `(time)` | float | `degrees` | Required. Heading of the platform relative to true north. |
| `altitude` | none or `(time)` | double | `metres` | Optional. Height of the radar antenna above mean sea level. |
| `roll` | none or `(time)` | float | `degrees` | Optional. Roll about the longitudinal axis of the platform; positive is left side up, looking forward. |
| `pitch` | none or `(time)` | float | `degrees` | Optional. Pitch about the lateral axis of the platform; positive is up at the front. |
| `eastward_velocity` | none or `(time)` | float | `m/s` | Optional. Eastward velocity of the platform. |
| `northward_velocity` | none or `(time)` | float | `m/s` | Optional. Northward velocity of the platform. |

## Azimuth reference

FM 301 defines `azimuth` relative to true north.
At Level 1a, where the data must not be changed, `azimuth` is the antenna angle as recorded by the radar, relative to the radar's own zero direction; on a ship, this is typically the bow.
The azimuth relative to true north is obtained as

```
azimuth + azimuth_correction + heading
```

where `heading` is taken from the `georeference` subgroup and `azimuth_correction` from the optional [`georeference_correction` group](../../metadata_attributes/radar_parameters.md#the-georeference_correction-group); a missing variable counts as 0.
For a fixed platform, there is no `heading`, and `azimuth_correction` is the direction of the radar's zero direction relative to true north.

## Minimal example

A radar on a fixed platform.

```
netcdf or_2023-08-31-17-00_radar_raw {
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
                altitude:units = "metres" ;
                altitude:standard_name = "altitude" ;
                altitude:long_name = "height of radar antenna above mean sea level" ;
        string platform_type ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :title = "Bare minimum level 1a X-band radar data example" ;
                :source = "ground-based radar" ;
                :history = "20230831T170026Z: File creation time" ;
                :creator_name = "Dr. Famous Scientist" ;
                :creator_email = "famous.scientist@frori.org" ;
                :processing_level = "L1a" ;
                :platform_is_mobile = "false" ;
data:
        latitude = 54.1826 ;
        longitude = 7.8853 ;
        altitude = 43. ;
        platform_type = "fixed" ;

group: sweep_0 {
  dimensions:
        time = 986 ;
        range = 435 ;
  variables:
        double time(time) ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:calendar = "standard" ;
                time:standard_name = "time" ;
                time:long_name = "time of radar pulse" ;
        float range(range) ;
                range:units = "metres" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ;
                range:meters_to_center_of_first_gate = 3.75f ;
                range:meters_between_gates = 7.5f ;
        float azimuth(time) ;
                azimuth:units = "degrees" ;
                azimuth:long_name = "radar antenna pointing direction" ;
                azimuth:comment = "clockwise positive, relative to the radar's zero direction, not North-oriented" ;
        ushort polar_amp(time, range) ;
                polar_amp:scale_factor = 0.176738930567883 ;
                polar_amp:add_offset = 0. ;
                polar_amp:_FillValue = 65535US ;
                polar_amp:long_name = "radar_backscatter_amplitude" ;
                polar_amp:units = "1" ;
                polar_amp:coordinates = "azimuth range" ;
                polar_amp:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). I and Q are the in-phase and quadrature channels both measured in counts of the analog-to-digital-converter (ADC)." ;
  } // group sweep_0

// ... additional sweep_<n> groups follow the same layout, one per antenna revolution ...
}
```

## Example for a moving platform

A radar on a ship, with the position and heading of the ship at the start of each sweep, the pulse parameters, and the `radar_parameters` and `georeference_correction` groups.

```
netcdf or_2025-01-15-11-00_radar_raw {
variables:
        double latitude ;
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of radar antenna at the start of the file" ;
        double longitude ;
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of radar antenna at the start of the file" ;
        double altitude ;
                altitude:units = "metres" ;
                altitude:standard_name = "altitude" ;
                altitude:long_name = "height of radar antenna above mean sea level" ;
        string platform_type ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :title = "Level 1a marine X-band radar data from R/V Ocean Research" ;
                :source = "Shipboard marine X-band radar" ;
                :history = "20250115T120500Z: File creation time" ;
                :creator_name = "Dr. Famous Scientist" ;
                :creator_email = "famous.scientist@frori.org" ;
                :platform = "R/V Ocean Research" ;
                :instrument = "Helmholtz-Zentrum Hereon coherent-on-receive marine X-band radar" ;
                :processing_level = "L1a" ;
                :platform_is_mobile = "true" ;
data:
        latitude = 14.9952749946079 ;
        longitude = 145.868167860183 ;
        altitude = 18.5 ;
        platform_type = "ship" ;

group: sweep_0 {
  dimensions:
        time = 986 ;
        range = 435 ;
        frequency = 1 ;
  variables:
        double time(time) ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:calendar = "standard" ;
                time:standard_name = "time" ;
                time:long_name = "time of radar pulse" ;
        float range(range) ;
                range:units = "metres" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ;
                range:meters_to_center_of_first_gate = 3.75f ;
                range:meters_between_gates = 7.5f ;
        float frequency(frequency) ;
                frequency:units = "s-1" ;
                frequency:long_name = "operating frequency of the radar" ;
        float azimuth(time) ;
                azimuth:units = "degrees" ;
                azimuth:long_name = "radar antenna pointing direction" ;
                azimuth:comment = "clockwise positive, relative to the bow of the ship, not North-oriented" ;
        string sweep_mode ;
        string polarization_mode ;
        float pulse_width(time) ;
                pulse_width:units = "seconds" ;
                pulse_width:long_name = "length of the transmitted pulse" ;
        float prt(time) ;
                prt:units = "seconds" ;
                prt:long_name = "pulse repetition time" ;
        ushort polar_amp(time, range) ;
                polar_amp:scale_factor = 0.176738930567883 ;
                polar_amp:add_offset = 0. ;
                polar_amp:_FillValue = 65535US ;
                polar_amp:long_name = "radar_backscatter_amplitude" ;
                polar_amp:units = "1" ;
                polar_amp:coordinates = "azimuth range" ;
                polar_amp:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). I and Q are the in-phase and quadrature channels both measured in counts of the analog-to-digital-converter (ADC)." ;
  data:
        frequency = 9.41e+09 ;
        sweep_mode = "azimuth_surveillance" ;
        polarization_mode = "vertical" ;

  group: georeference {
    variables:
        double latitude ;
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of radar antenna at the start of the sweep" ;
        double longitude ;
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of radar antenna at the start of the sweep" ;
        float heading ;
                heading:units = "degrees" ;
                heading:standard_name = "platform_orientation" ;
                heading:long_name = "heading of the platform relative to true north at the start of the sweep" ;
    } // group georeference
  } // group sweep_0

// ... additional sweep_<n> groups follow the same layout, one per antenna revolution ...

group: radar_parameters {
  variables:
        float beam_width_h ;
                beam_width_h:units = "degrees" ;
                beam_width_h:long_name = "horizontal antenna beam width" ;
        float beam_width_v ;
                beam_width_v:units = "degrees" ;
                beam_width_v:long_name = "vertical antenna beam width" ;
        float receiver_bandwidth ;
                receiver_bandwidth:units = "s-1" ;
                receiver_bandwidth:long_name = "bandwidth of radar receiver" ;
  data:
        beam_width_h = 0.95 ;
        beam_width_v = 20. ;
        receiver_bandwidth = 2.e+07 ;
  } // group radar_parameters

group: georeference_correction {
  variables:
        float azimuth_correction ;
                azimuth_correction:units = "degrees" ;
                azimuth_correction:long_name = "correction to azimuth values" ;
        float range_correction ;
                range_correction:units = "metres" ;
                range_correction:long_name = "correction to range values" ;
  data:
        azimuth_correction = -1.3 ;
        range_correction = -22.5 ;
  } // group georeference_correction
}
```

If the position and heading are given per pulse instead, the variables of the `georeference` subgroup have the dimension `time`:

```
  group: georeference {
    variables:
        double latitude(time) ;
                latitude:units = "degrees_north" ;
                latitude:standard_name = "latitude" ;
                latitude:long_name = "latitude of radar antenna" ;
        double longitude(time) ;
                longitude:units = "degrees_east" ;
                longitude:standard_name = "longitude" ;
                longitude:long_name = "longitude of radar antenna" ;
        float heading(time) ;
                heading:units = "degrees" ;
                heading:standard_name = "platform_orientation" ;
                heading:long_name = "heading of the platform relative to true north" ;
    } // group georeference
```

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
