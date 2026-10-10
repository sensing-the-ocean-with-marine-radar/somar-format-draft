---
title: SOMaR data types
layout: default
nav_order: 4
---

# SOMaR data types

SOMaR products are organized by processing level, from radar data as recorded by the instrument to derived geophysical variables.
[Level 1](level1/index.md) products retain the radar's own measurement (backscatter intensity or amplitude in uncalibrated units), either pulse by pulse in the sensor's polar geometry ([Level 1a](level1/level1a.md)) or as individual images with a regular azimuth axis ([Level 1b polar](level1/level1b.md#polar-image-sequences-pol3d)) or on a local Cartesian grid ([Level 1b Cartesian](level1/level1b.md#cartesian-image-sequences-cart3d)).
[Level 2](level2/index.md) products are geophysical variables, either retrieved directly from image sequences (Level 2a) or derived from those retrievals (Level 2b).
Each page below documents the product-specific dimensions, variables, and attributes, with a minimal example, in addition to the [shared metadata](../metadata_attributes/index.md).

## Terms

- A **sweep** is the sequence of pulses of one antenna revolution, or of one pass over the sector for a radar that scans a sector. It is the unit in which Level 1a data are stored.
- A **revolution** yields one **image** at Level 1b.
- An **analysis window** is the area, within the radar footprint, from which one Level 2 measurement is retrieved.
- A **measurement period** is the time span over which the images contributing to one Level 2 map or measurement are collected.
