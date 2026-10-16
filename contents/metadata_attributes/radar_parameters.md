---
title: Radar parameters
layout: default
parent: Metadata
nav_order: 4
---

# Radar parameters

SOMaR files describe the radar instrument in words through the global attributes [`instrument`](optional_global.md) and [`source`](optional_global.md).
The technical parameters of the radar are stored as variables.
SOMaR takes their names, meanings, and types from the WMO-CF Radial profile [FM 301][fm301] (see [Level 1a data](../product_types/level1/level1a.md#relation-to-fm-301-and-cfradial)), but not always their location in the file.

Constant technical parameters of the radar antenna, pulse, and scan are stored in a group named `radar_parameters` in the root group. The table below lists the variables that apply to marine radars, with the FM 301 table that defines each of them; all of them are optional. Only the beam widths are part of the FM 301 `radar_parameters` group (Table 301-12). FM 301 stores the pulse and scan parameters per ray in each sweep group (Table 301-8) and `frequency` as a sweep coordinate (Table 301-6); collecting them as constants in `radar_parameters` is a SOMaR choice, since they rarely change for a marine radar.

| Variable | Values | Description |
|---|---|---|
| `beam_width_h`<br><small>[FM 301][fm301], Table 301-12</small> | float; `degree` | Horizontal beam width of the antenna. |
| `beam_width_v`<br><small>[FM 301][fm301], Table 301-12</small> | float; `degree` | Vertical beam width of the antenna. |
| `frequency`<br><small>[FM 301][fm301], Table 301-6</small> | float; `s-1` | Operating frequency of the radar. Scalar in SOMaR; FM 301 defines a `frequency` dimension for multi-frequency radars. |
| `polarization_mode`<br><small>[FM 301][fm301], Tables 301-8, 301-15</small> | string; `"horizontal"` or `"vertical"` | Antenna polarization (typically horizontal or vertical). |
| `pulse_width`<br><small>[FM 301][fm301], Table 301-8</small> | float; `s` | Length of the transmitted pulse. |
| `prt`<br><small>[FM 301][fm301], Table 301-8</small> | float; `s` | Pulse repetition time. |
| `scan_rate`<br><small>[FM 301][fm301], Table 301-8</small> | float; `degree s-1` | Antenna rotation rate. |
| `n_samples`<br><small>[FM 301][fm301], Table 301-8</small> | int | Number of samples contributing to each stored pulse. 1 at Level 1a unless the radar itself averages pulses. |
{: .variable-table }

When pulse or scan parameters vary, [Level 1a](../product_types/level1/level1a.md#sweep-groups) stores them in each sweep group (as scalars per sweep, or with dimension `time` per pulse) and [Level 1b polar](../product_types/level1/level1b_polar.md) stores them in the root group with dimension `time` (per image) or `(time, azimuth)` (per pulse).

## Example

```
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
```

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
