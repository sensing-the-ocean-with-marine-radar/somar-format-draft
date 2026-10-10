---
title: Radar parameters
layout: default
parent: Metadata
nav_order: 4
---

# Radar parameters

SOMaR files describe the radar instrument in words through the global attributes [`instrument`](optional_global.md) and [`source`](mandatory_global.md).
The technical parameters of the radar are stored as variables.
SOMaR does not define these itself but takes them from the WMO-CF Radial profile [FM 301][fm301], which already specifies them for radars in general, and, where FM 301 has no provision, from the earlier [CfRadial 2.1][cfradial] draft (see [Level 1a data](../data_types/level1/level1a.md#relation-to-fm-301-and-cfradial)).
The tables below list the variables that apply to marine radars, with the table or section that defines each of them; all of them are optional.

## Pulse and scan parameters

Parameters that may change from pulse to pulse are stored as variables in the sweep groups, alongside the data (see [Level 1a data](../data_types/level1/level1a.md#sweep-groups)).

| Variable | Values | Description |
|---|---|---|
| `frequency`<br><small>[FM 301][fm301], Table 301-6</small> | float `(frequency)`; `s-1` | Operating frequency of the radar. |
| `polarization_mode`<br><small>[FM 301][fm301], Tables 301-8, 301-15</small> | string; `"horizontal"` or `"vertical"` | Polarization of the radar: HH or VV. |
| `pulse_width`<br><small>[FM 301][fm301], Table 301-8</small> | float `(time)`; `seconds` | Length of the transmitted pulse. |
| `prt`<br><small>[FM 301][fm301], Table 301-8</small> | float `(time)`; `seconds` | Pulse repetition time. |
| `scan_rate`<br><small>[FM 301][fm301], Table 301-8</small> | float `(time)`; `degrees/s` | Antenna rotation rate. |
| `n_samples`<br><small>[FM 301][fm301], Table 301-8</small> | int `(time)` | Number of samples contributing to each stored pulse. 1 at Level 1a unless the radar itself averages pulses. |
{: .variable-table }

## The `radar_parameters` group

Constant properties of the antenna are stored in a group named `radar_parameters` in the root group (FM 301, regulation 301.5 and Table 301-12).

| Variable | Values | Description |
|---|---|---|
| `beam_width_h`<br><small>[FM 301][fm301], Table 301-12</small> | float; `degrees` | Horizontal beam width of the antenna. |
| `beam_width_v`<br><small>[FM 301][fm301], Table 301-12</small> | float; `degrees` | Vertical beam width of the antenna. |
{: .variable-table }

## The `georeference_correction` group

Known offsets of the recorded pointing direction, range, time, and platform position are stored in a group named `georeference_correction` in the root group.
This group is not part of FM 301; it is taken from CfRadial 2.1 (section 7.5), except for the time correction and the position offsets, which are SOMaR additions.
The corrections are constant for a file and are added to the recorded values; a missing variable is equivalent to a correction of 0.
The position offsets are rotated by the heading before they are added (see [Position offset](#position-offset)).
At [Level 1a](../data_types/level1/level1a.md), the data are stored as recorded and the corrections are not applied.

| Variable | Values | Description |
|---|---|---|
| `azimuth_correction`<br><small>[CfRadial 2.1][cfradial], Section 7.5</small> | float; `degrees` | Correction to the `azimuth` values, e.g. the offset between the radar's zero direction and the bow of the ship, including any constant bias of the heading sensor. |
| `range_correction`<br><small>[CfRadial 2.1][cfradial], Section 7.5</small> | float; `metres` | Correction to the `range` values, e.g. a range offset caused by a trigger delay. |
| `time_correction`<br><small>SOMaR</small> | double; `seconds` | Correction to the `time` values, e.g. a known constant offset of the radar clock relative to GPS time. |
| `position_offset_x`<br><small>SOMaR</small> | float; `metres` | Position of the radar antenna relative to the GPS antenna in the ship frame, positive to starboard. |
| `position_offset_y`<br><small>SOMaR</small> | float; `metres` | Position of the radar antenna relative to the GPS antenna in the ship frame, positive toward the bow. |
{: .variable-table }

### Position offset

Where the position of a moving platform has been taken from a GPS antenna at a different location on the platform, the recorded `latitude` and `longitude` are those of the GPS antenna.
`position_offset_x` and `position_offset_y` give the position of the radar antenna relative to the GPS antenna in a ship frame whose x-axis is positive to starboard and whose y-axis is positive toward the bow.
They replace the `latitude_correction` and `longitude_correction` of CfRadial 2.1, which are constant in degrees and therefore valid for a single heading only; an offset in the ship frame is independent of the heading.

With the heading `H`, the radar antenna is located

```
east  =  position_offset_x * cos(H) + position_offset_y * sin(H)
north = -position_offset_x * sin(H) + position_offset_y * cos(H)
```

meters east and north of the recorded position; the conversion to `latitude` and `longitude` is carried out on the WGS 84 ellipsoid.
The offsets are horizontal distances for a level ship; roll and pitch are neglected.
For a fixed platform, the position offsets are not used, and `latitude` and `longitude` in the root group give the position of the radar antenna.

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
