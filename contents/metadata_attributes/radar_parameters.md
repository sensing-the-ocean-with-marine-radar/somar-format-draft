---
title: Radar parameters
layout: default
parent: Metadata attributes
nav_order: 4
---

# Radar Parameters/Calibration Group

SOMaR files describe the radar instrument in words through two global attributes, `instrument` (see [Optional global attributes](optional_global.md)) and `source` (see [Mandatory global attributes](mandatory_global.md)):

| Attribute | Defined by | Values | Description | Example |
|---|---|---|---|---|
| `instrument` | [ACDD](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3) | String; free text | The manufacturer, model, and/or type of the radar system used, including relevant technical detail such as whether the receiver is coherent. | `"Helmholtz-Zentrum Hereon coherent-on-receive marine X-band radar"` |
| `source` | [CF](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents) | String; free text | The general method of production, e.g. platform and sensor type. | `"Shipboard marine X-band radar"` |
{: .attribute-table }

The technical parameters of the radar are stored as variables.
SOMaR does not define these itself but takes them from the WMO-CF Radial profile [FM 301][fm301], which already specifies them for radars in general, and, where FM 301 has no provision, from the earlier [CfRadial 2.1][cfradial] draft (see [Level 1a data](../data_types/level1/level1a.md#relation-to-fm-301-and-cfradial)).
The tables below list the variables that apply to marine radars, with the table or section that defines each of them; all of them are optional.
Variables for the vertical polarization channel (`antenna_gain_v`, `xmit_power_v`, ...) are defined by FM 301 in the same way; a radar with a single polarization uses the `_h` variables.

## Pulse and scan parameters

Parameters that may change from pulse to pulse are stored in the sweep groups, alongside the data (see [Level 1a data](../data_types/level1/level1a.md#sweep-groups)): `frequency`, `polarization_mode`, `pulse_width`, `prt`, `scan_rate`, and `n_samples` (FM 301, Tables 301-6 and 301-8).

## The `radar_parameters` group

Constant properties of the antenna and receiver are stored in a group named `radar_parameters` in the root group (FM 301, regulation 301.5 and Table 301-12).

| Variable | Type | Units | Description |
|---|---|---|---|
| `antenna_gain_h` | float | `dBi` | Nominal antenna gain. |
| `beam_width_h` | float | `degrees` | Horizontal beam width of the antenna. |
| `beam_width_v` | float | `degrees` | Vertical beam width of the antenna. |
| `receiver_bandwidth` | float | `s-1` | Bandwidth of the radar receiver. |

## The `radar_calibration` group

Where a radiometric calibration of the radar is available, it is stored in a group named `radar_calibration` in the root group (FM 301, regulation 301.7 and Table 301-14).
Since a different calibration applies to each pulse width, all variables in this group have the dimension `calib`.
FM 301 defines a comprehensive set of calibration variables there, among them `pulse_width`, `xmit_power_h`, `antenna_gain_h`, and the waveguide and radome losses; SOMaR uses them as defined.

## The `georeference_correction` group

Known offsets of the recorded pointing direction, range, and platform data are stored in a group named `georeference_correction` in the root group.
This group is not part of FM 301; it is taken from CfRadial 2.1 (section 7.5), except for the position offsets, which are a SOMaR addition.
The corrections are constant for a file and are added to the recorded values; a missing variable is equivalent to a correction of 0.
The position offsets are rotated by the heading before they are added (see [Position offset](#position-offset)).
At [Level 1a](../data_types/level1/level1a.md), the data are stored as recorded and the corrections are not applied.

| Variable | Type | Units | Description |
|---|---|---|---|
| `azimuth_correction` | float | `degrees` | Correction to the `azimuth` values, e.g. the offset between the radar's zero direction and the bow of the ship. |
| `range_correction` | float | `metres` | Correction to the `range` values, e.g. a range offset caused by a trigger delay. |
| `heading_correction` | float | `degrees` | Correction to the `heading` values. |
| `position_offset_x` | float | `metres` | Position of the radar antenna relative to the GPS antenna in the ship frame, positive to starboard. |
| `position_offset_y` | float | `metres` | Position of the radar antenna relative to the GPS antenna in the ship frame, positive toward the bow. |

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

Until a radiometric calibration is applied, Level 1 data variables hold raw analog-to-digital converter (ADC) counts or a quantity derived from them. As introduced in [Level 1a data](../data_types/level1/level1a.md), such variables use the standard CF/UDUNITS `scale_factor` and `add_offset` attributes together with `units = "1"` or `units = "dB"`, and must state in a `comment` attribute whether the stored quantity is an amplitude or a power:

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

Data variables in [Level 1b polar images](../data_types/level1/level1b.md#polar-image-sequences-pol3d), whose irregular pulse azimuths have been resampled onto a regular azimuth grid, additionally carry a variable attribute recording how this was done:

| Attribute | Defined by | Values | Description | Example |
|---|---|---|---|---|
| `azimuth_regularization` | SOMaR | String; one of `nearest_neighbor`, `linear_interpolation`, `average` | The method used to resample pulses recorded at irregular azimuths onto the regular `azimuth` axis: selection of the closest pulse, linear interpolation between the two adjacent pulses, or the mean of all pulses falling within each azimuth bin. Should be accompanied by a `comment` describing the method in words. | `"nearest_neighbor"` |
{: .attribute-table }

## Retrieval calibration

Several Level 2 products derive physically calibrated quantities (e.g. significant wave height, current velocity, water depth) from the radar signal using retrieval-specific calibration parameters — for example, the `summary` attributes of the wave and current products reference an "empirical modulation transfer function" and "radar specific calibration parameters" used internally during processing. These parameters describe the retrieval rather than the radar and are not covered by FM 301 or CfRadial. They are not yet exposed as their own NetCDF attributes or variables in current SOMaR output; formalizing how they should be recorded is an open item for a future revision of the format.

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
