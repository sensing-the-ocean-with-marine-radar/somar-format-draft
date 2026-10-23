---
title: Bathymetric maps (L2a)
layout: default
parent: "Annex: Example products"
nav_order: 9
---

# L2a: Bathymetric maps

{: .informative }
> This page is informative. The product type `bathymetry` is one of the [gridded products](../product_types/gridded.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md). The [file contents](#file-contents) summarize these definitions for this product; where they differ, the definitions apply.

Bathymetric maps (`bathymetry`) provide sea floor depth ([`sea_floor_depth_below_sea_surface`](../product_types/product_variables.md#sea_floor_depth_below_sea_surface)) in a set of analysis windows along the platform trajectory, together with an optional standard error and a `measurement_quality` bit flag.
As for the [near-surface current maps](current_maps.md), each depth is retrieved from the wave signal in the wavenumber-frequency spectrum of a local analysis window, here exploiting the depth-induced deviation from the deep-water dispersion relation; the method is named by [`retrieval_method`](../metadata_attributes/processing_parameters.md#retrieval_method), e.g. a least-squares fit of the wave signal to the dispersion relation that solves for water depth rather than current velocity (`dispersion_relation_least_squares_fit`; Bell [1999](../references/index.md#bell-1999)).
Because this deviation only becomes detectable once the water depth is a small enough fraction of the dominant ocean wavelength, marine radar bathymetry retrievals are limited to waters shallower than approximately 30% of the underlying ocean wavelength; [`mean_wavenumber`](../product_types/product_variables.md#mean_wavenumber) reports the actual mean wavenumber of the wave signal used for a given measurement.

The depths are not tide-corrected, as the definition of `sea_floor_depth_below_sea_surface` states; depths relative to a fixed vertical datum, such as mean sea level, are obtained by applying the correction.

## File contents

**Layout.** On a moving platform, the file holds one [time-bounded grid](../product_types/gridded.md#time-bounded-grids) per measurement, each in a `time_<YYYYMMDDHHMMSS>` group; on a fixed platform, it holds one [single grid](../product_types/gridded.md#fixed-platform) in the root group, with the leading dimension [`time`](../product_types/gridded.md#variables-time). Each grid is the [geographic grid](../product_types/gridded.md#geographic-grid) `(latitude, longitude)` or the [local grid](../product_types/gridded.md#local-grid) `(y, x)`.

A file of this product holds the following items; each links to its definition, and the condition, where one is given, states when the tier applies.

| Item | Tier | Condition |
|---|---|---|
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`product_type`](../metadata_attributes/mandatory_global.md#product_type) `= "bathymetry"` | Required | |
| [`platform_is_mobile`](../metadata_attributes/optional_global.md#platform_is_mobile) `= "true"` | Required | moving platform |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| [`analysis_window_shape`](../metadata_attributes/processing_parameters.md#analysis_window_shape), [`analysis_window_size`](../metadata_attributes/processing_parameters.md#analysis_window_size), [`analysis_window_spacing`](../metadata_attributes/processing_parameters.md#analysis_window_spacing), [`measurement_duration`](../metadata_attributes/processing_parameters.md#measurement_duration), [`number_of_images`](../metadata_attributes/processing_parameters.md#number_of_images), [`retrieval_method`](../metadata_attributes/processing_parameters.md#retrieval_method) | Recommended | |
| **Variables of each grid** | | |
| [`time`](../product_types/gridded.md#variables-time) | Required | |
| [`time_iso_8601`](../metadata_attributes/variable_attributes.md#time_iso_8601) on `time` | Optional | time-bounded grid |
| [`time_bounds`](../product_types/gridded.md#time_bounds) | Optional | |
| [`latitude`](../product_types/gridded.md#variables-latitude), [`longitude`](../product_types/gridded.md#variables-longitude) | Required | |
| [`x`](../product_types/gridded.md#variables-x), [`y`](../product_types/gridded.md#variables-y) | Required | local grid |
| [`crs`](../product_types/gridded.md#variables-crs) | Required | local grid |
| [`crs`](../product_types/gridded.md#variables-crs) | Recommended | geographic grid |
| [`radar_latitude`](../product_types/gridded.md#radar_latitude), [`radar_longitude`](../product_types/gridded.md#radar_longitude) | Optional | |
| [`sea_floor_depth_below_sea_surface`](../product_types/product_variables.md#sea_floor_depth_below_sea_surface) | Required | |
| [`mean_wavenumber`](../product_types/product_variables.md#mean_wavenumber) | Recommended | |
| [`sea_floor_depth_below_sea_surface_standard_error`](../product_types/product_variables.md#sea_floor_depth_below_sea_surface_standard_error), [`number_of_fitted_spectral_points`](../product_types/product_variables.md#number_of_fitted_spectral_points) | Optional | |
| [`measurement_quality`](../product_types/gridded.md#measurement_quality) | Recommended | |
| [`coordinates`](../metadata_attributes/variable_attributes.md#coordinates) `= "longitude latitude"` on the data variables | Required | local grid |
| [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) `= "crs"` on the data variables | Required | with `crs` |
{: .contents-table }

## Example

A radar on a moving platform, with the map on the [geographic grid](../product_types/gridded.md#geographic-grid).

```
netcdf or_2025-01-15-12_bathymetry {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 14.9785 ; // recommended
                :geospatial_lat_min = 14.887 ; // recommended
                :geospatial_lon_max = 146.042 ; // recommended
                :geospatial_lon_min = 145.9175 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > WATER DEPTH" ; // highly recommended
                :platform_is_mobile = "true" ;
                :product_type = "bathymetry" ;
                :summary = "Water depths from a marine X-band radar on board R/V Ocean Research, retrieved by least-squares fits of the dispersion relation to the wave signal in the wavenumber-frequency spectra of 240 s image sequences." ; // highly recommended
                :time_coverage_end = "2025-01-15T12:59:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T12:00:31.417000Z" ; // recommended
                :title = "Marine X-band radar bathymetric maps from R/V Ocean Research" ; // highly recommended
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 1245. ; // recommended
                :analysis_window_spacing = 500. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_images = 160 ; // recommended
                :retrieval_method = "dispersion_relation_least_squares_fit" ; // recommended

group: time_20250115120031 {
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
                time:long_name = "start time of bathymetry measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T12:00:31.417000Z" ; // optional
        double longitude(longitude) ;
                longitude:long_name = "center longitude of bathymetry measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(latitude) ;
                latitude:long_name = "center latitude of bathymetry measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_floor_depth_below_sea_surface(latitude, longitude) ;
                sea_floor_depth_below_sea_surface:long_name = "distance between sea surface and sea floor" ;
                sea_floor_depth_below_sea_surface:standard_name = "sea_floor_depth_below_sea_surface" ;
                sea_floor_depth_below_sea_surface:units = "m" ;
                sea_floor_depth_below_sea_surface:grid_mapping = "crs" ;
                sea_floor_depth_below_sea_surface:_FillValue = NaN ;
        double mean_wavenumber(latitude, longitude) ; // recommended
                mean_wavenumber:long_name = "mean wavenumber of the wave signal used by the bathymetry measurement" ;
                mean_wavenumber:units = "m-1" ;
                mean_wavenumber:grid_mapping = "crs" ;
                mean_wavenumber:_FillValue = NaN ;
        double sea_floor_depth_below_sea_surface_standard_error(latitude, longitude) ; // optional
                sea_floor_depth_below_sea_surface_standard_error:long_name = "standard error of the bathymetry measurement" ;
                sea_floor_depth_below_sea_surface_standard_error:units = "m" ;
                sea_floor_depth_below_sea_surface_standard_error:grid_mapping = "crs" ;
                sea_floor_depth_below_sea_surface_standard_error:_FillValue = NaN ;
        int number_of_fitted_spectral_points(latitude, longitude) ; // optional
                number_of_fitted_spectral_points:long_name = "number of points of the wavenumber-frequency spectrum used in the least-squares fit" ;
                number_of_fitted_spectral_points:units = "1" ;
                number_of_fitted_spectral_points:grid_mapping = "crs" ;
                number_of_fitted_spectral_points:_FillValue = -1 ;
        ubyte measurement_quality(latitude, longitude) ; // recommended
                measurement_quality:long_name = "measurement quality (0: good, 1-127: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold bathymetry_fit_boundaries_reached number_of_spatial_neighbors_below_threshold number_of_temporal_neighbors_below_threshold difference_from_all_temporal_neighbors_exceeds_threshold measurement_outside_area_of_validity" ;
                measurement_quality:valid_range = 0UB, 127UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB, 64UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:_FillValue = 255UB ;
  } // group time_20250115120031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per measurement period ...
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2025-01-15-12_bathymetry {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :platform_is_mobile = "true" ;
                :product_type = "bathymetry" ;

group: time_20250115120031 {
  dimensions:
        latitude = 17 ;
        longitude = 17 ;
  variables:
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of bathymetry measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude(longitude) ;
                longitude:long_name = "center longitude of bathymetry measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(latitude) ;
                latitude:long_name = "center latitude of bathymetry measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_floor_depth_below_sea_surface(latitude, longitude) ;
                sea_floor_depth_below_sea_surface:long_name = "distance between sea surface and sea floor" ;
                sea_floor_depth_below_sea_surface:standard_name = "sea_floor_depth_below_sea_surface" ;
                sea_floor_depth_below_sea_surface:units = "m" ;
                sea_floor_depth_below_sea_surface:_FillValue = NaN ;
  } // group time_20250115120031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per measurement period ...
}
```

## Example for a fixed platform

A radar on a fixed platform, with the map on the [local grid](../product_types/gridded.md#local-grid): all measurements share a [single grid](../product_types/gridded.md#fixed-platform) in the root group, with the leading dimension [`time`](../product_types/gridded.md#variables-time), and the [`crs`](../product_types/gridded.md#variables-crs) is centered on the radar antenna.

```
netcdf or_2023-08-31-17_bathymetry {
dimensions:
        time = 15 ;
        y = 17 ;
        x = 17 ;
variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 7.8853 ;
                crs:latitude_of_projection_origin = 54.1826 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of bathymetry measurement" ;
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
                longitude:long_name = "center longitude of bathymetry measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(y, x) ;
                latitude:long_name = "center latitude of bathymetry measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_floor_depth_below_sea_surface(time, y, x) ;
                sea_floor_depth_below_sea_surface:long_name = "distance between sea surface and sea floor" ;
                sea_floor_depth_below_sea_surface:standard_name = "sea_floor_depth_below_sea_surface" ;
                sea_floor_depth_below_sea_surface:units = "m" ;
                sea_floor_depth_below_sea_surface:grid_mapping = "crs" ;
                sea_floor_depth_below_sea_surface:coordinates = "longitude latitude" ;
                sea_floor_depth_below_sea_surface:_FillValue = NaN ;
        double mean_wavenumber(time, y, x) ; // recommended
                mean_wavenumber:long_name = "mean wavenumber of the wave signal used by the bathymetry measurement" ;
                mean_wavenumber:units = "m-1" ;
                mean_wavenumber:grid_mapping = "crs" ;
                mean_wavenumber:coordinates = "longitude latitude" ;
                mean_wavenumber:_FillValue = NaN ;
        double sea_floor_depth_below_sea_surface_standard_error(time, y, x) ; // optional
                sea_floor_depth_below_sea_surface_standard_error:long_name = "standard error of the bathymetry measurement" ;
                sea_floor_depth_below_sea_surface_standard_error:units = "m" ;
                sea_floor_depth_below_sea_surface_standard_error:grid_mapping = "crs" ;
                sea_floor_depth_below_sea_surface_standard_error:coordinates = "longitude latitude" ;
                sea_floor_depth_below_sea_surface_standard_error:_FillValue = NaN ;
        int number_of_fitted_spectral_points(time, y, x) ; // optional
                number_of_fitted_spectral_points:long_name = "number of points of the wavenumber-frequency spectrum used in the least-squares fit" ;
                number_of_fitted_spectral_points:units = "1" ;
                number_of_fitted_spectral_points:grid_mapping = "crs" ;
                number_of_fitted_spectral_points:coordinates = "longitude latitude" ;
                number_of_fitted_spectral_points:_FillValue = -1 ;
        ubyte measurement_quality(time, y, x) ; // recommended
                measurement_quality:long_name = "measurement quality (0: good, 1-127: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold bathymetry_fit_boundaries_reached number_of_spatial_neighbors_below_threshold number_of_temporal_neighbors_below_threshold difference_from_all_temporal_neighbors_exceeds_threshold measurement_outside_area_of_validity" ;
                measurement_quality:valid_range = 0UB, 127UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB, 64UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:coordinates = "longitude latitude" ;
                measurement_quality:_FillValue = 255UB ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 54.2185 ; // recommended
                :geospatial_lat_min = 54.1467 ; // recommended
                :geospatial_lon_max = 7.9467 ; // recommended
                :geospatial_lon_min = 7.8239 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > WATER DEPTH" ; // highly recommended
                :product_type = "bathymetry" ;
                :summary = "Water depths from a marine X-band radar at Ocean Research Station, retrieved by least-squares fits of the dispersion relation to the wave signal in the wavenumber-frequency spectra of 240 s image sequences." ; // highly recommended
                :time_coverage_end = "2023-08-31T17:59:59Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar bathymetric maps from Ocean Research Station" ; // highly recommended
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 1245. ; // recommended
                :analysis_window_spacing = 500. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_images = 160 ; // recommended
                :retrieval_method = "dispersion_relation_least_squares_fit" ; // recommended
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2023-08-31-17_bathymetry {
dimensions:
        time = 15 ;
        y = 17 ;
        x = 17 ;
variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 7.8853 ;
                crs:latitude_of_projection_origin = 54.1826 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of bathymetry measurement" ;
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
                longitude:long_name = "center longitude of bathymetry measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(y, x) ;
                latitude:long_name = "center latitude of bathymetry measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_floor_depth_below_sea_surface(time, y, x) ;
                sea_floor_depth_below_sea_surface:long_name = "distance between sea surface and sea floor" ;
                sea_floor_depth_below_sea_surface:standard_name = "sea_floor_depth_below_sea_surface" ;
                sea_floor_depth_below_sea_surface:units = "m" ;
                sea_floor_depth_below_sea_surface:grid_mapping = "crs" ;
                sea_floor_depth_below_sea_surface:coordinates = "longitude latitude" ;
                sea_floor_depth_below_sea_surface:_FillValue = NaN ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "bathymetry" ;
}
```

## Example for a rotated grid

A radar on a fixed platform at a coastal site, with the map on a [rotated local grid](../georeferencing/index.md#rotated-local-grids): its axes follow the convention of Argus and CIRN, [`x`](../product_types/gridded.md#variables-x) cross-shore, positive offshore, and [`y`](../product_types/gridded.md#variables-y) along-shore, at a coast whose offshore normal points to 110°, so that the azimuth of the y axis is 20°. The [`crs`](../product_types/gridded.md#variables-crs) gives `grid_mapping_name = "rotated_azimuthal_equidistant"`, [`azimuth_of_y_axis`](../metadata_attributes/variable_attributes.md#azimuth_of_y_axis), and [`crs_wkt`](../metadata_attributes/variable_attributes.md#crs_wkt).

```
netcdf cr_2023-08-31-17_bathymetry {
dimensions:
        time = 15 ;
        y = 17 ;
        x = 17 ;
variables:
        char crs ;
                crs:grid_mapping_name = "rotated_azimuthal_equidistant" ;
                crs:azimuth_of_y_axis = 20. ;
                crs:longitude_of_projection_origin = 7.8853 ;
                crs:latitude_of_projection_origin = 54.1826 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
                crs:crs_wkt = "DERIVEDPROJCRS[\"SOMaR rotated local grid\",",
                        "BASEPROJCRS[\"SOMaR local grid\",",
                        "BASEGEOGCRS[\"WGS 84\",DATUM[\"World Geodetic System 1984\",ELLIPSOID[\"WGS 84\",6378137,298.257223563,LENGTHUNIT[\"metre\",1]]],PRIMEM[\"Greenwich\",0,ANGLEUNIT[\"degree\",0.0174532925199433]]],",
                        "CONVERSION[\"Azimuthal equidistant\",METHOD[\"Azimuthal Equidistant\",ID[\"EPSG\",1125]],",
                        "PARAMETER[\"Latitude of natural origin\",54.1826,ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8801]],",
                        "PARAMETER[\"Longitude of natural origin\",7.8853,ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8802]],",
                        "PARAMETER[\"False easting\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8806]],",
                        "PARAMETER[\"False northing\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8807]]]],",
                        "DERIVINGCONVERSION[\"Rotation of the axes\",METHOD[\"Affine parametric transformation\",ID[\"EPSG\",9624]],",
                        "PARAMETER[\"A0\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8623]],",
                        "PARAMETER[\"A1\",0.939692620785908,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8624]],",
                        "PARAMETER[\"A2\",-0.342020143325669,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8625]],",
                        "PARAMETER[\"B0\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8639]],",
                        "PARAMETER[\"B1\",0.342020143325669,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8640]],",
                        "PARAMETER[\"B2\",0.939692620785908,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8641]]],",
                        "CS[Cartesian,2],AXIS[\"(x)\",unspecified,ORDER[1],LENGTHUNIT[\"metre\",1]],AXIS[\"(y)\",unspecified,ORDER[2],LENGTHUNIT[\"metre\",1]]]" ;
                crs:comment = "Argus/CIRN axes: x cross-shore, positive offshore; y along-shore" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of bathymetry measurement" ;
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
                longitude:long_name = "center longitude of bathymetry measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(y, x) ;
                latitude:long_name = "center latitude of bathymetry measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_floor_depth_below_sea_surface(time, y, x) ;
                sea_floor_depth_below_sea_surface:long_name = "distance between sea surface and sea floor" ;
                sea_floor_depth_below_sea_surface:standard_name = "sea_floor_depth_below_sea_surface" ;
                sea_floor_depth_below_sea_surface:units = "m" ;
                sea_floor_depth_below_sea_surface:grid_mapping = "crs" ;
                sea_floor_depth_below_sea_surface:coordinates = "longitude latitude" ;
                sea_floor_depth_below_sea_surface:_FillValue = NaN ;
        double mean_wavenumber(time, y, x) ; // recommended
                mean_wavenumber:long_name = "mean wavenumber of the wave signal used by the bathymetry measurement" ;
                mean_wavenumber:units = "m-1" ;
                mean_wavenumber:grid_mapping = "crs" ;
                mean_wavenumber:coordinates = "longitude latitude" ;
                mean_wavenumber:_FillValue = NaN ;
        double sea_floor_depth_below_sea_surface_standard_error(time, y, x) ; // optional
                sea_floor_depth_below_sea_surface_standard_error:long_name = "standard error of the bathymetry measurement" ;
                sea_floor_depth_below_sea_surface_standard_error:units = "m" ;
                sea_floor_depth_below_sea_surface_standard_error:grid_mapping = "crs" ;
                sea_floor_depth_below_sea_surface_standard_error:coordinates = "longitude latitude" ;
                sea_floor_depth_below_sea_surface_standard_error:_FillValue = NaN ;
        int number_of_fitted_spectral_points(time, y, x) ; // optional
                number_of_fitted_spectral_points:long_name = "number of points of the wavenumber-frequency spectrum used in the least-squares fit" ;
                number_of_fitted_spectral_points:units = "1" ;
                number_of_fitted_spectral_points:grid_mapping = "crs" ;
                number_of_fitted_spectral_points:coordinates = "longitude latitude" ;
                number_of_fitted_spectral_points:_FillValue = -1 ;
        ubyte measurement_quality(time, y, x) ; // recommended
                measurement_quality:long_name = "measurement quality (0: good, 1-127: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold bathymetry_fit_boundaries_reached number_of_spatial_neighbors_below_threshold number_of_temporal_neighbors_below_threshold difference_from_all_temporal_neighbors_exceeds_threshold measurement_outside_area_of_validity" ;
                measurement_quality:valid_range = 0UB, 127UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB, 64UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:coordinates = "longitude latitude" ;
                measurement_quality:_FillValue = 255UB ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 54.2286 ; // recommended
                :geospatial_lat_min = 54.1366 ; // recommended
                :geospatial_lon_max = 7.9640 ; // recommended
                :geospatial_lon_min = 7.8066 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > WATER DEPTH" ; // highly recommended
                :product_type = "bathymetry" ;
                :summary = "Water depths from a marine X-band radar at Coastal Research Station, retrieved by least-squares fits of the dispersion relation to the wave signal in the wavenumber-frequency spectra of 240 s image sequences." ; // highly recommended
                :time_coverage_end = "2023-08-31T17:59:59Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar bathymetric maps from Coastal Research Station" ; // highly recommended
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 1245. ; // recommended
                :analysis_window_spacing = 500. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_images = 160 ; // recommended
                :retrieval_method = "dispersion_relation_least_squares_fit" ; // recommended
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf cr_2023-08-31-17_bathymetry {
dimensions:
        time = 15 ;
        y = 17 ;
        x = 17 ;
variables:
        char crs ;
                crs:grid_mapping_name = "rotated_azimuthal_equidistant" ;
                crs:azimuth_of_y_axis = 20. ;
                crs:longitude_of_projection_origin = 7.8853 ;
                crs:latitude_of_projection_origin = 54.1826 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
                crs:crs_wkt = "DERIVEDPROJCRS[\"SOMaR rotated local grid\",",
                        "BASEPROJCRS[\"SOMaR local grid\",",
                        "BASEGEOGCRS[\"WGS 84\",DATUM[\"World Geodetic System 1984\",ELLIPSOID[\"WGS 84\",6378137,298.257223563,LENGTHUNIT[\"metre\",1]]],PRIMEM[\"Greenwich\",0,ANGLEUNIT[\"degree\",0.0174532925199433]]],",
                        "CONVERSION[\"Azimuthal equidistant\",METHOD[\"Azimuthal Equidistant\",ID[\"EPSG\",1125]],",
                        "PARAMETER[\"Latitude of natural origin\",54.1826,ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8801]],",
                        "PARAMETER[\"Longitude of natural origin\",7.8853,ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8802]],",
                        "PARAMETER[\"False easting\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8806]],",
                        "PARAMETER[\"False northing\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8807]]]],",
                        "DERIVINGCONVERSION[\"Rotation of the axes\",METHOD[\"Affine parametric transformation\",ID[\"EPSG\",9624]],",
                        "PARAMETER[\"A0\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8623]],",
                        "PARAMETER[\"A1\",0.939692620785908,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8624]],",
                        "PARAMETER[\"A2\",-0.342020143325669,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8625]],",
                        "PARAMETER[\"B0\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8639]],",
                        "PARAMETER[\"B1\",0.342020143325669,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8640]],",
                        "PARAMETER[\"B2\",0.939692620785908,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8641]]],",
                        "CS[Cartesian,2],AXIS[\"(x)\",unspecified,ORDER[1],LENGTHUNIT[\"metre\",1]],AXIS[\"(y)\",unspecified,ORDER[2],LENGTHUNIT[\"metre\",1]]]" ;
                crs:comment = "Argus/CIRN axes: x cross-shore, positive offshore; y along-shore" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of bathymetry measurement" ;
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
                longitude:long_name = "center longitude of bathymetry measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(y, x) ;
                latitude:long_name = "center latitude of bathymetry measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_floor_depth_below_sea_surface(time, y, x) ;
                sea_floor_depth_below_sea_surface:long_name = "distance between sea surface and sea floor" ;
                sea_floor_depth_below_sea_surface:standard_name = "sea_floor_depth_below_sea_surface" ;
                sea_floor_depth_below_sea_surface:units = "m" ;
                sea_floor_depth_below_sea_surface:grid_mapping = "crs" ;
                sea_floor_depth_below_sea_surface:coordinates = "longitude latitude" ;
                sea_floor_depth_below_sea_surface:_FillValue = NaN ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "bathymetry" ;
}
```
