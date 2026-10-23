---
title: Sea ice drift maps (L2a)
layout: default
parent: "Annex: Example products"
nav_order: 10
---

# L2a: Sea ice drift maps

{: .informative }
> This page is informative. The product type `sea_ice_drift` is one of the [gridded products](../product_types/gridded.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md). The [file contents](#file-contents) summarize these definitions for this product; where they differ, the definitions apply.

Sea ice drift maps (`sea_ice_drift`) provide the horizontal sea ice drift vector in a set of analysis windows along the platform trajectory, together with a `measurement_quality` bit flag.
Each drift vector is retrieved from the displacement of the backscatter pattern between two radar images, which may be temporally averaged, separated by a short time lag.
The method is named by [`retrieval_method`](../metadata_attributes/processing_parameters.md#retrieval_method): for example, cross-correlation of the two images within a local analysis window, where the offset at the correlation peak yields the drift vector (`cross_correlation`; Lund et al. [2018](../references/index.md#lund-2018)), or optical flow (`optical_flow`; Thomson et al. [2021](../references/index.md#thomson-2021)).
If the retrieval is also carried out backward in time, two independent drift vector estimates are reported for each location: [`eastward_sea_ice_velocity`](../product_types/product_variables.md#eastward_sea_ice_velocity)/[`northward_sea_ice_velocity`](../product_types/product_variables.md#northward_sea_ice_velocity) from the forward retrieval and [`eastward_sea_ice_velocity_backward`](../product_types/product_variables.md#eastward_sea_ice_velocity_backward)/[`northward_sea_ice_velocity_backward`](../product_types/product_variables.md#northward_sea_ice_velocity_backward) from the backward retrieval.
A cross-correlation reports the peak correlation coefficients of both, [`correlation_coefficient`](../product_types/product_variables.md#correlation_coefficient) and [`correlation_coefficient_backward`](../product_types/product_variables.md#correlation_coefficient_backward).
The cross-correlation method is blind to the actual presence or absence of sea ice in the analysis window; a high correlation coefficient together with good agreement between the forward and backward drift vectors is therefore used as an indicator that sea ice, rather than open water or noise, was tracked.

## File contents

**Layout.** On a moving platform, the file holds one [time-bounded grid](../product_types/gridded.md#time-bounded-grids) per measurement, each in a `time_<YYYYMMDDHHMMSS>` group; on a fixed platform, it holds one [single grid](../product_types/gridded.md#fixed-platform) in the root group, with the leading dimension [`time`](../product_types/gridded.md#variables-time). Each grid is the [geographic grid](../product_types/gridded.md#geographic-grid) `(latitude, longitude)` or the [local grid](../product_types/gridded.md#local-grid) `(y, x)`.

A file of this product holds the following items; each links to its definition, and the condition, where one is given, states when the tier applies.

| Item | Tier | Condition |
|---|---|---|
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`product_type`](../metadata_attributes/mandatory_global.md#product_type) `= "sea_ice_drift"` | Required | |
| [`platform_is_mobile`](../metadata_attributes/optional_global.md#platform_is_mobile) `= "true"` | Required | moving platform |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| [`analysis_window_shape`](../metadata_attributes/processing_parameters.md#analysis_window_shape), [`analysis_window_size`](../metadata_attributes/processing_parameters.md#analysis_window_size), [`analysis_window_spacing`](../metadata_attributes/processing_parameters.md#analysis_window_spacing), [`measurement_duration`](../metadata_attributes/processing_parameters.md#measurement_duration), [`retrieval_method`](../metadata_attributes/processing_parameters.md#retrieval_method), [`time_lag`](../metadata_attributes/processing_parameters.md#time_lag) | Recommended | |
| [`averaging_duration`](../metadata_attributes/processing_parameters.md#averaging_duration) | Recommended | |
| **Variables of each grid** | | |
| [`time`](../product_types/gridded.md#variables-time) | Required | |
| [`time_iso_8601`](../metadata_attributes/variable_attributes.md#time_iso_8601) on `time` | Optional | time-bounded grid |
| [`time_bounds`](../product_types/gridded.md#time_bounds) | Optional | |
| [`latitude`](../product_types/gridded.md#variables-latitude), [`longitude`](../product_types/gridded.md#variables-longitude) | Required | |
| [`x`](../product_types/gridded.md#variables-x), [`y`](../product_types/gridded.md#variables-y) | Required | local grid |
| [`crs`](../product_types/gridded.md#variables-crs) | Required | local grid |
| [`crs`](../product_types/gridded.md#variables-crs) | Recommended | geographic grid |
| [`radar_latitude`](../product_types/gridded.md#radar_latitude), [`radar_longitude`](../product_types/gridded.md#radar_longitude) | Optional | |
| [`eastward_sea_ice_velocity`](../product_types/product_variables.md#eastward_sea_ice_velocity), [`northward_sea_ice_velocity`](../product_types/product_variables.md#northward_sea_ice_velocity) | Required | north-oriented grid |
| [`sea_ice_x_velocity`](../product_types/product_variables.md#sea_ice_x_velocity), [`sea_ice_y_velocity`](../product_types/product_variables.md#sea_ice_y_velocity) | Required | rotated grid |
| [`correlation_coefficient`](../product_types/product_variables.md#correlation_coefficient), [`correlation_coefficient_backward`](../product_types/product_variables.md#correlation_coefficient_backward) | Optional | |
| [`eastward_sea_ice_velocity_backward`](../product_types/product_variables.md#eastward_sea_ice_velocity_backward), [`northward_sea_ice_velocity_backward`](../product_types/product_variables.md#northward_sea_ice_velocity_backward) | Optional | north-oriented grid |
| [`sea_ice_x_velocity_backward`](../product_types/product_variables.md#sea_ice_x_velocity_backward), [`sea_ice_y_velocity_backward`](../product_types/product_variables.md#sea_ice_y_velocity_backward) | Optional | rotated grid |
| [`measurement_quality`](../product_types/gridded.md#measurement_quality) | Recommended | |
| [`coordinates`](../metadata_attributes/variable_attributes.md#coordinates) `= "longitude latitude"` on the data variables | Required | local grid |
| [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) `= "crs"` on the data variables | Required | with `crs` |
{: .contents-table }

## Example

A radar on a moving platform, with the map on the [geographic grid](../product_types/gridded.md#geographic-grid).

```
netcdf or_2025-08-23-12_sea_ice_drift {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 79.0600 ; // recommended
                :geospatial_lat_min = 78.8800 ; // recommended
                :geospatial_lon_max = 5.4000 ; // recommended
                :geospatial_lon_min = 4.6500 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > SEA ICE > SEA ICE MOTION" ; // highly recommended
                :platform_is_mobile = "true" ;
                :product_type = "sea_ice_drift" ;
                :summary = "Sea ice drift vectors from a marine X-band radar on board R/V Ocean Research, retrieved from the cross-correlation of backscatter patterns between time-averaged radar images." ; // highly recommended
                :time_coverage_end = "2025-08-23T12:59:59Z" ; // recommended
                :time_coverage_start = "2025-08-23T12:00:31.417000Z" ; // recommended
                :title = "Marine X-band radar sea ice drift maps from R/V Ocean Research" ; // highly recommended
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 720. ; // recommended
                :analysis_window_spacing = 500. ; // recommended
                :averaging_duration = 30. ; // recommended
                :measurement_duration = 120. ; // recommended
                :retrieval_method = "cross_correlation" ; // recommended
                :time_lag = 90. ; // recommended

group: time_20250823120031 {
  dimensions:
        latitude = 17 ;
        longitude = 17 ;
  variables:
        char crs ; // recommended
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of sea ice drift measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-08-23T12:00:31.417000Z" ; // optional
        double longitude(longitude) ;
                longitude:long_name = "center longitude of sea ice drift measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(latitude) ;
                latitude:long_name = "center latitude of sea ice drift measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_ice_velocity(latitude, longitude) ;
                eastward_sea_ice_velocity:long_name = "eastward component of the sea ice velocity from forward cross-correlation" ;
                eastward_sea_ice_velocity:standard_name = "eastward_sea_ice_velocity" ;
                eastward_sea_ice_velocity:units = "m s-1" ;
                eastward_sea_ice_velocity:grid_mapping = "crs" ;
                eastward_sea_ice_velocity:_FillValue = NaN ;
        double northward_sea_ice_velocity(latitude, longitude) ;
                northward_sea_ice_velocity:long_name = "northward component of the sea ice velocity from forward cross-correlation" ;
                northward_sea_ice_velocity:standard_name = "northward_sea_ice_velocity" ;
                northward_sea_ice_velocity:units = "m s-1" ;
                northward_sea_ice_velocity:grid_mapping = "crs" ;
                northward_sea_ice_velocity:_FillValue = NaN ;
        double correlation_coefficient(latitude, longitude) ; // optional
                correlation_coefficient:long_name = "maximum Pearson coefficient from forward cross-correlation" ;
                correlation_coefficient:units = "1" ;
                correlation_coefficient:grid_mapping = "crs" ;
                correlation_coefficient:_FillValue = NaN ;
        double eastward_sea_ice_velocity_backward(latitude, longitude) ; // optional
                eastward_sea_ice_velocity_backward:long_name = "eastward component of the sea ice velocity from backward cross-correlation" ;
                eastward_sea_ice_velocity_backward:standard_name = "eastward_sea_ice_velocity" ;
                eastward_sea_ice_velocity_backward:units = "m s-1" ;
                eastward_sea_ice_velocity_backward:grid_mapping = "crs" ;
                eastward_sea_ice_velocity_backward:_FillValue = NaN ;
        double northward_sea_ice_velocity_backward(latitude, longitude) ; // optional
                northward_sea_ice_velocity_backward:long_name = "northward component of the sea ice velocity from backward cross-correlation" ;
                northward_sea_ice_velocity_backward:standard_name = "northward_sea_ice_velocity" ;
                northward_sea_ice_velocity_backward:units = "m s-1" ;
                northward_sea_ice_velocity_backward:grid_mapping = "crs" ;
                northward_sea_ice_velocity_backward:_FillValue = NaN ;
        double correlation_coefficient_backward(latitude, longitude) ; // optional
                correlation_coefficient_backward:long_name = "maximum Pearson coefficient from backward cross-correlation" ;
                correlation_coefficient_backward:units = "1" ;
                correlation_coefficient_backward:grid_mapping = "crs" ;
                correlation_coefficient_backward:_FillValue = NaN ;
        ubyte measurement_quality(latitude, longitude) ; // recommended
                measurement_quality:long_name = "measurement quality (0: good, 1-7: bad)" ;
                measurement_quality:flag_meanings = "forward_and_backward_cross_correlation_results_too_different sea_ice_speed_too_high correlation_coefficient_too_low" ;
                measurement_quality:valid_range = 0UB, 7UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:_FillValue = 255UB ;
  } // group time_20250823120031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per measurement period ...
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2025-08-23-12_sea_ice_drift {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :platform_is_mobile = "true" ;
                :product_type = "sea_ice_drift" ;

group: time_20250823120031 {
  dimensions:
        latitude = 17 ;
        longitude = 17 ;
  variables:
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of sea ice drift measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude(longitude) ;
                longitude:long_name = "center longitude of sea ice drift measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(latitude) ;
                latitude:long_name = "center latitude of sea ice drift measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_ice_velocity(latitude, longitude) ;
                eastward_sea_ice_velocity:long_name = "eastward component of the sea ice velocity from forward cross-correlation" ;
                eastward_sea_ice_velocity:standard_name = "eastward_sea_ice_velocity" ;
                eastward_sea_ice_velocity:units = "m s-1" ;
                eastward_sea_ice_velocity:_FillValue = NaN ;
        double northward_sea_ice_velocity(latitude, longitude) ;
                northward_sea_ice_velocity:long_name = "northward component of the sea ice velocity from forward cross-correlation" ;
                northward_sea_ice_velocity:standard_name = "northward_sea_ice_velocity" ;
                northward_sea_ice_velocity:units = "m s-1" ;
                northward_sea_ice_velocity:_FillValue = NaN ;
  } // group time_20250823120031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per measurement period ...
}
```

## Example for a fixed platform

A radar on a fixed platform, with the map on the [local grid](../product_types/gridded.md#local-grid): all measurements share a [single grid](../product_types/gridded.md#fixed-platform) in the root group, with the leading dimension [`time`](../product_types/gridded.md#variables-time), and the [`crs`](../product_types/gridded.md#variables-crs) is centered on the radar antenna.

```
netcdf or_2025-03-12-12_sea_ice_drift {
dimensions:
        time = 30 ;
        y = 17 ;
        x = 17 ;
variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 11.4500 ;
                crs:latitude_of_projection_origin = 78.9800 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of sea ice drift measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double x(x) ;
                x:long_name = "eastward distance from radar antenna" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from radar antenna" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        double longitude(y, x) ;
                longitude:long_name = "center longitude of sea ice drift measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(y, x) ;
                latitude:long_name = "center latitude of sea ice drift measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_ice_velocity(time, y, x) ;
                eastward_sea_ice_velocity:long_name = "eastward component of the sea ice velocity from forward cross-correlation" ;
                eastward_sea_ice_velocity:standard_name = "eastward_sea_ice_velocity" ;
                eastward_sea_ice_velocity:units = "m s-1" ;
                eastward_sea_ice_velocity:grid_mapping = "crs" ;
                eastward_sea_ice_velocity:coordinates = "longitude latitude" ;
                eastward_sea_ice_velocity:_FillValue = NaN ;
        double northward_sea_ice_velocity(time, y, x) ;
                northward_sea_ice_velocity:long_name = "northward component of the sea ice velocity from forward cross-correlation" ;
                northward_sea_ice_velocity:standard_name = "northward_sea_ice_velocity" ;
                northward_sea_ice_velocity:units = "m s-1" ;
                northward_sea_ice_velocity:grid_mapping = "crs" ;
                northward_sea_ice_velocity:coordinates = "longitude latitude" ;
                northward_sea_ice_velocity:_FillValue = NaN ;
        double correlation_coefficient(time, y, x) ; // optional
                correlation_coefficient:long_name = "maximum Pearson coefficient from forward cross-correlation" ;
                correlation_coefficient:units = "1" ;
                correlation_coefficient:grid_mapping = "crs" ;
                correlation_coefficient:coordinates = "longitude latitude" ;
                correlation_coefficient:_FillValue = NaN ;
        double eastward_sea_ice_velocity_backward(time, y, x) ; // optional
                eastward_sea_ice_velocity_backward:long_name = "eastward component of the sea ice velocity from backward cross-correlation" ;
                eastward_sea_ice_velocity_backward:standard_name = "eastward_sea_ice_velocity" ;
                eastward_sea_ice_velocity_backward:units = "m s-1" ;
                eastward_sea_ice_velocity_backward:grid_mapping = "crs" ;
                eastward_sea_ice_velocity_backward:coordinates = "longitude latitude" ;
                eastward_sea_ice_velocity_backward:_FillValue = NaN ;
        double northward_sea_ice_velocity_backward(time, y, x) ; // optional
                northward_sea_ice_velocity_backward:long_name = "northward component of the sea ice velocity from backward cross-correlation" ;
                northward_sea_ice_velocity_backward:standard_name = "northward_sea_ice_velocity" ;
                northward_sea_ice_velocity_backward:units = "m s-1" ;
                northward_sea_ice_velocity_backward:grid_mapping = "crs" ;
                northward_sea_ice_velocity_backward:coordinates = "longitude latitude" ;
                northward_sea_ice_velocity_backward:_FillValue = NaN ;
        double correlation_coefficient_backward(time, y, x) ; // optional
                correlation_coefficient_backward:long_name = "maximum Pearson coefficient from backward cross-correlation" ;
                correlation_coefficient_backward:units = "1" ;
                correlation_coefficient_backward:grid_mapping = "crs" ;
                correlation_coefficient_backward:coordinates = "longitude latitude" ;
                correlation_coefficient_backward:_FillValue = NaN ;
        ubyte measurement_quality(time, y, x) ; // recommended
                measurement_quality:long_name = "measurement quality (0: good, 1-7: bad)" ;
                measurement_quality:flag_meanings = "forward_and_backward_cross_correlation_results_too_different sea_ice_speed_too_high correlation_coefficient_too_low" ;
                measurement_quality:valid_range = 0UB, 7UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:coordinates = "longitude latitude" ;
                measurement_quality:_FillValue = 255UB ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 79.0159 ; // recommended
                :geospatial_lat_min = 78.9441 ; // recommended
                :geospatial_lon_max = 11.6380 ; // recommended
                :geospatial_lon_min = 11.2620 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > SEA ICE > SEA ICE MOTION" ; // highly recommended
                :product_type = "sea_ice_drift" ;
                :summary = "Sea ice drift vectors from a marine X-band radar at Arctic Ocean Research Station, retrieved from the cross-correlation of backscatter patterns between time-averaged radar images." ; // highly recommended
                :time_coverage_end = "2025-03-12T12:59:59Z" ; // recommended
                :time_coverage_start = "2025-03-12T12:00:00Z" ; // recommended
                :title = "Marine X-band radar sea ice drift maps from Arctic Ocean Research Station" ; // highly recommended
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 720. ; // recommended
                :analysis_window_spacing = 500. ; // recommended
                :averaging_duration = 30. ; // recommended
                :measurement_duration = 120. ; // recommended
                :retrieval_method = "cross_correlation" ; // recommended
                :time_lag = 90. ; // recommended
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2025-03-12-12_sea_ice_drift {
dimensions:
        time = 30 ;
        y = 17 ;
        x = 17 ;
variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 11.4500 ;
                crs:latitude_of_projection_origin = 78.9800 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of sea ice drift measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double x(x) ;
                x:long_name = "eastward distance from radar antenna" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from radar antenna" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        double longitude(y, x) ;
                longitude:long_name = "center longitude of sea ice drift measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(y, x) ;
                latitude:long_name = "center latitude of sea ice drift measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_ice_velocity(time, y, x) ;
                eastward_sea_ice_velocity:long_name = "eastward component of the sea ice velocity from forward cross-correlation" ;
                eastward_sea_ice_velocity:standard_name = "eastward_sea_ice_velocity" ;
                eastward_sea_ice_velocity:units = "m s-1" ;
                eastward_sea_ice_velocity:grid_mapping = "crs" ;
                eastward_sea_ice_velocity:coordinates = "longitude latitude" ;
                eastward_sea_ice_velocity:_FillValue = NaN ;
        double northward_sea_ice_velocity(time, y, x) ;
                northward_sea_ice_velocity:long_name = "northward component of the sea ice velocity from forward cross-correlation" ;
                northward_sea_ice_velocity:standard_name = "northward_sea_ice_velocity" ;
                northward_sea_ice_velocity:units = "m s-1" ;
                northward_sea_ice_velocity:grid_mapping = "crs" ;
                northward_sea_ice_velocity:coordinates = "longitude latitude" ;
                northward_sea_ice_velocity:_FillValue = NaN ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "sea_ice_drift" ;
}
```

## Example for a rotated grid

A radar on a fixed platform at a coastal site, with the map on a [rotated local grid](../georeferencing/index.md#rotated-local-grids): its axes follow the convention of Argus and CIRN, [`x`](../product_types/gridded.md#variables-x) cross-shore, positive offshore, and [`y`](../product_types/gridded.md#variables-y) along-shore, at a coast whose offshore normal points to 110°, so that the azimuth of the y axis is 20°. The [`crs`](../product_types/gridded.md#variables-crs) gives `grid_mapping_name = "rotated_azimuthal_equidistant"` and [`azimuth_of_y_axis`](../metadata_attributes/variable_attributes.md#azimuth_of_y_axis), and the sea ice drift is given in [`sea_ice_x_velocity`](../product_types/product_variables.md#sea_ice_x_velocity) and [`sea_ice_y_velocity`](../product_types/product_variables.md#sea_ice_y_velocity) in place of its eastward and northward components.

```
netcdf cr_2025-03-12-12_sea_ice_drift {
dimensions:
        time = 30 ;
        y = 17 ;
        x = 17 ;
variables:
        char crs ;
                crs:grid_mapping_name = "rotated_azimuthal_equidistant" ;
                crs:azimuth_of_y_axis = 20. ;
                crs:longitude_of_projection_origin = 11.4500 ;
                crs:latitude_of_projection_origin = 78.9800 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
                crs:comment = "Argus/CIRN axes: x cross-shore, positive offshore; y along-shore" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of sea ice drift measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double x(x) ;
                x:long_name = "cross-shore distance from radar antenna, positive offshore" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "along-shore distance from radar antenna" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        double longitude(y, x) ;
                longitude:long_name = "center longitude of sea ice drift measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(y, x) ;
                latitude:long_name = "center latitude of sea ice drift measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_ice_x_velocity(time, y, x) ;
                sea_ice_x_velocity:long_name = "offshore component of the sea ice velocity from forward cross-correlation" ;
                sea_ice_x_velocity:standard_name = "sea_ice_x_velocity" ;
                sea_ice_x_velocity:units = "m s-1" ;
                sea_ice_x_velocity:grid_mapping = "crs" ;
                sea_ice_x_velocity:coordinates = "longitude latitude" ;
                sea_ice_x_velocity:_FillValue = NaN ;
        double sea_ice_y_velocity(time, y, x) ;
                sea_ice_y_velocity:long_name = "along-shore component of the sea ice velocity from forward cross-correlation" ;
                sea_ice_y_velocity:standard_name = "sea_ice_y_velocity" ;
                sea_ice_y_velocity:units = "m s-1" ;
                sea_ice_y_velocity:grid_mapping = "crs" ;
                sea_ice_y_velocity:coordinates = "longitude latitude" ;
                sea_ice_y_velocity:_FillValue = NaN ;
        double correlation_coefficient(time, y, x) ; // optional
                correlation_coefficient:long_name = "maximum Pearson coefficient from forward cross-correlation" ;
                correlation_coefficient:units = "1" ;
                correlation_coefficient:grid_mapping = "crs" ;
                correlation_coefficient:coordinates = "longitude latitude" ;
                correlation_coefficient:_FillValue = NaN ;
        double sea_ice_x_velocity_backward(time, y, x) ; // optional
                sea_ice_x_velocity_backward:long_name = "offshore component of the sea ice velocity from backward cross-correlation" ;
                sea_ice_x_velocity_backward:standard_name = "sea_ice_x_velocity" ;
                sea_ice_x_velocity_backward:units = "m s-1" ;
                sea_ice_x_velocity_backward:grid_mapping = "crs" ;
                sea_ice_x_velocity_backward:coordinates = "longitude latitude" ;
                sea_ice_x_velocity_backward:_FillValue = NaN ;
        double sea_ice_y_velocity_backward(time, y, x) ; // optional
                sea_ice_y_velocity_backward:long_name = "along-shore component of the sea ice velocity from backward cross-correlation" ;
                sea_ice_y_velocity_backward:standard_name = "sea_ice_y_velocity" ;
                sea_ice_y_velocity_backward:units = "m s-1" ;
                sea_ice_y_velocity_backward:grid_mapping = "crs" ;
                sea_ice_y_velocity_backward:coordinates = "longitude latitude" ;
                sea_ice_y_velocity_backward:_FillValue = NaN ;
        double correlation_coefficient_backward(time, y, x) ; // optional
                correlation_coefficient_backward:long_name = "maximum Pearson coefficient from backward cross-correlation" ;
                correlation_coefficient_backward:units = "1" ;
                correlation_coefficient_backward:grid_mapping = "crs" ;
                correlation_coefficient_backward:coordinates = "longitude latitude" ;
                correlation_coefficient_backward:_FillValue = NaN ;
        ubyte measurement_quality(time, y, x) ; // recommended
                measurement_quality:long_name = "measurement quality (0: good, 1-7: bad)" ;
                measurement_quality:flag_meanings = "forward_and_backward_cross_correlation_results_too_different sea_ice_speed_too_high correlation_coefficient_too_low" ;
                measurement_quality:valid_range = 0UB, 7UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:coordinates = "longitude latitude" ;
                measurement_quality:_FillValue = 255UB ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 79.0260 ; // recommended
                :geospatial_lat_min = 78.9340 ; // recommended
                :geospatial_lon_max = 11.6910 ; // recommended
                :geospatial_lon_min = 11.2090 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > SEA ICE > SEA ICE MOTION" ; // highly recommended
                :product_type = "sea_ice_drift" ;
                :summary = "Sea ice drift vectors from a marine X-band radar at Arctic Coastal Research Station, retrieved from the cross-correlation of backscatter patterns between time-averaged radar images." ; // highly recommended
                :time_coverage_end = "2025-03-12T12:59:59Z" ; // recommended
                :time_coverage_start = "2025-03-12T12:00:00Z" ; // recommended
                :title = "Marine X-band radar sea ice drift maps from Arctic Coastal Research Station" ; // highly recommended
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 720. ; // recommended
                :analysis_window_spacing = 500. ; // recommended
                :averaging_duration = 30. ; // recommended
                :measurement_duration = 120. ; // recommended
                :retrieval_method = "cross_correlation" ; // recommended
                :time_lag = 90. ; // recommended
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf cr_2025-03-12-12_sea_ice_drift {
dimensions:
        time = 30 ;
        y = 17 ;
        x = 17 ;
variables:
        char crs ;
                crs:grid_mapping_name = "rotated_azimuthal_equidistant" ;
                crs:azimuth_of_y_axis = 20. ;
                crs:longitude_of_projection_origin = 11.4500 ;
                crs:latitude_of_projection_origin = 78.9800 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
                crs:comment = "Argus/CIRN axes: x cross-shore, positive offshore; y along-shore" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of sea ice drift measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double x(x) ;
                x:long_name = "cross-shore distance from radar antenna, positive offshore" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "along-shore distance from radar antenna" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        double longitude(y, x) ;
                longitude:long_name = "center longitude of sea ice drift measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(y, x) ;
                latitude:long_name = "center latitude of sea ice drift measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_ice_x_velocity(time, y, x) ;
                sea_ice_x_velocity:long_name = "offshore component of the sea ice velocity from forward cross-correlation" ;
                sea_ice_x_velocity:standard_name = "sea_ice_x_velocity" ;
                sea_ice_x_velocity:units = "m s-1" ;
                sea_ice_x_velocity:grid_mapping = "crs" ;
                sea_ice_x_velocity:coordinates = "longitude latitude" ;
                sea_ice_x_velocity:_FillValue = NaN ;
        double sea_ice_y_velocity(time, y, x) ;
                sea_ice_y_velocity:long_name = "along-shore component of the sea ice velocity from forward cross-correlation" ;
                sea_ice_y_velocity:standard_name = "sea_ice_y_velocity" ;
                sea_ice_y_velocity:units = "m s-1" ;
                sea_ice_y_velocity:grid_mapping = "crs" ;
                sea_ice_y_velocity:coordinates = "longitude latitude" ;
                sea_ice_y_velocity:_FillValue = NaN ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "sea_ice_drift" ;
}
```
