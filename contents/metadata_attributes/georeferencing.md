---
title: Georeferencing
layout: default
parent: Metadata
nav_order: 5
---

# Georeferencing

## Polar sensor coordinates

[Level 1a data](../data_types/level1/level1a.md) and [Level 1b polar images](../data_types/level1/level1b.md#polar-image-sequences-pol3d) are stored in the polar coordinates of the sensor, `range` and `azimuth`, with the radar antenna at the origin.
They are located in space with the variables that the WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes) and, for moving platforms, the [CfRadial 2.1](https://github.com/NCAR/CfRadial/tree/master/docs) draft define for this purpose, rather than with a grid mapping:

- `latitude`, `longitude`, and `altitude`, in the root group, give the position of the radar antenna (FM 301). For a moving platform at Level 1a, they give the recorded position at the start of the file, which is that of the radar antenna only if `position_offset_x` and `position_offset_y` are 0.
- For a moving platform at Level 1a, the `georeference` subgroup of each sweep gives the `latitude`, `longitude`, and `heading` of the platform, either once per sweep, at the time of its first pulse, or for every pulse (CfRadial 2.1; see [Level 1a data](../data_types/level1/level1a.md#moving-platforms)).
- For a moving platform at Level 1b, `latitude`, `longitude`, and `heading` have the dimension `time` and give the values at the start of each revolution (see [Level 1b polar images](../data_types/level1/level1b.md#position-and-heading)).
- `azimuth_correction` and `range_correction`, in the `georeference_correction` group, give known offsets of the recorded azimuth and range (CfRadial 2.1; see [Radar parameters](radar_parameters.md#the-georeference_correction-group)).
- `time_correction`, in the same group, gives a known offset of the radar clock relative to GPS time (SOMaR; see [Radar parameters](radar_parameters.md#the-georeference_correction-group)).
- `position_offset_x` and `position_offset_y`, in the same group, give the position of the radar antenna relative to the GPS antenna in the ship frame, for a moving platform whose position is recorded at a different location than the radar (SOMaR; see [Position offset](radar_parameters.md#position-offset)).

The `azimuth` variable holds the antenna angle as recorded by the radar. The azimuth of a pulse relative to true north, clockwise positive, is

```
azimuth + azimuth_correction + heading
```

where a missing variable counts as 0, and the ground range follows from the slant range `range + range_correction` and the `altitude` of the antenna above the sea surface.
The position of the radar antenna is the recorded `latitude` and `longitude`, displaced by the position offsets after their rotation by the heading.
The elevation angle that FM 301 stores for every ray is not used, since a marine radar scans horizontally only.

## Coordinate reference system variables

Georeferenced data variables reference a scalar `char` coordinate reference system (CRS) variable, conventionally named `crs`, through a `grid_mapping` attribute, following standard CF practice. The `crs` variable's own attributes describe the projection:

- For data given directly in longitude and latitude (e.g. [near-surface current maps](../data_types/level2/current_maps.md), [bathymetric maps](../data_types/level2/depth_maps.md), [sea ice drift maps](../data_types/level2/sea_ice_drift.md), and the wave products), `grid_mapping_name = "latitude_longitude"`, together with the reference ellipsoid (`longitude_of_prime_meridian`, `semi_major_axis`, `inverse_flattening`) and an `authority_string` (e.g. an EPSG code).
- For Cartesian image grids stored one per group (the [roughness images](../data_types/level2/roughness_images.md) and [roughness image mosaics](../data_types/level2/roughness_mosaics.md), and the current, bathymetric, and sea ice drift maps in their [local-grid form](../data_types/level2/current_maps.md#local-grid-form)), `grid_mapping_name = "azimuthal_equidistant"`, with the origin of the local grid given by `longitude_of_projection_origin` and `latitude_of_projection_origin`, together with the reference ellipsoid and a `projected_crs_name` (see [Time-bounded local grids](#time-bounded-local-grids)).

All attributes of the `crs` variable are listed, with their origin and permitted values, under [Variable attributes](variable_attributes.md#coordinate-reference-system-variables).

```
char crs ;
        crs:grid_mapping_name = "latitude_longitude" ;
        crs:longitude_of_prime_meridian = 0. ;
        crs:semi_major_axis = 6378137. ;
        crs:inverse_flattening = 298.257223563 ;
        crs:authority_string = "EPSG:4326" ;
```

## Time-bounded local grids

As introduced in the [Introduction](../introduction/index.md), SOMaR's Cartesian image products (e.g. Cartesian images, roughness images) are mapped onto a local, radar-centric grid whose origin is the position of the radar antenna at the start of each measurement, and which is therefore only valid for a limited time window. Rather than one global grid for the whole file, the roughness images and mosaics store each time-bounded grid as a sibling NetCDF group per time window, named `time_<YYYYMMDDHHMMSS>`, with its own `crs` and `x`/`y` coordinate variables.
The near-surface current, bathymetric, and sea ice drift maps are stored in groups of the same kind, one per measurement period, on a longitude/latitude grid or, for a processor that works on the local grid, on that grid together with two-dimensional `longitude` and `latitude` (see [Positions of analysis windows](#positions-of-analysis-windows)).
The [Level 1b Cartesian images](../data_types/level1/level1b.md#position-and-orientation) are stored as one cube instead: all images share `x` and `y`, the origin of each image is given by `longitude` and `latitude` on the `time` dimension, and there is no `crs`, since a single `crs` variable can describe only one origin.

### Definition of the local grid

Marine radars measure natively in meters, as range and bearing from the antenna. The local grid keeps this geometry:

- `x` and `y` are distances in meters east and north of the origin, on a flat plane. The `y` axis points to true north, not to the grid north of any map projection.
- The origin is the position of the radar antenna at the start of the measurement, i.e. the concurrent GPS position after application of the [position offsets](radar_parameters.md#position-offset).

In CF terms, this plane is described as an azimuthal equidistant projection on the WGS 84 ellipsoid, centered on the origin (see [Azimuthal equidistant](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#azimuthal-equidistant) in the CF conventions). This projection preserves the distance and the bearing from its center, which are the two quantities the radar measures; at the ranges covered by a marine radar, it differs from a flat plane by less than a millimeter at 5 km.

```
char crs ;
        crs:grid_mapping_name = "azimuthal_equidistant" ;
        crs:longitude_of_projection_origin = 145.868167860183 ;
        crs:latitude_of_projection_origin = 14.9952749946079 ;
        crs:longitude_of_prime_meridian = 0. ;
        crs:semi_major_axis = 6378137. ;
        crs:inverse_flattening = 298.257223563 ;
        crs:projected_crs_name = "WGS 84 / origin of coordinate system is radar location at measurement start time" ;
```

Coordinates in other projected systems, such as UTM, are not stored, since they follow exactly from the `crs` variable. Data variables on a local grid reference it through `grid_mapping = "crs"`.

### Group time variable

Each time-bounded grid carries a scalar `double` variable `time`, following CF conventions (`standard_name = "time"`, `calendar`, and `units = "seconds since 1970-01-01T00:00:00Z"`), that gives the start time of the measurement the grid belongs to. The name of a group, `time_<YYYYMMDDHHMMSS>`, repeats this time truncated (not rounded) to whole seconds.
Because a raw numeric `time` is hard to read, `time` may optionally carry a SOMaR-specific attribute `time_iso_8601` (see [Variable attributes](variable_attributes.md)) with the same instant as an ISO 8601 UTC string, including fractional seconds, so that the start time of each group is human-readable without decoding the variable:

```
double time ;
        time:calendar = "standard" ;
        time:long_name = "start time of radar measurement" ;
        time:standard_name = "time" ;
        time:units = "seconds since 1970-01-01T00:00:00Z" ;
        time:time_iso_8601 = "2025-01-15T11:10:01.357666Z" ;
```

`time_iso_8601` is redundant with `time` and must agree with it. The start of the first group and the end of the last group are additionally given at file level by the global attributes `time_coverage_start` and `time_coverage_end` (see [Optional global attributes](optional_global.md)).

## Positions of analysis windows

Level 2 products that report `longitude` and `latitude` directly (e.g. [near-surface current maps](../data_types/level2/current_maps.md), [bathymetric maps](../data_types/level2/depth_maps.md), [sea ice drift maps](../data_types/level2/sea_ice_drift.md), and the wave products) are retrieved within analysis windows.
Depending on the processor, the windows are placed on an Earth-fixed lattice in longitude and latitude or on the local grid, at known `x` and `y` distances east and north of the radar.
On an Earth-fixed lattice, a measurement period uses a single longitude spacing, so the current, bathymetric, and sea ice drift maps are rectangular grids with one-dimensional `latitude` and `longitude` coordinate variables.
On the local grid, these maps store `x` and `y` with the `crs` of the local grid, together with two-dimensional `longitude` and `latitude`, which are obtained by inverting the local projection defined above, i.e. the azimuthal equidistant projection on the WGS 84 ellipsoid centered on the position of the radar antenna at the start of the measurement.
The conversion must be carried out on the ellipsoid; a spherical approximation must not be used, since it can displace positions by up to about 0.5% of their distance from the radar.
The position stored is that of the center of the analysis window or, for the wave products, the mean position of the analysis windows contributing to a measurement.

So that the range and bearing of a measurement from the radar can be recovered, these products may optionally carry the radar position that served as the origin for each measurement, in the variables `radar_longitude` and `radar_latitude`. For the current, bathymetric, and sea ice drift maps, they are scalar variables of each group; for the wave products, they have the dimension `time`:

```
double radar_longitude ;
        radar_longitude:long_name = "longitude of radar at start of measurement" ;
        radar_longitude:standard_name = "longitude" ;
        radar_longitude:units = "degrees_east" ;
double radar_latitude ;
        radar_latitude:long_name = "latitude of radar at start of measurement" ;
        radar_latitude:standard_name = "latitude" ;
        radar_latitude:units = "degrees_north" ;
```
