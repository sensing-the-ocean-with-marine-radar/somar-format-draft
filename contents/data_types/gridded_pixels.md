---
title: gridded_pixels (L2a)
layout: default
parent: SOMaR data types
nav_order: 5
---

# gridded_pixels (L2a)

Files of the data type `gridded_pixels` hold Level 2a values at the resolution of the radar image, one per pixel of a regular grid, such as the time mean of the backscatter in a relative roughness image.
The averaging over time that leads to the value of a pixel is recorded by [`averaging_duration`](../metadata_attributes/processing_parameters.md#averaging_duration).
The annex gives a complete [example](../annex/relative_roughness_images.md#example).

## Grids

The values are stored on the [local grid](../georeferencing/index.md#local-grid), whose `crs` locates every pixel: from a moving platform, one [time-bounded grid](../georeferencing/index.md#time-bounded-grids) per averaging period or measurement period, each in a `time_<YYYYMMDDHHMMSS>` group; from a fixed platform, a [single grid](../georeferencing/index.md#single-grid) in the root group, with the leading dimension `time`.
From a fixed platform, the grid may be a [rotated local grid](../georeferencing/index.md#rotated-local-grids).
A relative roughness image mosaic is stored on a single, larger local grid per measurement period, which extends along the platform track beyond the footprint of a single relative roughness image; mosaics are therefore defined for moving platforms only.
Since the pixels are not analysis windows, the files carry no `longitude` and `latitude` of window centers, no position of the radar antenna other than the origin of the `crs`, and, like the Level 1 data types, no quality flag (see [Quality flags](../metadata_attributes/quality_flags.md)).

## Variables

Each grid holds the following variables, in each `time_<YYYYMMDDHHMMSS>` group or in the root group of a file from a fixed platform, in addition to those of its product (see [Products](#products)).
The data variables of a product are defined under [Product variables](product_variables.md), where `(…)` stands for the dimensions of the grid, preceded by `time` from a fixed platform.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required. Coordinate reference system of the local grid (see [Georeferencing](../georeferencing/index.md#time-bounded-local-grids)). |
| `time`<br><small>[CF][cf-names]</small> | double, or double `(time)` from a fixed platform; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of the averaging period of a relative roughness image, or of the measurement period of a mosaic. Carries `bounds = "time_bounds"` where `time_bounds` is present. |
| `time_bounds`<br><small>[CF][cf-bounds]</small> | double `(nv)`, or double `(time, nv)` from a fixed platform; `seconds since 1970-01-01T00:00:00Z` | Optional. Start and end of the nominal averaging period of a relative roughness image, or of the measurement period of a mosaic, along the dimension `nv` of size 2 ([CF][cf-bounds] section 7.1). |
| `x`<br><small>SOMaR</small> | double `(x)`; `m` | Required. Distance east of the radar antenna at the start of the period, or along the x axis of a rotated grid. |
| `y`<br><small>SOMaR</small> | double `(y)`; `m` | Required. Distance north of the radar antenna at the start of the period, or along the y axis of a rotated grid. |
{: .variable-table }

The data variables carry `grid_mapping = "crs"`.

## Products

The following products have the data type `gridded_pixels`.
For each, the table lists the data variables that it requires, recommends, or allows, in addition to the variables above; they are defined under [Product variables](product_variables.md).
The name of each product links to the table of its file contents in the annex, which lists everything a file of the product holds.

| Product | `data_type` | `product_type` | Variables |
|---|---|---|---|
| [Relative roughness images](../annex/relative_roughness_images.md#file-contents) (L2a) | `gridded_pixels` | `relative_roughness` | **Required:** [`relative_roughness`](product_variables.md#relative_roughness)<br>**Optional:** [`number_of_observations`](product_variables.md#number_of_observations) |
| [Relative roughness image mosaics](../annex/relative_roughness_mosaics.md#file-contents) (L2a) | `gridded_pixels` | `relative_roughness_mosaic` | **Required:** [`relative_roughness`](product_variables.md#relative_roughness), [`start_time_of_observations`](product_variables.md#start_time_of_observations)<br>**Optional:** [`number_of_observations`](product_variables.md#number_of_observations), [`scan_sectors`](product_variables.md#scan_sectors) |
{: .product-type-table }

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/95/build/cf-standard-name-table.html
[cf-bounds]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#cell-boundaries
