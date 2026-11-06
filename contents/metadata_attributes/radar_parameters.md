---
title: Radar parameters
layout: default
parent: Metadata
nav_order: 6
---

# Radar parameters

SOMaR files describe the radar instrument in words through the global attributes [`instrument`](optional_global.md#instrument) and [`source`](optional_global.md#source).
The technical parameters of the radar are stored as variables.
SOMaR takes their names, meanings, and types from the WMO-CF Radial profile [FM 301][fm301] (see [Relation to FM 301 and CfRadial](../data_types/polar_raw.md#relation-to-fm-301-and-cfradial)), but not always their location in the file.

Constant technical parameters of the radar antenna, pulse, and scan are stored in a group named `radar_parameters` in the root group. The table below lists the variables that apply to marine radars, with the FM 301 table that defines each of them; all of them are optional. Only the beam widths are part of the FM 301 `radar_parameters` group (Table 301-12a). FM 301 stores the pulse and scan parameters per ray in each sweep group (Table 301-8a) and `frequency` as a sweep coordinate (Table 301-6a); collecting them as constants in `radar_parameters` is a SOMaR choice, since they rarely change for a marine radar.
The FM 301 `radar_calibration` group (Table 301-14a) is not adopted: its constants convert the received power of a weather radar into calibrated quantities such as reflectivity, whereas the backscatter of a marine radar is stored in uncalibrated units of its analog-to-digital converter, for which no such constants exist. A calibration of marine radar backscatter would be added as a group of its own.

| Variable | Values | Description |
|---|---|---|
| `beam_width_h`<br><small>[FM 301][fm301], Table 301-12a</small> | float; `degree` | Horizontal beam width of the antenna. |
| `beam_width_v`<br><small>[FM 301][fm301], Table 301-12a</small> | float; `degree` | Vertical beam width of the antenna. |
| `frequency`<br><small>[FM 301][fm301], Table 301-6a</small> | float; `s-1` | Operating frequency of the radar. Scalar in SOMaR; FM 301 defines a `frequency` dimension for multi-frequency radars. |
| `n_samples`<br><small>[FM 301][fm301], Table 301-8a</small> | int | Number of samples contributing to each ray. 1 at Level 1a unless the radar itself averages pulses. Not stored here for [pulse-averaged data](../data_types/polar_pulse_averaged.md), which require it in each sweep group. |
| `obstructed_sectors`<br><small>SOMaR</small> | float `(obstructed_sector, nv)`; `degree` | Start and end azimuth of each sector of the field of view that is obstructed or blanked, for example by platform superstructure (see [Obstructed sectors](#obstructed-sectors)). |
| `polarization_mode`<br><small>[FM 301][fm301], Tables 301-8a, 301-15</small> | string; `"horizontal"` or `"vertical"` | Antenna polarization (typically horizontal or vertical). |
| `prt`<br><small>[FM 301][fm301], Table 301-8a</small> | float; `s` | Pulse repetition time. |
| `pulse_width`<br><small>[FM 301][fm301], Table 301-8a</small> | float; `s` | Length of the transmitted pulse. |
| `scan_rate`<br><small>[FM 301][fm301], Table 301-8a</small> | float; `degree s-1` | Antenna rotation rate: positive for an antenna that rotates clockwise, seen from above, and negative for one that rotates counterclockwise, as in FM 301. The `azimuth` values are clockwise positive in either case. |
{: .variable-table }

When pulse or scan parameters vary, [Level 1a](../data_types/polar_raw.md#sweep-groups) and [Level 1b pulse-averaged data](../data_types/polar_pulse_averaged.md) store them in each sweep group (as scalars per sweep, or with dimension `time` per ray) and [Level 1b polar images](../data_types/polar_image_cube.md) store them in the root group with dimension `time` (per image) or `(time, azimuth)` (per ray).

## Obstructed sectors

Sectors of the field of view that are shadowed by platform superstructure or blanked by the radar are given by `obstructed_sectors`, with the start and end azimuth of each sector along the dimension `nv` (number of vertices, as in [CF][cf-bounds] section 7.1), of size 2.
Each sector runs clockwise from its start to its end azimuth and may wrap through 0°, e.g. from 350° to 5°.
The azimuths are given in the frame of `azimuth + azimuth_correction` (see [Applying georeference corrections](../georeferencing/index.md#applying-georeference-corrections)), i.e. relative to the bow on a ship and to true north on a fixed platform; unlike the `azimuth` of the polar data types, they do not depend on the radar's zero direction.
At Level 1b Cartesian and Level 2, grid cells and analysis windows that fall inside an obstructed sector hold the [`_FillValue`](variable_attributes.md#_FillValue).

## Example

```
group: radar_parameters {
  dimensions:
        obstructed_sector = 2 ;
        nv = 2 ;
  variables:
        float beam_width_h ; // optional
                beam_width_h:units = "degree" ;
                beam_width_h:long_name = "horizontal antenna beam width" ;
        float beam_width_v ; // optional
                beam_width_v:units = "degree" ;
                beam_width_v:long_name = "vertical antenna beam width" ;
        float frequency ; // optional
                frequency:units = "s-1" ;
                frequency:long_name = "operating frequency of the radar" ;
        string polarization_mode ; // optional
                polarization_mode:long_name = "antenna polarization mode" ;
        float pulse_width ; // optional
                pulse_width:units = "s" ;
                pulse_width:long_name = "length of the transmitted pulse" ;
        float prt ; // optional
                prt:units = "s" ;
                prt:long_name = "pulse repetition time" ;
        float scan_rate ; // optional
                scan_rate:units = "degree s-1" ;
                scan_rate:long_name = "antenna rotation rate" ;
        int n_samples ; // optional
                n_samples:long_name = "number of samples contributing to each ray" ;
        float obstructed_sectors(obstructed_sector, nv) ; // optional
                obstructed_sectors:units = "degree" ;
                obstructed_sectors:long_name = "start and end azimuth of obstructed sectors, clockwise, relative to the bow" ;
  data:
        beam_width_h = 0.95 ;
        beam_width_v = 20. ;
        frequency = 9.41e+09 ;
        polarization_mode = "horizontal" ;
        pulse_width = 5.e-08 ;
        prt = 3.33e-04 ;
        scan_rate = 240. ;
        n_samples = 1 ;
        obstructed_sectors = 160., 200., 350., 5. ;
  } // group radar_parameters
```

[cf-bounds]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#cell-boundaries
[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
