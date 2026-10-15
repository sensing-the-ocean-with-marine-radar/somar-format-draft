---
title: Example metadata
layout: default
parent: Metadata
nav_order: 6
---

# Example metadata

This page illustrates how shared metadata (i.e. global attributes, coordinate reference systems, radar position, radar parameters, and georeference corrections) appear in NetCDF CDL format in a SOMaR product.

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
                :institution_id = "https://ror.org/01abcde23" ;
                :instrument = "Famous Radar Ocean Research Institute coherent-on-receive marine X-band radar" ;
                :license = "Creative Commons Attribution 4.0 International Public License (CC BY 4.0)" ;
                :platform = "R/V Ocean Research" ;
                :platform_is_mobile = "true" ;
                :processing_level = "L2a" ;
                :processing_software = "FRORI X-band radar processing software version 2.5.0 (Python 3.13.6)" ;
                :source = "Shipboard marine X-band radar" ;
                :summary = "The near-surface current vectors are obtained through least-squares fits ..." ;
                :time_coverage_end = "2025-01-15T12:00:00.775429Z" ;
                :time_coverage_start = "2025-01-15T11:10:01.357666Z" ;
                :title = "Marine X-band radar near-surface current measurements with quality control flag from R/V Ocean Research" ;
```

## Coordinate reference system variables

Georeferenced data variables link to a coordinate reference system (CRS) variable through their `grid_mapping` attribute (see [Georeferencing](../georeferencing/index.md#coordinate-reference-system-variables) and [Variable attributes](variable_attributes.md#coordinate-reference-system-variables)).

### Geographic coordinates (WGS 84)

Used by wave products and standard Level 2 maps on an Earth-fixed longitude/latitude grid:

```
char crs ;
        crs:grid_mapping_name = "latitude_longitude" ;
        crs:longitude_of_prime_meridian = 0. ;
        crs:semi_major_axis = 6378137. ;
        crs:inverse_flattening = 298.257223563 ;
```

### Time-bounded local grid (azimuthal equidistant)

Used by time-bounded Cartesian image products (roughness images and mosaics) and local-grid Level 2 maps, centered on the radar position at the start of each measurement (see [Time-bounded local grids](../georeferencing/index.md#time-bounded-local-grids)). Each time-bounded grid carries a scalar `time` variable giving the measurement start time, optionally complemented by `time_iso_8601` (see [Group time variable](../georeferencing/index.md#group-time-variable)):

```
char crs ;
        crs:grid_mapping_name = "azimuthal_equidistant" ;
        crs:longitude_of_projection_origin = 145.868167860183 ;
        crs:latitude_of_projection_origin = 14.9952749946079 ;
        crs:longitude_of_prime_meridian = 0. ;
        crs:semi_major_axis = 6378137. ;
        crs:inverse_flattening = 298.257223563 ;
        crs:projected_crs_name = "WGS 84 / origin of coordinate system is radar location at measurement start time" ;
double time ;
        time:calendar = "standard" ;
        time:long_name = "start time of radar measurement" ;
        time:standard_name = "time" ;
        time:units = "seconds since 1970-01-01T00:00:00Z" ;
        time:time_iso_8601 = "2025-01-15T11:10:01.357666Z" ;
```

## Radar position

Level 2 products retrieved within analysis windows may optionally record the radar position that served as the origin for each measurement (see [Radar position](../georeferencing/index.md#radar-position)):

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

## Radar parameters

Technical parameters of the radar are stored as variables (see [Radar parameters](radar_parameters.md)).

### Pulse and scan parameters

Parameters describing the pulse and scan are stored in each sweep group. They are typically constant over a sweep and stored as scalars, but may carry the dimension `time` if they vary from pulse to pulse:

```
variables:
        float frequency ;
                frequency:units = "s-1" ;
                frequency:long_name = "operating frequency of the radar" ;
        string polarization_mode ;
        float pulse_width ;
                pulse_width:units = "s" ;
                pulse_width:long_name = "length of the transmitted pulse" ;
        float prt ;
                prt:units = "s" ;
                prt:long_name = "pulse repetition time" ;
        float scan_rate ;
                scan_rate:units = "degree s-1" ;
                scan_rate:long_name = "antenna rotation rate" ;
        int n_samples ;
                n_samples:long_name = "number of samples contributing to each stored pulse" ;
data:
        frequency = 9.41e+09 ;
        polarization_mode = "vertical" ;
        pulse_width = 8.e-08 ;
        prt = 0.0005 ;
        scan_rate = 144. ;
        n_samples = 1 ;
```

### The `radar_parameters` group

Constant antenna properties are stored in a dedicated `radar_parameters` group in the root group:

```
group: radar_parameters {
  variables:
        float beam_width_h ;
                beam_width_h:units = "degree" ;
                beam_width_h:long_name = "horizontal antenna beam width" ;
        float beam_width_v ;
                beam_width_v:units = "degree" ;
                beam_width_v:long_name = "vertical antenna beam width" ;
  data:
        beam_width_h = 0.95 ;
        beam_width_v = 20. ;
  } // group radar_parameters
```

## Georeference correction parameters

Known offsets of pointing direction, range, time, and platform position relative to GPS are stored in the `georeference_correction` group in the root group of polar products (see [Georeference correction parameters](georeference_correction.md)):

```
group: georeference_correction {
  variables:
        float azimuth_correction ;
                azimuth_correction:units = "degree" ;
                azimuth_correction:long_name = "correction to azimuth values" ;
        float range_correction ;
                range_correction:units = "m" ;
                range_correction:long_name = "correction to range values" ;
        double time_correction ;
                time_correction:units = "s" ;
                time_correction:long_name = "correction to time values" ;
        float position_offset_x ;
                position_offset_x:units = "m" ;
                position_offset_x:long_name = "position of radar antenna relative to GPS antenna, positive to starboard" ;
        float position_offset_y ;
                position_offset_y:units = "m" ;
                position_offset_y:long_name = "position of radar antenna relative to GPS antenna, positive toward the bow" ;
  data:
        azimuth_correction = -1.3 ;
        range_correction = -22.5 ;
        time_correction = 0.35 ;
        position_offset_x = 2.4 ;
        position_offset_y = -11.8 ;
  } // group georeference_correction
```
