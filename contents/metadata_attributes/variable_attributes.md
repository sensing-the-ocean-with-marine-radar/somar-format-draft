---
title: Variable attributes
layout: default
parent: Metadata attributes
nav_order: 3
---

# Variable attributes

The tables below list the attributes that SOMaR files attach to individual variables, as opposed to the file as a whole.
Which of them a given variable carries depends on the product and is shown in the minimal example on each product's page; where an attribute has a fixed set of permitted values, all of them are listed and those currently used by SOMaR are set in bold.

## Data and coordinate variables

| Attribute | Defined by | Values | Description | Example |
|---|---|---|---|---|
| `standard_name` | [CF][cf-standard-name] | String; a name from the CF standard name table | Identifies the physical quantity. Given wherever a suitable CF standard name exists. | `"sea_surface_wave_significant_height"` |
| `long_name` | [CF][cf-long-name] | String; free text | A human-readable description of the variable. | `"start time of wave measurement"` |
| `units` | [CF][cf-units] | String; a unit recognized by UDUNITS | The unit of the stored values. Uncalibrated radar backscatter uses `"1"` (linear) or `"dB"` (logarithmic). | `"m s-1"` |
| `comment` | [CF][cf-description] | String; free text | Additional information about the variable. Required on Level 1 backscatter variables to state whether the stored quantity is an amplitude or a power (see [Radar parameters](radar_parameters.md)). | `"the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). ..."` |
| `calendar` | [CF][cf-calendar] | String; a CF calendar name. SOMaR uses **`standard`** | The calendar in which a time variable is expressed. | `"standard"` |
| `scale_factor` | [CF][cf-packed] | Number | Factor by which stored values are multiplied to unpack them. | `0.176738930567883` |
| `add_offset` | [CF][cf-packed] | Number | Offset added to stored values after scaling. | `0.` |
| `_FillValue` | [CF][cf-missing] | Same type as the variable | The value marking missing data. | `-1b` |
| `valid_range` | [CF][cf-missing] | Two numbers of the variable's type: minimum, maximum | The smallest and largest valid values. | `0UB, 127UB` |
| `ancillary_variables` | [CF][cf-ancillary] | String; blank-separated list of variable names | Variables that qualify this one, such as observation counts or quality flags. | `"number_of_observations"` |
| `flag_values` | [CF][cf-flags] | List of values of the variable's type | The values a flag variable can take. | `0UB, 1UB` |
| `flag_meanings` | [CF][cf-flags] | String; blank-separated list with one word per flag value | The meaning of each entry in `flag_values`, in the same order. | `"good bad"` |
| `time_iso_8601` | SOMaR | String; ISO 8601 date and time in UTC, fractional seconds permitted | Optional, on the scalar `time` variable of a time-bounded grid: the same instant as the variable's value in human-readable form. It must agree with `time` (see [Georeferencing](georeferencing.md)). | `"2025-01-15T11:10:01.357666Z"` |
| `azimuth_regularization` | SOMaR | String; one of `nearest_neighbor`, `linear_interpolation`, `average` | On Level 1b polar data variables: how pulses recorded at irregular azimuths were resampled onto the regular `azimuth` axis (see [Radar parameters](radar_parameters.md)). | `"nearest_neighbor"` |

## Trajectory and grid mapping references

| Attribute | Defined by | Values | Description | Example |
|---|---|---|---|---|
| `cf_role` | [CF][cf-dsg] | String; one of `timeseries_id`, `profile_id`, **`trajectory_id`** | Marks the variable that identifies the feature the file's data belong to. In SOMaR it is carried by the scalar `trajectory` variable. | `"trajectory_id"` |
| `grid_mapping` | [CF][cf-grid-mapping] | String; either the name of one coordinate reference system variable, or the extended form `<crs variable>: <coordinate> [<coordinate> ...]`, repeated for each coordinate reference system | Links a data or coordinate variable to the variable describing its coordinate reference system. The extended form names the coordinate variables a coordinate reference system applies to. | `"crs"`<br>`"crs: x y"` |

## Coordinate reference system variables

These attributes are carried by the scalar coordinate reference system variables (conventionally `crs`) that `grid_mapping` refers to.

| Attribute | Defined by | Values | Description | Example |
|---|---|---|---|---|
| `grid_mapping_name` | [CF][cf-appendix-f] | String; a grid mapping name from CF Appendix F. SOMaR uses **`latitude_longitude`** and **`azimuthal_equidistant`** | The type of coordinate reference system: geographic coordinates for point and trajectory data, an azimuthal equidistant projection for the local Cartesian grids (see [Georeferencing](georeferencing.md#time-bounded-local-grids)). | `"azimuthal_equidistant"` |
| `longitude_of_prime_meridian` | [CF][cf-appendix-f] | Number; degrees east | The longitude of the prime meridian of the geographic coordinate system. | `0.` |
| `semi_major_axis` | [CF][cf-appendix-f] | Number; meters | The semi-major axis of the reference ellipsoid. | `6378137.` |
| `inverse_flattening` | [CF][cf-appendix-f] | Number | The inverse flattening of the reference ellipsoid. | `298.257223563` |
| `longitude_of_projection_origin` | [CF][cf-azimuthal-equidistant] | Number; degrees east | Azimuthal equidistant only: the longitude of the origin of the local grid, i.e. of the radar at the start of the measurement. | `145.868167860183` |
| `latitude_of_projection_origin` | [CF][cf-azimuthal-equidistant] | Number; degrees north | Azimuthal equidistant only: the latitude of the origin of the local grid, i.e. of the radar at the start of the measurement. | `14.9952749946079` |
| `projected_crs_name` | [CF][cf-appendix-f] | String; free text | The name of the projected coordinate reference system. | `"WGS 84 / origin of coordinate system is radar location at measurement start time"` |
| `authority_string` | SOMaR | String; `<authority>:<code>` | An identifier of the coordinate reference system in a public registry. Not a CF attribute; given in addition to the CF attributes above, which remain the authoritative definition. | `"EPSG:4326"` |

[cf-standard-name]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#standard-name
[cf-long-name]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#long-name
[cf-units]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#units
[cf-description]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents
[cf-calendar]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#calendar
[cf-packed]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#packed-data
[cf-missing]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#missing-data
[cf-ancillary]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#ancillary-data
[cf-flags]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#flags
[cf-dsg]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#discrete-sampling-geometries
[cf-grid-mapping]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#grid-mappings-and-projections
[cf-appendix-f]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#appendix-grid-mappings
[cf-azimuthal-equidistant]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#azimuthal-equidistant
