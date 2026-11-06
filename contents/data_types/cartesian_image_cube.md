---
title: cartesian_image_cube (L1b)
layout: default
parent: SOMaR data types
nav_order: 4
---

# cartesian_image_cube (L1b)

Files of the data type `cartesian_image_cube` hold Level 1b Cartesian image sequences: radar images, one per antenna revolution, that have been mapped from the polar coordinates of the sensor onto a regular Cartesian `x`/`y` grid, while otherwise remaining as close as possible to the underlying [`polar_raw`](polar_raw.md) data.
No radiometric calibration or temporal averaging is applied.
The annex gives a complete [example](../annex/level1b_cartesian.md#example).

A file has the following structure, with the groups ending in `/`, the main variables of each group, and alternatives separated by `|`; parentheses after variables give their dimensions, and a label ending in a colon, such as "moving platform:", names the files in which the variables after it occur. The sections below define each item.

```text
/                              time, x, y,
                               fixed platform:  longitude, latitude, crs
                               moving platform: longitude, latitude (time)
                               backscatter_amplitude | backscatter_power (time, y, x)
```

## Image cube

All images of a file share one grid of fixed extent and resolution, and only its origin, the position of the radar antenna at the start of each revolution, moves with a moving platform.
They are therefore stored as a single cube in the root group, whose data variable, [`backscatter_amplitude`](product_variables.md#backscatter_amplitude) or [`backscatter_power`](product_variables.md#backscatter_power), has the dimensions `(time, y, x)`, rather than as [time-bounded grids](../georeferencing/index.md#time-bounded-grids), which would take thousands of groups for the short-lived images of one file.
The data variable is required, and a file holds exactly one of the two; its [`units`](../metadata_attributes/variable_attributes.md#units) and [`comment`](../metadata_attributes/variable_attributes.md#comment) are those of the [data variable](polar_raw.md#data-variable) of `polar_raw`.
The grids of the Level 2 data types, by contrast, can change their extent and dimensions from one measurement to the next with the motion of the platform, and are therefore stored as time-bounded grids.
Grid cells that fall outside the valid field of view, for example those obstructed by platform superstructure, hold the [`_FillValue`](../metadata_attributes/variable_attributes.md#_FillValue).

## Position and orientation

`x` and `y` are distances in meters east and north of the grid origin.
The images are north-oriented: the platform heading and the azimuth and range corrections have been applied in the mapping, so no `heading` is stored; from a fixed platform, they may instead be oriented along the axes of a [rotated local grid](../georeferencing/index.md#rotated-local-grids). This is the main difference from the polar data types, which are stored as recorded.

The grid origin is the position of the radar antenna at the start of each revolution, i.e. the recorded position after application of the [position offsets](../georeferencing/index.md#position-offset), and is given by `longitude` and `latitude`.
For a moving platform, they have the dimension `time`, with one value per image; for a fixed platform, they are scalar, and the cube is a [single grid](../georeferencing/index.md#single-grid).

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required for a fixed platform; omitted for a moving platform. Local azimuthal equidistant projection centered on the radar antenna (see [Georeferencing](../georeferencing/index.md#time-bounded-local-grids)). |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each revolution. |
| `x`<br><small>SOMaR</small> | double `(x)`; `m` | Required. Distance east of the grid origin, or along the x axis of a rotated grid. |
| `y`<br><small>SOMaR</small> | double `(y)`; `m` | Required. Distance north of the grid origin, or along the y axis of a rotated grid. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)` or scalar; `degrees_east` | Required. Longitude (WGS 84) of the grid origin. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)` or scalar; `degrees_north` | Required. Latitude (WGS 84) of the grid origin. |
{: .variable-table }

From a moving platform, the file has no `crs` variable and the data variable no [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) attribute, since a single coordinate reference system variable can describe only one grid origin, whereas the origin here changes from image to image.
For the same reason, `x` and `y` then carry no [`standard_name`](../metadata_attributes/variable_attributes.md#standard_name): CF defines `projection_x_coordinate` and `projection_y_coordinate` in relation to a grid mapping.
From a fixed platform, the origin does not move: the file carries a `crs` that describes the azimuthal equidistant projection centered on the radar antenna, the data variable carries `grid_mapping = "crs"`, and `x` and `y` carry the standard names `projection_x_coordinate` and `projection_y_coordinate`.

## Resampling

The polar data are resampled onto the Cartesian grid by selection, interpolation, or averaging, and the method is recorded in one attribute; as for the [azimuth regularization](polar_image_cube.md#azimuth-regularization) of the polar images, the quantity on which interpolation and averaging are done is recorded in [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity).

| Attribute | Values | Description |
|---|---|---|
| `cartesian_resampling`<br><small>SOMaR</small> | String; one of `nearest_neighbor`, `linear_interpolation`, `average`, `average_or_interpolation` | Required. On the data variable: the method used to resample the polar data onto the Cartesian grid: selection of the polar sample closest to the cell center, bilinear interpolation in range and azimuth between the surrounding polar samples, the mean of all polar samples falling within the cell (cells holding no sample are set to [`_FillValue`](../metadata_attributes/variable_attributes.md#_FillValue)), or that mean where the cell holds at least one polar sample and linear interpolation where it holds none, typically at far range. Except for `nearest_neighbor`, the data variable also carries [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity), which states whether interpolation and averaging are done on power, amplitude, or the stored values. Should be accompanied by a [`comment`](../metadata_attributes/variable_attributes.md#comment) describing the method in words. |
{: .attribute-table }

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/95/build/cf-standard-name-table.html
