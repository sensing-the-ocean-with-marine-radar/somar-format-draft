---
title: Variable attributes
layout: default
parent: Metadata
nav_order: 3
---

# Variable attributes

The tables below list the attributes that SOMaR files attach to individual variables, as opposed to the file as a whole.
Which of them a given variable carries depends on the product and is shown in the minimal example on each product's page; where an attribute has a fixed set of permitted values, all of them are listed and those currently used by SOMaR are set in bold.

## Data and coordinate variables

| Attribute | Values | Description |
|---|---|---|
| `standard_name`<br><small>[CF][cf-standard-name]</small> | String; a name from the CF standard name table | Identifies the physical quantity. Given wherever a suitable CF standard name exists. |
| `long_name`<br><small>[CF][cf-long-name]</small> | String; free text | A human-readable description of the variable. |
| `units`<br><small>[CF][cf-units]</small> | String; a unit recognized by UDUNITS | The unit of the stored values. Time variables use `"seconds since 1970-01-01T00:00:00Z"` (UNIX time). Uncalibrated radar backscatter uses `"1"` (linear) or `"dB"` (logarithmic). |
| `comment`<br><small>[CF][cf-description]</small> | String; free text | Additional information about the variable. Required on Level 1 backscatter variables to state whether the stored quantity is an amplitude or a power (see [Radar parameters](radar_parameters.md)). |
| `calendar`<br><small>[CF][cf-calendar]</small> | String; a CF calendar name. SOMaR uses **`standard`** | The calendar in which a time variable is expressed. |
| `scale_factor`<br><small>[CF][cf-packed]</small> | Number | Factor by which stored values are multiplied to unpack them. |
| `add_offset`<br><small>[CF][cf-packed]</small> | Number | Offset added to stored values after scaling. |
| `_FillValue`<br><small>[CF][cf-missing]</small> | Same type as the variable | The value marking missing data. |
| `valid_range`<br><small>[CF][cf-missing]</small> | Two numbers of the variable's type: minimum, maximum | The smallest and largest valid values. |
| `ancillary_variables`<br><small>[CF][cf-ancillary]</small> | String; blank-separated list of variable names | Variables that qualify this one, such as observation counts or quality flags. |
| `flag_values`<br><small>[CF][cf-flags]</small> | List of values of the variable's type | The values a flag variable can take. |
| `flag_meanings`<br><small>[CF][cf-flags]</small> | String; blank-separated list with one word per flag value | The meaning of each entry in `flag_values`, in the same order. |
| `coordinates`<br><small>[CF][cf-coordinates]</small> | String; blank-separated list of variable names | Auxiliary coordinate variables of a data variable. On Level 1a data variables it is set to `"azimuth range"`; FM 301 prescribes `"elevation azimuth range"`, but SOMaR does not use elevation. |
| `time_iso_8601`<br><small>SOMaR</small> | String; ISO 8601 date and time in UTC, fractional seconds permitted | Optional, on the scalar `time` variable of a time-bounded grid: the same instant as the variable's value in human-readable form. |
| `grid_mapping`<br><small>[CF][cf-grid-mapping]</small> | String; the name of a coordinate reference system variable, conventionally `crs` | Links a data or coordinate variable to the variable describing its coordinate reference system. |
{: .attribute-table }

## Coordinate reference system variables

These attributes are carried by the scalar coordinate reference system variables (conventionally `crs`) that `grid_mapping` refers to.

| Attribute | Values | Description |
|---|---|---|
| `grid_mapping_name`<br><small>[CF][cf-appendix-f]</small> | String; a grid mapping name from CF Appendix F. SOMaR uses **`latitude_longitude`** and **`azimuthal_equidistant`** | The type of coordinate reference system: geographic coordinates for point data, an azimuthal equidistant projection for the local Cartesian grids (see [Georeferencing](georeferencing.md#time-bounded-local-grids)). |
| `longitude_of_prime_meridian`<br><small>[CF][cf-appendix-f]</small> | Number; degrees east | The longitude of the prime meridian of the geographic coordinate system. |
| `semi_major_axis`<br><small>[CF][cf-appendix-f]</small> | Number; meters | The semi-major axis of the reference ellipsoid. |
| `inverse_flattening`<br><small>[CF][cf-appendix-f]</small> | Number | The inverse flattening of the reference ellipsoid. |
| `longitude_of_projection_origin`<br><small>[CF][cf-azimuthal-equidistant]</small> | Number; degrees east | Azimuthal equidistant only: the longitude of the origin of the local grid, i.e. of the radar at the start of the measurement. |
| `latitude_of_projection_origin`<br><small>[CF][cf-azimuthal-equidistant]</small> | Number; degrees north | Azimuthal equidistant only: the latitude of the origin of the local grid, i.e. of the radar at the start of the measurement. |
| `projected_crs_name`<br><small>[CF][cf-appendix-f]</small> | String; free text | The name of the projected coordinate reference system. |
| `authority_string`<br><small>SOMaR</small> | String; `<authority>:<code>` | An identifier of the coordinate reference system in a public registry. Not a CF attribute; given in addition to the CF attributes above, which remain the authoritative definition. |
{: .attribute-table }

[cf-standard-name]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#standard-name
[cf-long-name]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#long-name
[cf-units]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#units
[cf-description]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents
[cf-coordinates]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#coordinate-system
[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cf-calendar]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#calendar
[cf-packed]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#packed-data
[cf-missing]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#missing-data
[cf-ancillary]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#ancillary-data
[cf-flags]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#flags
[cf-grid-mapping]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#grid-mappings-and-projections
[cf-appendix-f]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#appendix-grid-mappings
[cf-azimuthal-equidistant]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#azimuthal-equidistant
