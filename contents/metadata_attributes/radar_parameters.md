---
title: Radar parameters
layout: default
parent: Metadata
nav_order: 4
---

# Radar parameters

SOMaR files describe the radar instrument in words through the global attributes [`instrument`](optional_global.md) and [`source`](optional_global.md).
The technical parameters of the radar are stored as variables.
SOMaR does not define these itself but takes them from the WMO-CF Radial profile [FM 301][fm301], which already specifies them for radars in general (see [Level 1a data](../product_types/level1/level1a.md#relation-to-fm-301-and-cfradial)).

Constant technical parameters of the radar antenna, pulse, and scan are stored in a group named `radar_parameters` in the root group. The table below lists the variables that apply to marine radars, with the FM 301 table or section that defines each of them; all of them are optional.

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

Where pulse or scan parameters vary from sweep to sweep or from pulse to pulse, they are stored as variables in the sweep groups instead, alongside the data (see [Level 1a data](../product_types/level1/level1a.md#sweep-groups)). Parameters constant over a sweep are stored as scalars in that sweep group; where they vary from pulse to pulse, they carry the dimension `time`.

For examples showing these variables in NetCDF CDL format, see [Example metadata](example.md#radar-parameters) and [Level 1a data](../product_types/level1/level1a.md#example-for-a-moving-platform).

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
