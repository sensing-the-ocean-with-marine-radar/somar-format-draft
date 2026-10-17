---
title: Georeferencing
layout: default
nav_order: 4
---

# Georeferencing

## Polar sensor coordinates

[Level 1a data](../product_types/level1/level1a.md) and [Level 1b polar images](../product_types/level1/level1b_polar.md) are stored in the polar coordinates of the sensor, `range` and `azimuth`, with the radar antenna at the origin.
The `azimuth` variable holds the antenna angle as recorded by the radar relative to its zero direction; on a ship, this is typically the bow.
This differs from FM 301, which defines `azimuth` relative to true north; SOMaR polar data are stored as recorded without modification.
The elevation angle that FM 301 stores for every ray is not used, since a marine radar scans horizontally only.

Whether the platform moves is stated by the global attribute [`platform_is_mobile`](../metadata_attributes/optional_global.md) (`"true"` or `"false"`; assumed `"false"` if missing).

They are located in space with variables from the WMO-CF Radial profile [FM 301][fm301] and the [CfRadial 2.1][cfradial] draft:

- Scalar `altitude` in the root group gives the height of the radar antenna above mean sea level (FM 301). SOMaR assumes it constant for both fixed and moving platforms, whereas CfRadial 2.1 also allows `altitude(time)` in the `georeference` group.
- For a fixed platform, scalar `latitude` and `longitude` in the root group give the position of the radar antenna (FM 301).
- For a moving platform (`platform_is_mobile = "true"`), platform position and orientation are recorded in `latitude` (double; `degrees_north`), `longitude` (double; `degrees_east`), and `heading` (float; `degree`, standard name `platform_orientation`), following CfRadial 2.1 (Section 5.4). All navigation variables within a group or subgroup must use the same representation, provided either **per sweep** (scalar at the start of each revolution, i.e. at the time of its first pulse; a SOMaR addition, as CfRadial defines them per ray only) or **per pulse** (dimension `time`, keeping the full resolution of navigation data as in CfRadial). FM 301 and CfRadial index `time` by ray; at Level 1a, where each stored pulse is one ray (`n_samples` = 1 unless the radar itself averages pulses), the two are the same:
  - **Level 1a**: stored in each sweep's `georeference` subgroup, either as scalars (per sweep) or with dimension `time` (per pulse; see [Level 1a data](../product_types/level1/level1a.md#moving-platforms)). In addition, FM 301 requires scalar `latitude` and `longitude` at file start in the root group.
  - **Level 1b polar**: stored in the root group with dimension `time` (per sweep) or `(time, azimuth)` (per pulse; see [Level 1b polar images](../product_types/level1/level1b_polar.md#position-and-heading)).

## Applying georeference corrections

In polar products ([Level 1a](../product_types/level1/level1a.md) and [Level 1b polar](../product_types/level1/level1b_polar.md)), `azimuth`, `range`, `time`, and platform position are stored as recorded by the instrument, and the corrections have not been applied.
Known offsets of the recorded pointing direction, range, time, and platform position are stored in the optional `georeference_correction` group in the root group (see [Georeference correction parameters](../metadata_attributes/georeference_correction.md)).
The azimuth, range, and time offsets of a ship-borne radar can be estimated from the imagery itself (McCann and Bell [2018](../references/index.md#mccann-bell-2018)).
Users must apply these constant offsets to the recorded values to obtain corrected values; a missing variable is equivalent to a correction of 0:

- **Azimuth**: The azimuth of a pulse relative to true north, clockwise positive, is `(azimuth + azimuth_correction + heading) mod 360`, where `heading` is taken from the navigation variables (the `georeference` subgroup at Level 1a or the root group at Level 1b polar) and `azimuth_correction` from the `georeference_correction` group. For a fixed platform, there is no `heading`, and `azimuth_correction` is the direction of the radar's zero direction relative to true north. With per-sweep navigation, the heading at the start of the sweep is applied to all its pulses, which is an approximation while the ship turns.
- **Range**: The corrected slant range $R_s$ is `range + range_correction`. The ground range $R_g$ follows from the corrected slant range and the antenna height $h$ (`altitude`) above mean sea level as $R_g = \sqrt{R_s^2 - h^2}$ for $R_s \ge h$. Range gates where $R_s \lt h$ fall inside the platform near-field or nadir blind zone, do not intersect the sea surface, and are left unmapped or set to the `_FillValue` when projecting to horizontal coordinates.
- **Time**: The corrected time is `time + time_correction`.
- **Platform position**:<a id="position-offset"></a> Where the position of a moving platform has been taken from a GPS antenna at a different location on the platform, `position_offset_x` and `position_offset_y` give the position of the radar antenna relative to the GPS antenna in a ship frame (x-axis positive to starboard, y-axis positive toward the bow). With heading $H$ (in degrees clockwise from true north, converted to radians for trigonometric evaluation), the radar antenna's displacement in meters east and north of the recorded position is:

    ```
    east  =  position_offset_x * cos(H) + position_offset_y * sin(H)
    north = -position_offset_x * sin(H) + position_offset_y * cos(H)
    ```

    The conversion to `latitude` and `longitude` is carried out on the WGS 84 ellipsoid. The offsets are horizontal distances for a level ship (roll and pitch are neglected); for a fixed platform, position offsets are not used. They replace the `latitude_correction` and `longitude_correction` of CfRadial 2.1, which are constant in degrees and therefore valid for a single heading only.

In Cartesian products such as [Level 1b Cartesian](../product_types/level1/level1b_cartesian.md) and Level 2 products, these corrections have already been applied during grid generation, so this group is omitted.

## Coordinate reference system variables

Georeferenced data variables reference a scalar `char` coordinate reference system (CRS) variable, conventionally named `crs`, through a `grid_mapping` attribute, following standard CF practice.
All attributes of the `crs` variable are listed, with their origin and permitted values, under [Variable attributes](../metadata_attributes/variable_attributes.md#coordinate-reference-system-variables).

SOMaR uses two coordinate reference systems:

### Geographic coordinates

Used by wave products and standard Level 2 maps ([near-surface current maps](../product_types/level2/current_maps.md), [bathymetric maps](../product_types/level2/depth_maps.md), and [sea ice drift maps](../product_types/level2/sea_ice_drift.md)) on an Earth-fixed longitude/latitude grid.
The `crs` variable specifies `grid_mapping_name = "latitude_longitude"` (see [Latitude-longitude](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#_latitude_longitude) in the CF conventions), describes the reference ellipsoid (`longitude_of_prime_meridian`, `semi_major_axis`, `inverse_flattening`), and names the geodetic datum (`horizontal_datum_name`):

```
variables:
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
data:
        crs = " " ;
```

### Time-bounded local grids

Marine radars measure natively in meters, as range and bearing from the antenna. Cartesian image products ([roughness images](../product_types/level2/roughness_images.md) and [roughness image mosaics](../product_types/level2/roughness_mosaics.md)) and local-grid [Level 2 maps](../product_types/level2/current_maps.md#local-grid-form) preserve this geometry on a radar-centric grid:

- `x` and `y` are distances in meters east and north of the origin, on a flat plane. The `y` axis points to true north, not to the grid north of any map projection.
- The origin is the position of the radar antenna at the start of the measurement, i.e. the concurrent GPS position after application of the [position offsets](#position-offset).

In CF terms, this plane is described as an azimuthal equidistant projection on the WGS 84 ellipsoid, centered on the origin (see [Azimuthal equidistant](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#azimuthal-equidistant) in the CF conventions). This projection preserves distance and bearing from its center, differing from a flat plane by less than a millimeter at 5 km. The `crs` variable specifies `grid_mapping_name = "azimuthal_equidistant"`, the origin (`longitude_of_projection_origin`, `latitude_of_projection_origin`), the reference ellipsoid, and the name of the geodetic datum. Each time-bounded grid also carries a scalar `time` giving the start of the measurement:

```
variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 145.868167860183 ;
                crs:latitude_of_projection_origin = 14.9952749946079 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T11:00:31.417000Z" ;
data:
        crs = " " ;
        time = 1736938831.417 ;
```

Because the origin changes as a platform moves, each local grid is valid only for a limited time window. Rather than one global grid for the whole file, roughness images, mosaics, and local-grid Level 2 maps store each time-bounded grid as a sibling NetCDF group named `time_<YYYYMMDDHHMMSS>`, with its own `crs` and coordinate variables:
- Each group carries a scalar `double` variable `time` giving the start time of the measurement (`units = "seconds since 1970-01-01T00:00:00Z"`), optionally complemented by a human-readable `time_iso_8601` string (see [Variable attributes](../metadata_attributes/variable_attributes.md)).
- Local-grid Level 2 maps additionally store two-dimensional `longitude` and `latitude` auxiliary coordinates for their analysis windows (see [Positions of analysis windows](#positions-of-analysis-windows)).

[Level 1b Cartesian images](../product_types/level1/level1b_cartesian.md#position-and-orientation) are stored as one cube instead: all images share `x` and `y`, the origin of each image is given by `longitude` and `latitude` on the `time` dimension, and there is no `crs`, since a single `crs` variable can describe only one origin.

## Positions of analysis windows

Level 2 products that report `longitude` and `latitude` directly (e.g. [near-surface current maps](../product_types/level2/current_maps.md), [bathymetric maps](../product_types/level2/depth_maps.md), [sea ice drift maps](../product_types/level2/sea_ice_drift.md), and the wave products) are retrieved within analysis windows.
Depending on the processor, the windows are placed on an Earth-fixed lattice in longitude and latitude or on the local grid, at known `x` and `y` distances east and north of the radar.
On an Earth-fixed lattice, a measurement period uses a single longitude spacing, so the current, bathymetric, and sea ice drift maps are rectangular grids with one-dimensional `latitude` and `longitude` coordinate variables.
On the local grid, these maps store `x` and `y` with the `crs` of the local grid, together with two-dimensional `longitude` and `latitude`, which are obtained by inverting the local projection defined above, i.e. the azimuthal equidistant projection on the WGS 84 ellipsoid centered on the position of the radar antenna at the start of the measurement.
The conversion must be carried out on the ellipsoid; a spherical approximation must not be used, since it can displace positions by up to about 0.5% of their distance from the radar.
The stored position is that of the center of the analysis window or, for wave products, the mean position of the analysis windows contributing to a measurement.

<a id="radar-position"></a>To allow recovering the range and bearing of a measurement from the radar, these products may optionally carry the radar position that served as the origin for each measurement, in the variables `radar_longitude` and `radar_latitude` . For current, bathymetric, and sea ice drift maps, they are scalar variables of each group; for wave products, they have the dimension `time`.

```
variables:
        double radar_longitude ;
                radar_longitude:long_name = "longitude of radar at start of measurement" ;
                radar_longitude:standard_name = "longitude" ;
                radar_longitude:units = "degrees_east" ;
        double radar_latitude ;
                radar_latitude:long_name = "latitude of radar at start of measurement" ;
                radar_latitude:standard_name = "latitude" ;
                radar_latitude:units = "degrees_north" ;
data:
        radar_longitude = 145.86816786 ;
        radar_latitude = 14.99527499 ;
```

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
