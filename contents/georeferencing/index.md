---
title: Georeferencing
layout: default
nav_order: 5
---

# Georeferencing

## Polar sensor coordinates

[Level 1a data](../product_types/level1/level1a.md) and [Level 1b polar images](../product_types/level1/level1b_polar.md) are stored in the polar coordinates of the sensor, `range` and `azimuth`, with the radar antenna at the origin.
The `azimuth` variable holds the antenna angle as recorded by the radar relative to its zero direction; on a ship, this is typically the bow.
The elevation angle that FM 301 stores for every ray is not used, since a marine radar scans horizontally only.

They are located in space with variables from the WMO-CF Radial profile [FM 301][fm301] and the [CfRadial 2.1][cfradial] draft:

- Scalar `altitude` in the root group gives the height of the radar antenna above mean sea level; it is assumed constant for both fixed and moving platforms (FM 301).
- For a fixed platform, scalar `latitude` and `longitude` in the root group give the position of the radar antenna (FM 301).
- For a moving platform, platform position and orientation are recorded in `latitude`, `longitude`, and `heading` (CfRadial 2.1), provided either **per sweep** (at the start of each revolution) or **per pulse**:
  - **Level 1a**: stored in each sweep's `georeference` subgroup, either as scalars (per sweep) or with dimension `time` (per pulse; see [Level 1a data](../product_types/level1/level1a.md#moving-platforms)). In addition, FM 301 requires scalar `latitude` and `longitude` at file start in the root group.
  - **Level 1b polar**: stored in the root group with dimension `time` (per sweep) or `(time, azimuth)` (per pulse; see [Level 1b polar images](../product_types/level1/level1b_polar.md#position-and-heading)).

## Applying georeference corrections

In polar products ([Level 1a](../product_types/level1/level1a.md) and [Level 1b polar](../product_types/level1/level1b_polar.md)), `azimuth`, `range`, `time`, and platform position are stored as recorded by the instrument, and the corrections have not been applied.
Known offsets of the recorded pointing direction, range, time, and platform position are stored in the optional `georeference_correction` group in the root group (see [Georeference correction parameters](../metadata_attributes/georeference_correction.md)).
Users must apply these constant offsets to the recorded values to obtain corrected values; a missing variable is equivalent to a correction of 0:

- **Azimuth**: The azimuth of a pulse relative to true north, clockwise positive, is `azimuth + azimuth_correction + heading`.
- **Range**: The corrected slant range is `range + range_correction`. The ground range follows from the corrected slant range and the `altitude` of the antenna above the sea surface.
- **Time**: The corrected time is `time + time_correction`.
- **Platform position**: The antenna position is obtained by rotating `position_offset_x` and `position_offset_y` by the platform heading into eastward and northward displacements in meters, and converting these displacements to `latitude` and `longitude` on the WGS 84 ellipsoid (see [Position offset](#position-offset)).

In Cartesian products such as [Level 1b Cartesian](../product_types/level1/level1b_cartesian.md) and Level 2 products, these corrections have already been applied during grid generation, so this group is omitted.

## Position offset

Where the position of a moving platform has been taken from a GPS antenna at a different location on the platform, the recorded `latitude` and `longitude` are those of the GPS antenna.
`position_offset_x` and `position_offset_y` give the position of the radar antenna relative to the GPS antenna in a ship frame whose x-axis is positive to starboard and whose y-axis is positive toward the bow.
They replace the `latitude_correction` and `longitude_correction` of CfRadial 2.1, which are constant in degrees and therefore valid for a single heading only; an offset in the ship frame is independent of the heading.

With the heading `H`, the radar antenna is located

```
east  =  position_offset_x * cos(H) + position_offset_y * sin(H)
north = -position_offset_x * sin(H) + position_offset_y * cos(H)
```

meters east and north of the recorded position; the conversion to `latitude` and `longitude` is carried out on the WGS 84 ellipsoid.
The offsets are horizontal distances for a level ship; roll and pitch are neglected.
For a fixed platform, the position offsets are not used, and `latitude` and `longitude` in the root group give the position of the radar antenna.

## Coordinate reference system variables

Georeferenced data variables reference a scalar `char` coordinate reference system (CRS) variable, conventionally named `crs`, through a `grid_mapping` attribute, following standard CF practice. The `crs` variable's own attributes describe the projection:

- **Geographic coordinates** (the wave products and standard [near-surface current maps](../product_types/level2/current_maps.md), [bathymetric maps](../product_types/level2/depth_maps.md), and [sea ice drift maps](../product_types/level2/sea_ice_drift.md)): `grid_mapping_name = "latitude_longitude"`, specifying the reference ellipsoid (`longitude_of_prime_meridian`, `semi_major_axis`, `inverse_flattening`).
- **Cartesian image grids** (the [roughness images](../product_types/level2/roughness_images.md) and [roughness image mosaics](../product_types/level2/roughness_mosaics.md)): `grid_mapping_name = "azimuthal_equidistant"`, specifying the origin of the local grid (`longitude_of_projection_origin`, `latitude_of_projection_origin`), the reference ellipsoid, and a `projected_crs_name` (see [Time-bounded local grids](#time-bounded-local-grids)).
- **Local-grid Level 2 maps** (current, bathymetric, and sea ice drift maps in their [local-grid form](../product_types/level2/current_maps.md#local-grid-form)): use the same `azimuthal_equidistant` projection as the Cartesian images, but additionally store two-dimensional `longitude` and `latitude` auxiliary coordinates for the analysis windows (see [Positions of analysis windows](#positions-of-analysis-windows)).

All attributes of the `crs` variable are listed, with their origin and permitted values, under [Variable attributes](../metadata_attributes/variable_attributes.md#coordinate-reference-system-variables); for CDL examples of both systems, see [Example metadata](../metadata_attributes/example.md#coordinate-reference-system-variables).

## Time-bounded local grids

As introduced in the [Introduction](../introduction/index.md), SOMaR's Cartesian image products (e.g. Cartesian images, roughness images) are mapped onto a local, radar-centric grid whose origin is the position of the radar antenna at the start of each measurement, and which is therefore only valid for a limited time window. Rather than one global grid for the whole file, the roughness images and mosaics store each time-bounded grid as a sibling NetCDF group per time window, named `time_<YYYYMMDDHHMMSS>`, with its own `crs` and `x`/`y` coordinate variables.
The near-surface current, bathymetric, and sea ice drift maps are stored in groups of the same kind, one per measurement period, on a longitude/latitude grid or, for a processor that works on the local grid, on that grid together with two-dimensional `longitude` and `latitude` (see [Positions of analysis windows](#positions-of-analysis-windows)).
The [Level 1b Cartesian images](../product_types/level1/level1b_cartesian.md#position-and-orientation) are stored as one cube instead: all images share `x` and `y`, the origin of each image is given by `longitude` and `latitude` on the `time` dimension, and there is no `crs`, since a single `crs` variable can describe only one origin.

### Definition of the local grid

Marine radars measure natively in meters, as range and bearing from the antenna. The local grid keeps this geometry:

- `x` and `y` are distances in meters east and north of the origin, on a flat plane. The `y` axis points to true north, not to the grid north of any map projection.
- The origin is the position of the radar antenna at the start of the measurement, i.e. the concurrent GPS position after application of the [position offsets](#position-offset).

In CF terms, this plane is described as an azimuthal equidistant projection on the WGS 84 ellipsoid, centered on the origin (see [Azimuthal equidistant](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#azimuthal-equidistant) in the CF conventions). This projection preserves the distance and the bearing from its center, which are the two quantities the radar measures; at the ranges covered by a marine radar, it differs from a flat plane by less than a millimeter at 5 km.

### Group time variable

Each time-bounded grid carries a scalar `double` variable `time`, following CF conventions (`standard_name = "time"`, `calendar`, and `units = "seconds since 1970-01-01T00:00:00Z"`), that gives the start time of the measurement the grid belongs to. The name of a group, `time_<YYYYMMDDHHMMSS>`, repeats this time truncated (not rounded) to whole seconds.
Because a raw numeric `time` is hard to read, `time` may optionally carry a SOMaR-specific attribute `time_iso_8601` (see [Variable attributes](../metadata_attributes/variable_attributes.md)) with the same instant as an ISO 8601 UTC string, including fractional seconds, so that the start time of each group is human-readable without decoding the variable (see [Example metadata](../metadata_attributes/example.md#time-bounded-local-grid)).

## Positions of analysis windows

Level 2 products that report `longitude` and `latitude` directly (e.g. [near-surface current maps](../product_types/level2/current_maps.md), [bathymetric maps](../product_types/level2/depth_maps.md), [sea ice drift maps](../product_types/level2/sea_ice_drift.md), and the wave products) are retrieved within analysis windows.
Depending on the processor, the windows are placed on an Earth-fixed lattice in longitude and latitude or on the local grid, at known `x` and `y` distances east and north of the radar.
On an Earth-fixed lattice, a measurement period uses a single longitude spacing, so the current, bathymetric, and sea ice drift maps are rectangular grids with one-dimensional `latitude` and `longitude` coordinate variables.
On the local grid, these maps store `x` and `y` with the `crs` of the local grid, together with two-dimensional `longitude` and `latitude`, which are obtained by inverting the local projection defined above, i.e. the azimuthal equidistant projection on the WGS 84 ellipsoid centered on the position of the radar antenna at the start of the measurement.
The conversion must be carried out on the ellipsoid; a spherical approximation must not be used, since it can displace positions by up to about 0.5% of their distance from the radar.
The position stored is that of the center of the analysis window or, for the wave products, the mean position of the analysis windows contributing to a measurement.

### Radar position

So that the range and bearing of a measurement from the radar can be recovered, these products may optionally carry the radar position that served as the origin for each measurement, in the variables `radar_longitude` and `radar_latitude` (see [Example metadata](../metadata_attributes/example.md#radar-position)). For the current, bathymetric, and sea ice drift maps, they are scalar variables of each group; for the wave products, they have the dimension `time`.

[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
