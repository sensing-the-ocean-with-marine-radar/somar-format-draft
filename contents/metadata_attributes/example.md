---
title: Example metadata
layout: default
parent: Metadata
nav_order: 5
---

# Example metadata

This page illustrates how the shared metadata described in this chapter—global attributes, coordinate reference systems, group time, and radar position—appear in NetCDF CDL format in a SOMaR product.

## File-level metadata

The root group carries the [mandatory global attributes](mandatory_global.md) and any applicable [optional global attributes](optional_global.md):

```
// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "currents" ;
                :creator_email = "famous.scientist@frori.org" ;
                :creator_name = "Dr. Famous Scientist" ;
                :date_created = "2025-01-15T12:05:00Z" ;
                :geospatial_lat_max = 15.03 ;
                :geospatial_lat_min = 14.9265 ;
                :geospatial_lon_max = 145.96815 ;
                :geospatial_lon_min = 145.8426 ;
                :history = "20250115T120500Z: File creation time" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :institution_id = "https://ror.org/02dgjyy92" ;
                :instrument = "Helmholtz-Zentrum Hereon coherent-on-receive marine X-band radar" ;
                :license = "Creative Commons Attribution 4.0 International Public License (CC BY 4.0)" ;
                :platform = "R/V Ocean Research" ;
                :platform_is_mobile = "true" ;
                :processing_level = "L2a" ;
                :processing_software = "FRORI X-band radar processing software version 2.5.0 written in Python 3.13.6" ;
                :source = "Shipboard marine X-band radar" ;
                :summary = "The near-surface current vectors are obtained through least-squares fits ..." ;
                :time_coverage_end = "2025-01-15T12:00:00.775429Z" ;
                :time_coverage_start = "2025-01-15T11:10:01.357666Z" ;
                :title = "Marine X-band radar near-surface current measurements with quality control flag from R/V Ocean Research" ;
```

## Coordinate reference system variables

Georeferenced data variables link to a coordinate reference system (CRS) variable through their `grid_mapping` attribute (see [Georeferencing](../georeferencing/index.md#coordinate-reference-system-variables) and [Variable attributes](variable_attributes.md#coordinate-reference-system-variables)).

### Geographic coordinates (EPSG:4326)

Used by wave products and standard Level 2 maps on an Earth-fixed longitude/latitude grid:

```
char crs ;
        crs:grid_mapping_name = "latitude_longitude" ;
        crs:longitude_of_prime_meridian = 0. ;
        crs:semi_major_axis = 6378137. ;
        crs:inverse_flattening = 298.257223563 ;
        crs:authority_string = "EPSG:4326" ;
```

### Local Cartesian grid (azimuthal equidistant)

Used by time-bounded Cartesian image products (roughness images and mosaics) and local-grid Level 2 maps, centered on the radar position at the start of each measurement (see [Time-bounded local grids](../georeferencing/index.md#time-bounded-local-grids)):

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

## Group time variable

Each time-bounded grid carries a scalar `time` variable giving the measurement start time, optionally complemented by `time_iso_8601` (see [Group time variable](../georeferencing/index.md#group-time-variable)):

```
double time ;
        time:calendar = "standard" ;
        time:long_name = "start time of radar measurement" ;
        time:standard_name = "time" ;
        time:units = "seconds since 1970-01-01T00:00:00Z" ;
        time:time_iso_8601 = "2025-01-15T11:10:01.357666Z" ;
```

## Positions of analysis windows

Level 2 products retrieved within analysis windows may optionally record the radar position that served as the origin for each measurement (see [Positions of analysis windows](../georeferencing/index.md#positions-of-analysis-windows)):

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
