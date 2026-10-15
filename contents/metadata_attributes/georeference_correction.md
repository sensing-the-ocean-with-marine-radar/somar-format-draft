---
title: Georeference correction parameters
layout: default
parent: Metadata
nav_order: 5
---

# Georeference correction parameters

Known offsets of the recorded pointing direction, range, time, and platform position are stored in a group named `georeference_correction` in the root group.
This group is not part of FM 301; it is taken from CfRadial 2.1 (section 7.5), except for the time correction and the position offsets, which are SOMaR additions.

This group is only present in [Level 1a](../product_types/level1/level1a.md) and [Level 1b polar](../product_types/level1/level1b_polar.md) products, where coordinates are stored as recorded by the instrument and corrections have not been applied. In Cartesian and Level 2 products, these corrections have already been applied during grid generation, so this group is omitted (see [Georeferencing](../georeferencing/index.md#applying-georeference-corrections)).

| Variable | Values | Description |
|---|---|---|
| `azimuth_correction`<br><small>[CfRadial 2.1][cfradial], Section 7.5</small> | float; `degree` | Correction to the `azimuth` values, e.g. the offset between the radar's zero direction and the bow of the ship, including any constant bias of the heading sensor. |
| `range_correction`<br><small>[CfRadial 2.1][cfradial], Section 7.5</small> | float; `m` | Correction to the `range` values, e.g. a range offset caused by a trigger delay. |
| `time_correction`<br><small>SOMaR</small> | double; `s` | Correction to the `time` values, e.g. a known constant offset of the radar clock relative to GPS time. |
| `position_offset_x`<br><small>SOMaR</small> | float; `m` | Position of the radar antenna relative to the GPS antenna in the ship frame, positive to starboard (see [Position offset](../georeferencing/index.md#position-offset)). |
| `position_offset_y`<br><small>SOMaR</small> | float; `m` | Position of the radar antenna relative to the GPS antenna in the ship frame, positive toward the bow (see [Position offset](../georeferencing/index.md#position-offset)). |
{: .variable-table }

For an example showing this group in NetCDF CDL format, see [Example metadata](example.md#georeference-correction-parameters) and [Level 1a data](../product_types/level1/level1a.md#example-for-a-moving-platform).

[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
