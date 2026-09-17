---
title: Georeferencing
layout: default
parent: Metadata attributes
nav_order: 5
---

# Georeferencing

## Trajectory identification

Since every SOMaR Level 1b and Level 2 product is defined along a moving platform's track, files with `featureType = "trajectory"` (see [Mandatory global attributes](mandatory_global.md)) must carry a companion scalar `char` variable named `trajectory`, marked with `cf_role = "trajectory_id"`, identifying the trajectory to which the file's data belong:

```
char trajectory ;
        trajectory:cf_role = "trajectory_id" ;
        trajectory:long_name = "Current measurements along R/V Ocean Research trajectory" ;
```

## Coordinate reference system variables

Georeferenced data variables reference a scalar `char` coordinate reference system (CRS) variable, conventionally named `crs`, through a `grid_mapping` attribute, following standard CF practice. The `crs` variable's own attributes describe the projection:

- For point/trajectory data given directly as longitude/latitude (e.g. [near-surface current maps](../data_types/level2/gridded/current_maps.md), [bathymetric maps](../data_types/level2/gridded/depth_maps.md), [sea ice drift maps](../data_types/level2/gridded/sea_ice_drift.md), and the wave products), `grid_mapping_name = "latitude_longitude"`, together with the reference ellipsoid (`longitude_of_prime_meridian`, `semi_major_axis`, `inverse_flattening`) and an `authority_string` (e.g. an EPSG code).
- For Cartesian image grids (e.g. [Cartesian images](../data_types/level1/level1b.md), [roughness images](../data_types/level2/gridded/roughness_images.md)), `grid_mapping_name = "transverse_mercator"`, with the local projection defined by `longitude_of_projection_origin`, `latitude_of_projection_origin`, `scale_factor_at_central_meridian`, and (where relevant) `false_easting`/`false_northing`, plus `projected_crs_name`.

```
char crs ;
        crs:grid_mapping_name = "latitude_longitude" ;
        crs:longitude_of_prime_meridian = 0. ;
        crs:semi_major_axis = 6378137. ;
        crs:inverse_flattening = 298.257223563 ;
        crs:authority_string = "EPSG:4326" ;
```

## Time-bounded local grids

As introduced in the [Introduction](../introduction/index.md), SOMaR's Cartesian image products (e.g. Cartesian images, roughness images) are mapped onto a local, radar-centric grid whose origin is the platform's position at the start of each measurement, and which is therefore only valid for a limited time window. Rather than one global grid for the whole file, each time-bounded grid is stored with its own `crs` and `x`/`y` coordinate variables, either directly (one grid per file, as in Cartesian images) or as a sibling NetCDF group per time window within one file (as in roughness images, where each group is named `time_<YYYYMMDDHHMMSS>`).

Some products additionally provide a second, fixed-frame CRS alongside the primary radar-centric one — for example roughness images carry both a local `crs` and a UTM `crs_utm`, with corresponding `x`/`y` and `x_utm`/`y_utm` coordinate variables, so that a grid can be related to a location-independent frame without recomputing the projection. Where a variable is referenced to more than one CRS like this, its `grid_mapping` attribute lists each CRS variable together with the coordinate variables it applies to, space-separated:

```
grid_mapping = "crs: x y crs_utm: x_utm y_utm" ;
```

This compound, multi-mapping form of `grid_mapping` is a SOMaR-specific extension: standard CF only defines a single grid mapping per variable. It is only used where a variable is genuinely dual-referenced; a variable tied to a single CRS uses the plain CF form, `grid_mapping = "crs"`.
