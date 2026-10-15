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
The tables below list the variables that apply to marine radars, with the table or section that defines each of them; all of them are optional.

Known offsets of pointing direction, range, time, and antenna position relative to GPS are georeference corrections rather than instrument parameters; they are stored in the `georeference_correction` group and documented under [Georeference correction parameters](georeference_correction.md).

## Pulse and scan parameters

Parameters that may change from pulse to pulse are stored as variables in the sweep groups, alongside the data (see [Level 1a data](../product_types/level1/level1a.md#sweep-groups)).

| Variable | Values | Description |
|---|---|---|
| `frequency`<br><small>[FM 301][fm301], Table 301-6</small> | float `(frequency)`; `s-1` | Operating frequency of the radar. |
| `polarization_mode`<br><small>[FM 301][fm301], Tables 301-8, 301-15</small> | string; `"horizontal"` or `"vertical"` | Polarization of the radar: HH or VV. |
| `pulse_width`<br><small>[FM 301][fm301], Table 301-8</small> | float `(time)`; `s` | Length of the transmitted pulse. |
| `prt`<br><small>[FM 301][fm301], Table 301-8</small> | float `(time)`; `s` | Pulse repetition time. |
| `scan_rate`<br><small>[FM 301][fm301], Table 301-8</small> | float `(time)`; `degree s-1` | Antenna rotation rate. |
| `n_samples`<br><small>[FM 301][fm301], Table 301-8</small> | int `(time)` | Number of samples contributing to each stored pulse. 1 at Level 1a unless the radar itself averages pulses. |
{: .variable-table }

## The `radar_parameters` group

Constant properties of the antenna are stored in a group named `radar_parameters` in the root group (FM 301, regulation 301.5 and Table 301-12).

| Variable | Values | Description |
|---|---|---|
| `beam_width_h`<br><small>[FM 301][fm301], Table 301-12</small> | float; `degree` | Horizontal beam width of the antenna. |
| `beam_width_v`<br><small>[FM 301][fm301], Table 301-12</small> | float; `degree` | Vertical beam width of the antenna. |
{: .variable-table }

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
