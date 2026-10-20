---
title: Usage examples
layout: default
nav_order: 8
has_children: true
---

# Usage examples

## Processing parameters

The processing parameters needed to interpret the [roughness images](roughness_images.md), the [roughness image mosaics](roughness_mosaics.md), the [map products](#map-products), and the [wave products](#wave-products) are recorded in the following global attributes, in addition to the [shared global attributes](../../metadata_attributes/index.md).

| Attribute | Values | Description |
|---|---|---|
| `analysis_window_size`<br><small>SOMaR</small> | Number; `m` | Required for map and wave products. The diameter of the circular analysis windows. |
| `analysis_window_spacing`<br><small>SOMaR</small> | Number; `m` | Required for map products. The distance between the centers of neighboring analysis windows, i.e. the grid spacing of the map. |
| `averaging_duration`<br><small>SOMaR</small> | Number; `s` | Required for [roughness images](roughness_images.md), [roughness image mosaics](roughness_mosaics.md), and [sea ice drift maps](sea_ice_drift.md). The nominal duration over which Level 1b images are averaged: into one roughness image or mosaic pixel, or into each of the two correlated images of a drift vector. The window of an individual grid cell may be shorter, but never longer. |
| `measurement_duration`<br><small>SOMaR</small> | Number; `s` | Required for [roughness image mosaics](roughness_mosaics.md), map products, and wave products. The duration of the radar image sequence used for each mosaic, map, or wave measurement. |
| `number_of_analysis_windows`<br><small>SOMaR</small> | Integer | Required for wave products. The number of analysis windows averaged into each measurement. |
| `number_of_images`<br><small>SOMaR</small> | Integer | Required for map and wave products. The number of radar images used for each map or wave measurement. Omitted for [sea ice drift maps](sea_ice_drift.md), which are described by `time_lag` and `averaging_duration` instead. |
{: .attribute-table }
