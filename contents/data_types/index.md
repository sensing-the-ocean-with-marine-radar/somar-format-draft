---
title: SOMaR data types
layout: default
nav_order: 5
has_children: true
---

# SOMaR data types

SOMaR files are organized by their data type, i.e. by how their values are arranged and located in space.
Every SOMaR NetCDF file carries the mandatory global attribute [`data_type`](../metadata_attributes/mandatory_global.md#data_type), which names its data type and thereby its structure, and the mandatory global attribute [`platform_is_mobile`](../metadata_attributes/mandatory_global.md#platform_is_mobile), which chooses between the layouts of a moving and a fixed platform (see [Moving and fixed platforms](#moving-and-fixed-platforms)).
A Level 2 file should also carry the global attribute [`product_type`](../metadata_attributes/optional_global.md#product_type), which names the geophysical product that it holds and thereby its data variables; products are defined at Level 2 only, and a Level 1 file is fully described by its data type.
The processing level, from radar data as recorded by the instrument to derived geophysical quantities, is a property of each data type.

| Level | `data_type` | Examples (`product_type`) | Structure |
|:---:|---|---|---|
| **L1a** | [`polar_raw`](polar_raw.md) | [Raw radar data](../annex/level1a.md) | sweeps |
| **L1b** | [`polar_pulse_averaged`](polar_pulse_averaged.md) | [Pulse-averaged data](../annex/level1b_pointing.md) | averaged sweeps |
| **L1b** | [`polar_image_cube`](polar_image_cube.md) | [Polar image sequences](../annex/level1b_polar.md) | `(time, azimuth, range)` cube |
| **L1b** | [`cartesian_image_cube`](cartesian_image_cube.md) | [Cartesian image sequences](../annex/level1b_cartesian.md) | `(time, y, x)` cube |
| **L2a** | [`gridded_pixels`](gridded_pixels.md) | [Relative roughness images](../annex/relative_roughness_images.md) (`relative_roughness`)<br>[Relative roughness image mosaics](../annex/relative_roughness_mosaics.md) (`relative_roughness_mosaic`) | time-bounded grids or a single grid |
| **L2a** | [`gridded_windows`](gridded_windows.md) | [Near-surface current maps](../annex/current_maps.md) (`currents`)<br>[Near-surface current profile maps](../annex/current_profile_maps.md) (`currents_profile`)<br>[Bathymetric maps](../annex/depth_maps.md) (`bathymetry`)<br>[Sea ice drift maps](../annex/sea_ice_drift.md) (`sea_ice_drift`) | time-bounded grids or a single grid |
| **L2a/L2b** | [`discrete_windows`](discrete_windows.md) | [example on its page](discrete_windows.md#example) | `(time, window, …)` in the root group, with `longitude` and `latitude` `(time, window)` |
| **L2a/L2b** | [`averaged_windows`](averaged_windows.md) | [Surface wave two-dimensional wavenumber spectra](../annex/wave_wavenumber_spectra.md) (`wave_wavenumber_spectra`)<br>[Surface wave frequency-direction spectra](../annex/wave_frequency_direction_spectra.md) (`wave_frequency_direction_spectra`)<br>[Surface wave one-dimensional frequency spectra](../annex/wave_frequency_spectra.md) (`wave_frequency_spectra`)<br>[Peak and mean wave parameters](../annex/wave_parameters.md) (`wave_parameters`) | CF trajectory or time series |
{: .product-table }

## Processing levels

Level 1 data retain the radar's own measurement (backscatter amplitude or power in uncalibrated units), either ray by ray in the sensor's polar geometry ([`polar_raw`](polar_raw.md), Level 1a), averaged over consecutive pulses ([`polar_pulse_averaged`](polar_pulse_averaged.md)), or as individual images, one per antenna revolution, with a regular azimuth axis ([`polar_image_cube`](polar_image_cube.md)) or on a local Cartesian grid ([`cartesian_image_cube`](cartesian_image_cube.md)), and serve as the input of the Level 2 retrievals.
Level 2 products are derived from sequences of Level 1b images: geophysical quantities, such as near-surface currents, bathymetry, sea ice drift, and surface waves, and the relative sea surface roughness, a time mean of the backscatter that serves as an uncalibrated proxy of the sea surface roughness.
Level 2a products are the direct result of a retrieval applied to Level 1b image sequences: relative roughness images and mosaics, maps of near-surface currents, current profiles, bathymetry, and sea ice drift, and two-dimensional wavenumber spectra.
Level 2b products are computed from Level 2a products and therefore inherit their sampling, calibration, and quality control; currently all of them are surface wave products derived from the two-dimensional wavenumber spectra.
How the Level 2 products were obtained is recorded in their [processing parameters](../metadata_attributes/processing_parameters.md), and how good they are in their [quality flags](../metadata_attributes/quality_flags.md).

## Choosing the data type

Each data type is defined on a page of its own:

- The polar data types locate each value by the range and azimuth of the sensor, with the radar antenna at the origin: [`polar_raw`](polar_raw.md), every ray as recorded; [`polar_pulse_averaged`](polar_pulse_averaged.md), rays averaged over consecutive pulses; and [`polar_image_cube`](polar_image_cube.md), one image per revolution on a regular azimuth axis.
- [`cartesian_image_cube`](cartesian_image_cube.md) gives one image per revolution on a local Cartesian grid.
- [`gridded_pixels`](gridded_pixels.md) gives one value per pixel of a radar image, and [`gridded_windows`](gridded_windows.md) one value set per analysis window, where the windows form a grid fixed to the Earth.
- [`discrete_windows`](discrete_windows.md) gives one value set for each of a set of analysis windows that do not form a grid fixed to the Earth.
- [`averaged_windows`](averaged_windows.md) combines several analysis windows into one value set per measurement, located at their mean position.

A Level 1 file takes the data type of its form: the four Level 1 data types differ in their geometry and in whether rays or pulses are averaged.
A Level 2 file takes the first of the following data types whose question it answers with yes:

1. Does each value belong to one pixel of the radar image rather than to an analysis window? → `gridded_pixels`.
2. Are the window results merged into one value set per measurement? → `averaged_windows`.
3. Do the windows form a regular lattice that stays fixed to the Earth ([`analysis_window_motion`](../metadata_attributes/processing_parameters.md#analysis_window_motion) `= earth_fixed`)? → `gridded_windows`.
4. Otherwise → `discrete_windows`.

Each data-type page defines the structure and the variables that its files share; the pages of the Level 2 data types also list their products, in a product table, with the variables that each of them holds.
The variables themselves are defined under [Product variables](product_variables.md).
The informative [Annex: Examples](../annex/index.md) gives for each Level 1 data type and each Level 2 product a table of its [file contents](../annex/index.md#file-contents), which brings together the items that a file holds, with their tiers and links to their definitions, an example file, and for Level 2 a description of the product and its retrieval.
All files carry the [shared metadata](../metadata_attributes/index.md) in addition.

### Moving and fixed platforms

The structure of a file depends on its data type and on whether the platform moves, which the file states by setting [`platform_is_mobile`](../metadata_attributes/mandatory_global.md#platform_is_mobile) to `"true"` or `"false"`:

| | Moving platform | Fixed platform |
|---|---|---|
| **`polar_raw`, `polar_pulse_averaged`, `polar_image_cube`** | the position and heading of the platform per sweep or per ray (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)) | scalar `latitude` and `longitude` of the radar antenna |
| **`cartesian_image_cube`** | one [image cube](cartesian_image_cube.md#image-cube) whose origin `longitude(time)`, `latitude(time)` moves with the platform | the same cube with scalar `longitude` and `latitude`, as a [single grid](../georeferencing/index.md#single-grid) |
| **`gridded_pixels`, `gridded_windows`** | one [time-bounded grid](../georeferencing/index.md#time-bounded-grids) per measurement, each in its own `time_<YYYYMMDDHHMMSS>` group | a [single grid](../georeferencing/index.md#single-grid) for the whole file, with the leading dimension `time` |
| **`discrete_windows`** | the [windows](discrete_windows.md#windows) in the root group, with `longitude(time, window)` and `latitude(time, window)` | the same |
| **`averaged_windows`** | a [trajectory](averaged_windows.md#moving-and-fixed-platforms): `longitude(time)` and `latitude(time)` | a [time series](averaged_windows.md#moving-and-fixed-platforms): scalar `longitude` and `latitude` |

## Requirements

The tables state for each variable and attribute whether it is required, recommended, or optional:

- **Required** items are those without which a reader would misread the values or misplace them in time or space: the coordinates, the data variables that define the product, and the parameters that change what a value means.
- **Recommended** items document how the data were obtained and how good they are, such as the processing parameters, the quality flag, and retrieval diagnostics. A file should carry them where its producer can supply them.
- **Optional** items are further diagnostics and details that a producer may add.

Only the required items are part of [compliance](../metadata_attributes/mandatory_global.md#compliance).

Where the tier of an item depends on the file, its description begins with clauses of a fixed form, separated by semicolons, such as "Required on the local grid; recommended on the geographic grid.".
Each clause gives a tier, or "omitted" for an item that the file does not carry, and the files to which it applies: "for a moving platform" or "for a fixed platform"; "on the local grid" or "on the geographic grid" of a [gridded data type](../georeferencing/index.md#grids); "on a rotated grid", i.e. in a file whose `crs` is that of a [rotated local grid](../georeferencing/index.md#rotated-local-grids); for a data type, such as "for `gridded_windows`", or for a product type, such as "for `sea_ice_drift`"; or the files in which another item has a value, such as "if `sweep_mode` is `"pointing"`".
A clause ending in "otherwise" applies to the files that no other clause names, and where an omitting clause applies, it takes precedence.
For a file to which no clause applies, the item is not defined.
On a rotated local grid, a variable that takes the place of another, such as [`sea_water_x_velocity`](product_variables.md#sea_water_x_velocity) in place of [`eastward_sea_water_velocity`](product_variables.md#eastward_sea_water_velocity), has the tier of the variable it replaces, which is omitted (see [Product variables](product_variables.md)).
Sectors of the field of view that are shadowed or blanked are recorded in the `radar_parameters` group (see [Obstructed sectors](../metadata_attributes/radar_parameters.md#obstructed-sectors)).

## Adding a data type or product type

A file whose content fits none of the data types is not a SOMaR file.
A file of a Level 2 data type whose product has no product type yet complies with SOMaR through its data type alone, and omits [`product_type`](../metadata_attributes/optional_global.md#product_type).
A new product type is proposed as an [issue](https://github.com/sensing-the-ocean-with-marine-radar/somar-format-draft/issues) or pull request that gives its row in the product table of its data type, the definitions of any new variables under [Product variables](product_variables.md), and an example file for the annex; a new data type is proposed in the same way, with the page that defines its structure.
Adding a data type or product type invalidates no existing file, so that it can be released in a minor version (see [Versioning](../../index.md#versioning)).

{: .open_issue }
> Radar product types that are not yet defined:
> * Wave spectrum partitioning results (wave parameters for wind sea and swell systems),
> * Wind speed and direction retrieved from radar backscatter,
> * Products in discrete windows, such as windows fixed to the platform or upwind windows,
> * Products for coastal applications, such as the mapping of intertidal areas.
