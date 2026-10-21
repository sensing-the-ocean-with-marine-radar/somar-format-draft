---
title: Georeference correction parameters
layout: default
parent: Metadata
nav_order: 8
---

# Georeference correction parameters

Known offsets of the recorded pointing direction, range, time, and platform position are stored in a group named `georeference_correction` in the root group.
For a ship-borne radar, the azimuth, range, and time offsets can be estimated from the imagery itself (McCann and Bell [2018](../references/index.md#mccann-bell-2018)).
This group is not part of FM 301; it is taken from CfRadial 2.1 (section 7.5), except for the time correction and the position offsets, which are SOMaR additions.

The group is used only by [Level 1a](../product_types/polar.md) and [Level 1b polar](../product_types/polar.md#image-cube) products; how the corrections are applied is described under [Georeferencing](../georeferencing/index.md#applying-georeference-corrections).

| Variable | Values | Description |
|---|---|---|
| `azimuth_correction`<br><small>[CfRadial 2.1][cfradial], Section 7.5</small> | float; `degree` | Correction to the `azimuth` values, e.g. the offset between the radar's zero direction and the bow of the ship. A constant bias of the heading sensor is included here; the separate `heading_correction` of CfRadial 2.1 is not used. |
| `range_correction`<br><small>[CfRadial 2.1][cfradial], Section 7.5</small> | float; `m` | Correction to the `range` values, e.g. a range offset caused by a trigger delay. |
| `time_correction`<br><small>SOMaR</small> | double; `s` | Correction to the `time` values, e.g. a known constant offset of the radar clock relative to GPS time. |
| `position_offset_x`<br><small>SOMaR</small> | float; `m` | Position of the radar antenna relative to the GPS antenna in the ship frame, positive to starboard (see [Position offset](../georeferencing/index.md#position-offset)). |
| `position_offset_y`<br><small>SOMaR</small> | float; `m` | Position of the radar antenna relative to the GPS antenna in the ship frame, positive toward the bow (see [Position offset](../georeferencing/index.md#position-offset)). |
{: .variable-table }

## Example

```
group: georeference_correction {
  variables:
        float azimuth_correction ;
                azimuth_correction:units = "degree" ;
                azimuth_correction:long_name = "correction to azimuth values" ;
        float range_correction ;
                range_correction:units = "m" ;
                range_correction:long_name = "correction to range values" ;
        double time_correction ;
                time_correction:units = "s" ;
                time_correction:long_name = "correction to time values" ;
        float position_offset_x ;
                position_offset_x:units = "m" ;
                position_offset_x:long_name = "position of radar antenna relative to GPS antenna, positive to starboard" ;
        float position_offset_y ;
                position_offset_y:units = "m" ;
                position_offset_y:long_name = "position of radar antenna relative to GPS antenna, positive toward the bow" ;
  data:
        azimuth_correction = -1.3 ;
        range_correction = -22.5 ;
        time_correction = 0.35 ;
        position_offset_x = 2.4 ;
        position_offset_y = -11.8 ;
  } // group georeference_correction
```

[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
