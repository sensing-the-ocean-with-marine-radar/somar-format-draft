---
title: Radar parameters
layout: default
parent: Metadata
nav_order: 4
---

# Radar Parameters/Calibration Group

SOMaR files describe the radar instrument in words through two global attributes, `instrument` (see [Optional global attributes](optional_global.md)) and `source` (see [Mandatory global attributes](mandatory_global.md)):

| Attribute | Values | Description |
|---|---|---|
| `instrument`<br><small>[ACDD](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3)</small> | String; free text | The manufacturer, model, and/or type of the radar system used, including relevant technical detail such as whether the receiver is coherent. |
| `source`<br><small>[CF](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents)</small> | String; free text | The general method of production, e.g. platform and sensor type. |
{: .attribute-table }

The technical parameters of the radar are stored as variables.
SOMaR does not define these itself but takes them from the WMO-CF Radial profile [FM 301][fm301], which already specifies them for radars in general, and, where FM 301 has no provision, from the earlier [CfRadial 2.1][cfradial] draft (see [Level 1a data](../data_types/level1/level1a.md#relation-to-fm-301-and-cfradial)).
The tables below list the variables that apply to marine radars, with the table or section that defines each of them; all of them are optional.
Variables for the vertical polarization channel (`xmit_power_v`, ...) are defined by FM 301 in the same way; a radar with a single polarization uses the `_h` variables.

## Pulse and scan parameters

Parameters that may change from pulse to pulse are stored as variables in the sweep groups, alongside the data (see [Level 1a data](../data_types/level1/level1a.md#sweep-groups)).
All of them are optional.

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

Known offsets of the recorded pointing direction, range, and platform data are stored in a group named `georeference_correction` in the root group.
This group is not part of FM 301; it is taken from CfRadial 2.1 (section 7.5), except for the position offsets, which are a SOMaR addition.
The corrections are constant for a file and are added to the recorded values; a missing variable is equivalent to a correction of 0.
The position offsets are rotated by the heading before they are added (see [Position offset](#position-offset)).
At [Level 1a](../data_types/level1/level1a.md), the data are stored as recorded and the corrections are not applied.

| Variable | Values | Description |
|---|---|---|
| `azimuth_correction`<br><small>[CfRadial 2.1][cfradial], Section 7.5</small> | float; `degrees` | Correction to the `azimuth` values, e.g. the offset between the radar's zero direction and the bow of the ship. |
| `range_correction`<br><small>[CfRadial 2.1][cfradial], Section 7.5</small> | float; `metres` | Correction to the `range` values, e.g. a range offset caused by a trigger delay. |
| `heading_correction`<br><small>[CfRadial 2.1][cfradial], Section 7.5</small> | float; `degrees` | Correction to the `heading` values. |
| `position_offset_x`<br><small>SOMaR</small> | float; `metres` | Position of the radar antenna relative to the GPS antenna in the ship frame, positive to starboard. |
| `position_offset_y`<br><small>SOMaR</small> | float; `metres` | Position of the radar antenna relative to the GPS antenna in the ship frame, positive toward the bow. |
{: .variable-table }

### Position offset

Where the position of a moving platform has been taken from a GPS antenna at a different location on the platform, the recorded `latitude` and `longitude` are those of the GPS antenna.
`position_offset_x` and `position_offset_y` give the position of the radar antenna relative to the GPS antenna in a ship frame whose x-axis is positive to starboard and whose y-axis is positive toward the bow.
They replace the `latitude_correction` and `longitude_correction` of CfRadial 2.1, which are constant in degrees and therefore valid for a single heading only; an offset in the ship frame is independent of the heading.

With `H = heading + heading_correction`, the radar antenna is located

```
east  =  position_offset_x * cos(H) + position_offset_y * sin(H)
north = -position_offset_x * sin(H) + position_offset_y * cos(H)
```

metres east and north of the recorded position; the conversion to `latitude` and `longitude` is carried out on the WGS 84 ellipsoid.
The offsets are horizontal distances for a level ship; roll and pitch are neglected.
For a fixed platform, the position offsets are not used, and `latitude` and `longitude` in the root group give the position of the radar antenna.

## Uncalibrated backscatter

Level 1 data variables hold raw analog-to-digital converter (ADC) counts or a quantity derived from them. As introduced in [Level 1a data](../data_types/level1/level1a.md), such variables use the standard CF/UDUNITS `scale_factor` and `add_offset` attributes together with `units = "1"` or `units = "dB"`, and must state in a `comment` attribute whether the stored quantity is an amplitude or a power:

```
ushort polar_amp(time, range) ;
        polar_amp:scale_factor = 0.176738930567883 ;
        polar_amp:add_offset = 0. ;
        polar_amp:_FillValue = 65535US ;
        polar_amp:long_name = "radar_backscatter_amplitude" ;
        polar_amp:units = "1" ;
        polar_amp:coordinates = "azimuth range" ;
        polar_amp:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). I and Q are the in-phase and quadrature channels both measured in counts of the analog-to-digital-converter (ADC)." ;
```

## Retrieval calibration

Several Level 2 products derive physically calibrated quantities (e.g. significant wave height, current velocity, water depth) from the radar signal using retrieval-specific calibration parameters — for example, the `summary` attributes of the wave and current products reference an "empirical modulation transfer function" and "radar specific calibration parameters" used internally during processing. These parameters describe the retrieval rather than the radar and are not covered by FM 301 or CfRadial. They are not yet exposed as their own NetCDF attributes or variables in current SOMaR output; formalizing how they should be recorded is an open item for a future revision of the format.

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
