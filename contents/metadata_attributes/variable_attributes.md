---
title: Variable attributes
layout: default
parent: Metadata
nav_order: 3
---

# Variable attributes

Unlike file-level global attributes, the attributes listed below qualify individual variables.
Which attributes a given variable carries depends on the product type, as illustrated in the examples of the [Annex: Example products](../annex/index.md).

## Data and coordinate variables

These attributes define the physical meaning, units, valid ranges, and coordinate relationships of data and coordinate variables.

| Attribute | Values | Description |
|---|---|---|
| `_FillValue`<br><small>[CF][cf-missing]</small> | Same type as the variable | The value marking missing data. |
| `add_offset`<br><small>[CF][cf-packed]</small> | Number | Offset added to stored values after scaling. |
| `ancillary_variables`<br><small>[CF][cf-ancillary]</small> | String; blank-separated list of variable names | Variables that qualify this one, such as observation counts or quality flags. |
| `calendar`<br><small>[CF][cf-calendar]</small> | String; a CF calendar name. SOMaR uses **`standard`** | The calendar in which a time variable is expressed. |
| `cell_methods`<br><small>[CF][cf-cell-methods]</small> | String; `"<coordinate>: <method>"`, optionally followed by `" (comment: <text>)"`, e.g. `"time: mean"` | The statistic a value represents over its cell along one of the variable's coordinates, e.g. a time mean over the averaging window. A comment in parentheses may qualify the method, e.g. `"time: mean (comment: computed on linear power)"` for a mean stored in `dB`. Not used where the statistic runs over something that is not a coordinate of the variable, such as the spectral means `sea_surface_wave_mean_period` or `mean_wavenumber`. A scalar coordinate variable named here must also be listed in `coordinates`. |
| `cf_role`<br><small>[CF][cf-dsg]</small> | String; `trajectory_id` or `timeseries_id` | On the identifier variable of a [spatially averaged product](../product_types/spatially_averaged.md#moving-and-fixed-platforms), `trajectory` or `station`: marks it as the identifier of the trajectory or time series, in the sense of CF discrete sampling geometries. |
| `comment`<br><small>[CF][cf-description]</small> | String; free text | Additional information about the variable. |
| `coordinates`<br><small>[CF][cf-coordinates]</small> | String; blank-separated list of variable names | Auxiliary coordinate variables of a data variable. |
| `flag_masks`<br><small>[CF][cf-flags]</small> | List of values of the variable's type | The bits that can be set independently in a flag variable, used in place of `flag_values` where several conditions can hold at once. A value of 0 means that no condition holds. |
| `flag_meanings`<br><small>[CF][cf-flags]</small> | String; blank-separated list with one word per flag value or mask | The meaning of each entry in `flag_values` or `flag_masks`, in the same order. |
| `flag_values`<br><small>[CF][cf-flags]</small> | List of values of the variable's type | The values a flag variable can take. |
| `grid_mapping`<br><small>[CF][cf-grid-mapping]</small> | String; the name of a coordinate reference system variable, conventionally `crs` | Links a data variable to the variable describing the coordinate reference system of its coordinates (see [Coordinate reference system variables](#coordinate-reference-system-variables)). |
| `long_name`<br><small>[CF][cf-long-name]</small> | String; free text | A human-readable description of the variable. |
| `references`<br><small>[CF][cf-description]</small> | String; free text | Published or web-based references that describe the data or methods used. |
| `sampling_frequency`<br><small>SOMaR</small> | Number; `s-1` | Optional, on variables that hold recorded navigation data (`latitude`, `longitude`, and `heading` of a moving platform): the frequency at which the instrument sampled them, before they were matched to sweeps or rays. |
| `scale_factor`<br><small>[CF][cf-packed]</small> | Number | Factor by which stored values are multiplied to unpack them. |
| `source`<br><small>[CF][cf-description]</small> | String; free text | Optional. The method of production of the variable's values, where it differs from that given by the global attribute `source`, which the variable attribute then overrides; on navigation variables, the instrument they are taken from, e.g. a GNSS receiver or a gyrocompass. |
| `standard_name`<br><small>[CF][cf-standard-name]</small> | String; a name from the CF standard name table | Identifies the physical quantity. Given wherever a suitable CF standard name exists. A variable with a standard name is named after it, unless another convention fixes the name (e.g. `heading`, `x`, `y`), another variable in the same group already holds that name (e.g. `radar_latitude`, `eastward_sea_ice_velocity_backward`), or the standard name is generic (e.g. `quality_flag` for `measurement_quality`). |
| `time_iso_8601`<br><small>SOMaR</small> | String; ISO 8601 date and time in UTC, fractional seconds permitted | Optional, on the scalar `time` variable of a time-bounded grid: the same instant as the variable's value in human-readable form. |
| `units`<br><small>[CF][cf-units]</small> | String; a unit recognized by UDUNITS, or `dB` for uncalibrated logarithmic backscatter | The unit of the stored values. Variables use SI symbols (`m`, `degree`, `s`) in accordance with CF conventions and UDUNITS. Time variables use `"seconds since 1970-01-01T00:00:00Z"` (UNIX time). Uncalibrated radar backscatter uses `"1"` (linear) or `"dB"` (logarithmic). `dB` is not a UDUNITS unit, so generic CF checkers may flag it; SOMaR accepts it for consistency with FM 301. |
| `valid_range`<br><small>[CF][cf-missing]</small> | Two numbers of the variable's type: minimum, maximum | The smallest and largest valid values. |
{: .attribute-table }

## Coordinate reference system variables

These attributes are carried by coordinate reference system variables (conventionally `crs`) that `grid_mapping` refers to. Under [CF conventions][cf-grid-mapping], `crs` is a scalar container variable that holds projection metadata in its attributes and carries no data values.

| Attribute | Values | Description |
|---|---|---|
| `geographic_crs_name`<br><small>[CF][cf-appendix-f]</small> | String; a name per CF Appendix F. SOMaR uses **`WGS 84`** | The name of the geographic coordinate reference system, as in OGC WKT. Given together with `horizontal_datum_name`, `prime_meridian_name`, and `reference_ellipsoid_name`. |
| `grid_mapping_name`<br><small>[CF][cf-appendix-f]</small> | String; a grid mapping name from CF Appendix F. SOMaR uses **[`latitude_longitude`][cf-latitude-longitude]** and **[`azimuthal_equidistant`][cf-azimuthal-equidistant]** | The type of coordinate reference system: geographic coordinates for longitude/latitude grids and series, an azimuthal equidistant projection for the local Cartesian grids (see [Georeferencing](../georeferencing/index.md#time-bounded-local-grids)). |
| `horizontal_datum_name`<br><small>[CF][cf-appendix-f]</small> | String; a datum name per CF Appendix F. SOMaR uses **`World Geodetic System 1984`** | The name of the geodetic datum. Given together with `geographic_crs_name`, `prime_meridian_name`, and `reference_ellipsoid_name`. |
| `inverse_flattening`<br><small>[CF][cf-appendix-f]</small> | Number | The inverse flattening of the reference ellipsoid. |
| `latitude_of_projection_origin`<br><small>[CF][cf-azimuthal-equidistant]</small> | Number; degrees north | Azimuthal equidistant only: the latitude of the origin of the local grid, i.e. of the radar at the start of the measurement. |
| `longitude_of_prime_meridian`<br><small>[CF][cf-appendix-f]</small> | Number; degrees east | The longitude of the prime meridian of the geographic coordinate system. |
| `longitude_of_projection_origin`<br><small>[CF][cf-azimuthal-equidistant]</small> | Number; degrees east | Azimuthal equidistant only: the longitude of the origin of the local grid, i.e. of the radar at the start of the measurement. |
| `prime_meridian_name`<br><small>[CF][cf-appendix-f]</small> | String; a name per CF Appendix F. SOMaR uses **`Greenwich`** | The name of the prime meridian. Given together with `geographic_crs_name`, `horizontal_datum_name`, and `reference_ellipsoid_name`. |
| `reference_ellipsoid_name`<br><small>[CF][cf-appendix-f]</small> | String; a name per CF Appendix F. SOMaR uses **`WGS 84`** | The name of the reference ellipsoid. Given together with `geographic_crs_name`, `horizontal_datum_name`, and `prime_meridian_name`. |
| `semi_major_axis`<br><small>[CF][cf-appendix-f]</small> | Number; m | The semi-major axis of the reference ellipsoid. |
{: .attribute-table }

For examples of both coordinate reference systems in NetCDF CDL format, see [Georeferencing](../georeferencing/index.md#coordinate-reference-system-variables).

[cf-standard-name]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#standard-name
[cf-long-name]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#long-name
[cf-units]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#units
[cf-description]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents
[cf-coordinates]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#coordinate-system
[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cf-calendar]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#calendar
[cf-cell-methods]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#cell-methods
[cf-dsg]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#discrete-sampling-geometries
[cf-packed]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#packed-data
[cf-missing]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#missing-data
[cf-ancillary]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#ancillary-data
[cf-flags]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#flags
[cf-grid-mapping]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#grid-mappings-and-projections
[cf-appendix-f]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#appendix-grid-mappings
[cf-latitude-longitude]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#_latitude_longitude
[cf-azimuthal-equidistant]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#azimuthal-equidistant
