---
title: Surface wave two-dimensional wavenumber spectra (L2a)
layout: default
parent: "Annex: Example products"
nav_order: 11
---

# L2a: Surface wave two-dimensional wavenumber spectra

{: .informative }
> This page is informative. The product type `wave_wavenumber_spectra` is one of the [spatially averaged products](../product_types/spatially_averaged.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md). The [file contents](#file-contents) summarize these definitions for this product; where they differ, the definitions apply.

Two-dimensional wavenumber spectra (`wave_wavenumber_spectra`) give the (time-averaged) wave energy density, `sea_surface_wave_wavenumber_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber)`, as a function of the two horizontal wavenumber components for each measurement, averaged over the analysis windows that contribute to it.
By SOMaR convention, the wavenumber vector points toward the direction from which the waves come, opposite to the direction of propagation, so that the spectrum agrees with the from-direction of the [frequency-direction spectra](wave_frequency_direction_spectra.md); spectra that follow the propagation direction, as in many wave models, are mirrored through the origin (see [`eastward_wave_wavenumber`](../product_types/product_variables.md#eastward_wave_wavenumber)).
They are retrieved from the wavenumber-frequency spectra of local radar image analysis windows, as used for the [near-surface current retrieval](current_maps.md), by keeping the wave signal that follows the dispersion relation (Young et al. [1985](../references/index.md#young-1985)).
The Level 2b frequency-direction spectra, [one-dimensional frequency spectra](wave_frequency_spectra.md), and [peak and mean wave parameters](wave_parameters.md) are derived from these spectra.
The wave energy density is calibrated, typically against a reference wave data set (see [Wave calibration parameters](../metadata_attributes/wave_calibration.md)).
The quantities from which the calibration derives the significant wave height may be stored as for the wave parameters: [`wave_signal`](../product_types/product_variables.md#wave_signal) and [`background_noise`](../product_types/product_variables.md#background_noise) for the signal-to-noise ratio method, or [`sea_surface_wave_mean_square_slope`](../product_types/product_variables.md#sea_surface_wave_mean_square_slope) for the shadowing method.

## File contents

**Layout.** On a moving platform, the file holds a [trajectory](../product_types/spatially_averaged.md#moving-and-fixed-platforms) along the dimension `time`, with `longitude(time)` and `latitude(time)`; on a fixed platform, it holds a time series along the dimension `time`, with scalar `longitude` and `latitude`.

A file of this product holds the following items; each links to its definition, and the condition, where one is given, states when the tier applies.

| Item | Tier | Condition |
|---|---|---|
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`product_type`](../metadata_attributes/mandatory_global.md#product_type) `= "wave_wavenumber_spectra"` | Required | |
| [`platform_is_mobile`](../metadata_attributes/optional_global.md#platform_is_mobile) `= "true"` | Required | moving platform |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| [`featureType`](../metadata_attributes/optional_global.md#featureType) `= "trajectory"` or `"timeSeries"` | Recommended | |
| [`analysis_window_shape`](../metadata_attributes/processing_parameters.md#analysis_window_shape), [`analysis_window_size`](../metadata_attributes/processing_parameters.md#analysis_window_size), [`measurement_duration`](../metadata_attributes/processing_parameters.md#measurement_duration), [`number_of_analysis_windows`](../metadata_attributes/processing_parameters.md#number_of_analysis_windows), [`number_of_images`](../metadata_attributes/processing_parameters.md#number_of_images) | Recommended | |
| [`analysis_window_motion`](../metadata_attributes/processing_parameters.md#analysis_window_motion), [`retrieval_method`](../metadata_attributes/processing_parameters.md#retrieval_method) | Optional | |
| **Variables** | | |
| [`time`](../product_types/spatially_averaged.md#time), [`longitude`](../product_types/spatially_averaged.md#longitude), [`latitude`](../product_types/spatially_averaged.md#latitude) | Required | |
| [`time_bounds`](../product_types/spatially_averaged.md#time_bounds) | Optional | |
| [`crs`](../product_types/spatially_averaged.md#crs) | Required | rotated grid |
| [`crs`](../product_types/spatially_averaged.md#crs) | Recommended | north-oriented grid |
| [`trajectory`](../product_types/spatially_averaged.md#trajectory) | Recommended | moving platform |
| [`station`](../product_types/spatially_averaged.md#station) | Recommended | fixed platform |
| [`platform_speed_wrt_ground`](../product_types/spatially_averaged.md#platform_speed_wrt_ground), [`platform_course`](../product_types/spatially_averaged.md#platform_course) | Required | `analysis_window_motion = "platform_fixed"` |
| [`radar_latitude`](../product_types/spatially_averaged.md#radar_latitude), [`radar_longitude`](../product_types/spatially_averaged.md#radar_longitude) | Optional | |
| [`sea_surface_wave_wavenumber_variance_spectral_density`](../product_types/product_variables.md#sea_surface_wave_wavenumber_variance_spectral_density) | Required | |
| [`eastward_wave_wavenumber`](../product_types/product_variables.md#eastward_wave_wavenumber), [`northward_wave_wavenumber`](../product_types/product_variables.md#northward_wave_wavenumber) | Required | north-oriented grid |
| [`x_wave_wavenumber`](../product_types/product_variables.md#x_wave_wavenumber), [`y_wave_wavenumber`](../product_types/product_variables.md#y_wave_wavenumber) | Required | rotated grid |
| [`wave_signal`](../product_types/product_variables.md#wave_signal), [`background_noise`](../product_types/product_variables.md#background_noise), [`sea_surface_wave_mean_square_slope`](../product_types/product_variables.md#sea_surface_wave_mean_square_slope) | Optional | |
| [`eastward_sea_water_velocity`](../product_types/spatially_averaged.md#eastward_sea_water_velocity), [`northward_sea_water_velocity`](../product_types/spatially_averaged.md#northward_sea_water_velocity) | Optional | north-oriented grid |
| [`sea_water_x_velocity`](../product_types/product_variables.md#sea_water_x_velocity), [`sea_water_y_velocity`](../product_types/product_variables.md#sea_water_y_velocity) | Optional | rotated grid |
| [`measurement_quality`](../product_types/spatially_averaged.md#measurement_quality) | Recommended | |
| [`coordinates`](../metadata_attributes/variable_attributes.md#coordinates) `= "time longitude latitude"` on the data variables | Required | |
| [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) `= "crs"` on the data variables | Required | with `crs` |
| [`cell_methods`](../metadata_attributes/variable_attributes.md#cell_methods) `= "area: mean (comment: over the analysis windows of the measurement)"` on the spectrum, `wave_signal`, `background_noise`, and the near-surface current | Recommended | |
| **Groups** | | |
| [`wave_calibration`](../metadata_attributes/wave_calibration.md) | Recommended | |
{: .contents-table }

## Example

A radar on a moving platform.

```
netcdf or_2025-01-15-11_wave_wavenumber_spectra {
dimensions:
        time = 29 ;
        northward_wave_wavenumber = 512 ;
        eastward_wave_wavenumber = 512 ;
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
        string trajectory ; // recommended
                trajectory:long_name = "name of the platform" ;
                trajectory:cf_role = "trajectory_id" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double eastward_wave_wavenumber(eastward_wave_wavenumber) ;
                eastward_wave_wavenumber:long_name = "eastward component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                eastward_wave_wavenumber:units = "m-1" ;
        double northward_wave_wavenumber(northward_wave_wavenumber) ;
                northward_wave_wavenumber:long_name = "northward component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                northward_wave_wavenumber:units = "m-1" ;
        double longitude(time) ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(time) ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_wavenumber_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber) ;
                sea_surface_wave_wavenumber_variance_spectral_density:long_name = "wave energy density two dimensional wavenumber spectrum" ;
                sea_surface_wave_wavenumber_variance_spectral_density:units = "m4" ;
                sea_surface_wave_wavenumber_variance_spectral_density:coordinates = "time longitude latitude" ;
                sea_surface_wave_wavenumber_variance_spectral_density:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                sea_surface_wave_wavenumber_variance_spectral_density:grid_mapping = "crs" ;
                sea_surface_wave_wavenumber_variance_spectral_density:ancillary_variables = "measurement_quality" ;
        double wave_signal(time) ; // optional
                wave_signal:long_name = "radar image spectral density of the wave signal" ;
                wave_signal:units = "1" ;
                wave_signal:coordinates = "time longitude latitude" ;
                wave_signal:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                wave_signal:grid_mapping = "crs" ;
                wave_signal:ancillary_variables = "measurement_quality" ;
        double background_noise(time) ; // optional
                background_noise:long_name = "radar image spectral density of the background noise" ;
                background_noise:units = "1" ;
                background_noise:coordinates = "time longitude latitude" ;
                background_noise:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                background_noise:grid_mapping = "crs" ;
                background_noise:ancillary_variables = "measurement_quality" ;
        ubyte measurement_quality(time) ; // recommended
                measurement_quality:long_name = "measurement quality (0: good, 1-63: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold wave_steepness_above_threshold invalid_peak number_of_temporal_neighbors_below_threshold rain_contamination" ;
                measurement_quality:valid_range = 0UB, 63UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:coordinates = "time longitude latitude" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:_FillValue = 255UB ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :featureType = "trajectory" ; // recommended
                :geospatial_lat_max = 15.0012 ; // recommended
                :geospatial_lat_min = 14.9478 ; // recommended
                :geospatial_lon_max = 145.9486 ; // recommended
                :geospatial_lon_min = 145.8631 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE SPECTRA" ; // highly recommended
                :platform_is_mobile = "true" ;
                :product_type = "wave_wavenumber_spectra" ;
                :summary = "Two-dimensional surface wave wavenumber spectra from a marine X-band radar on board R/V Ocean Research, retrieved from 240 s image sequences in analysis windows fixed to the Earth and averaged over the windows of each measurement." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:59:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar surface wave two-dimensional wavenumber spectra from R/V Ocean Research" ; // highly recommended
                :analysis_window_motion = "earth_fixed" ; // optional
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 3840. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_analysis_windows = 6 ; // recommended
                :number_of_images = 160 ; // recommended
data:
        trajectory = "R/V Ocean Research" ;

group: wave_calibration { ... } // recommended; as in the example under Wave calibration parameters
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2025-01-15-11_wave_wavenumber_spectra {
dimensions:
        time = 29 ;
        northward_wave_wavenumber = 512 ;
        eastward_wave_wavenumber = 512 ;
variables:
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double eastward_wave_wavenumber(eastward_wave_wavenumber) ;
                eastward_wave_wavenumber:long_name = "eastward component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                eastward_wave_wavenumber:units = "m-1" ;
        double northward_wave_wavenumber(northward_wave_wavenumber) ;
                northward_wave_wavenumber:long_name = "northward component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                northward_wave_wavenumber:units = "m-1" ;
        double longitude(time) ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(time) ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_wavenumber_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber) ;
                sea_surface_wave_wavenumber_variance_spectral_density:long_name = "wave energy density two dimensional wavenumber spectrum" ;
                sea_surface_wave_wavenumber_variance_spectral_density:units = "m4" ;
                sea_surface_wave_wavenumber_variance_spectral_density:coordinates = "time longitude latitude" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :platform_is_mobile = "true" ;
                :product_type = "wave_wavenumber_spectra" ;

}
```

## Example for a fixed platform

A radar on a fixed platform: the measurements form a [time series](../product_types/spatially_averaged.md#moving-and-fixed-platforms), identified by [`station`](../product_types/spatially_averaged.md#station) in place of the trajectory, with scalar [`longitude`](../product_types/spatially_averaged.md#longitude) and [`latitude`](../product_types/spatially_averaged.md#latitude) given under `data`.

```
netcdf or_2023-08-31-17_wave_wavenumber_spectra {
dimensions:
        time = 29 ;
        northward_wave_wavenumber = 512 ;
        eastward_wave_wavenumber = 512 ;
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
        string station ; // recommended
                station:long_name = "name of the radar station" ;
                station:cf_role = "timeseries_id" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double eastward_wave_wavenumber(eastward_wave_wavenumber) ;
                eastward_wave_wavenumber:long_name = "eastward component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                eastward_wave_wavenumber:units = "m-1" ;
        double northward_wave_wavenumber(northward_wave_wavenumber) ;
                northward_wave_wavenumber:long_name = "northward component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                northward_wave_wavenumber:units = "m-1" ;
        double longitude ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_wavenumber_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber) ;
                sea_surface_wave_wavenumber_variance_spectral_density:long_name = "wave energy density two dimensional wavenumber spectrum" ;
                sea_surface_wave_wavenumber_variance_spectral_density:units = "m4" ;
                sea_surface_wave_wavenumber_variance_spectral_density:coordinates = "time longitude latitude" ;
                sea_surface_wave_wavenumber_variance_spectral_density:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                sea_surface_wave_wavenumber_variance_spectral_density:grid_mapping = "crs" ;
                sea_surface_wave_wavenumber_variance_spectral_density:ancillary_variables = "measurement_quality" ;
        double wave_signal(time) ; // optional
                wave_signal:long_name = "radar image spectral density of the wave signal" ;
                wave_signal:units = "1" ;
                wave_signal:coordinates = "time longitude latitude" ;
                wave_signal:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                wave_signal:grid_mapping = "crs" ;
                wave_signal:ancillary_variables = "measurement_quality" ;
        double background_noise(time) ; // optional
                background_noise:long_name = "radar image spectral density of the background noise" ;
                background_noise:units = "1" ;
                background_noise:coordinates = "time longitude latitude" ;
                background_noise:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                background_noise:grid_mapping = "crs" ;
                background_noise:ancillary_variables = "measurement_quality" ;
        ubyte measurement_quality(time) ; // recommended
                measurement_quality:long_name = "measurement quality (0: good, 1-63: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold wave_steepness_above_threshold invalid_peak number_of_temporal_neighbors_below_threshold rain_contamination" ;
                measurement_quality:valid_range = 0UB, 63UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:coordinates = "time longitude latitude" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:_FillValue = 255UB ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :featureType = "timeSeries" ; // recommended
                :geospatial_lat_max = 54.1702 ; // recommended
                :geospatial_lat_min = 54.1702 ; // recommended
                :geospatial_lon_max = 7.9050 ; // recommended
                :geospatial_lon_min = 7.9050 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE SPECTRA" ; // highly recommended
                :product_type = "wave_wavenumber_spectra" ;
                :summary = "Two-dimensional surface wave wavenumber spectra from a marine X-band radar at Ocean Research Station, retrieved from 240 s image sequences in analysis windows fixed to the Earth and averaged over the windows of each measurement." ; // highly recommended
                :time_coverage_end = "2023-08-31T17:59:59Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar surface wave two-dimensional wavenumber spectra from Ocean Research Station" ; // highly recommended
                :analysis_window_motion = "earth_fixed" ; // optional
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 3840. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_analysis_windows = 6 ; // recommended
                :number_of_images = 160 ; // recommended
data:
        station = "Ocean Research Station" ;
        longitude = 7.9050 ;
        latitude = 54.1702 ;

group: wave_calibration { ... } // recommended; as in the example under Wave calibration parameters
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2023-08-31-17_wave_wavenumber_spectra {
dimensions:
        time = 29 ;
        northward_wave_wavenumber = 512 ;
        eastward_wave_wavenumber = 512 ;
variables:
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double eastward_wave_wavenumber(eastward_wave_wavenumber) ;
                eastward_wave_wavenumber:long_name = "eastward component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                eastward_wave_wavenumber:units = "m-1" ;
        double northward_wave_wavenumber(northward_wave_wavenumber) ;
                northward_wave_wavenumber:long_name = "northward component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                northward_wave_wavenumber:units = "m-1" ;
        double longitude ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_wavenumber_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber) ;
                sea_surface_wave_wavenumber_variance_spectral_density:long_name = "wave energy density two dimensional wavenumber spectrum" ;
                sea_surface_wave_wavenumber_variance_spectral_density:units = "m4" ;
                sea_surface_wave_wavenumber_variance_spectral_density:coordinates = "time longitude latitude" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "wave_wavenumber_spectra" ;
data:
        longitude = 7.9050 ;
        latitude = 54.1702 ;

}
```

## Example for a rotated grid

A radar on a fixed platform at a coastal site, whose vector components are given along the axes of a [rotated local grid](../georeferencing/index.md#rotated-local-grids) centered on the radar antenna: its axes follow the convention of Argus and CIRN, `x` cross-shore, positive offshore, and `y` along-shore, at a coast whose offshore normal points to 110°, so that the azimuth of the y axis is 20°. The [`crs`](../product_types/spatially_averaged.md#crs) gives `grid_mapping_name = "rotated_azimuthal_equidistant"`, [`azimuth_of_y_axis`](../metadata_attributes/variable_attributes.md#azimuth_of_y_axis), and [`crs_wkt`](../metadata_attributes/variable_attributes.md#crs_wkt), while `longitude` and `latitude` remain geographic coordinates, and the wavenumbers are given in [`x_wave_wavenumber`](../product_types/product_variables.md#x_wave_wavenumber) and [`y_wave_wavenumber`](../product_types/product_variables.md#y_wave_wavenumber) in place of their eastward and northward components.

```
netcdf cr_2023-08-31-17_wave_wavenumber_spectra {
dimensions:
        time = 29 ;
        y_wave_wavenumber = 512 ;
        x_wave_wavenumber = 512 ;
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
        string station ; // recommended
                station:long_name = "name of the radar station" ;
                station:cf_role = "timeseries_id" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double x_wave_wavenumber(x_wave_wavenumber) ;
                x_wave_wavenumber:long_name = "offshore component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                x_wave_wavenumber:units = "m-1" ;
        double y_wave_wavenumber(y_wave_wavenumber) ;
                y_wave_wavenumber:long_name = "along-shore component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                y_wave_wavenumber:units = "m-1" ;
        double longitude ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_wavenumber_variance_spectral_density(time, y_wave_wavenumber, x_wave_wavenumber) ;
                sea_surface_wave_wavenumber_variance_spectral_density:long_name = "wave energy density two dimensional wavenumber spectrum" ;
                sea_surface_wave_wavenumber_variance_spectral_density:units = "m4" ;
                sea_surface_wave_wavenumber_variance_spectral_density:coordinates = "time longitude latitude" ;
                sea_surface_wave_wavenumber_variance_spectral_density:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                sea_surface_wave_wavenumber_variance_spectral_density:grid_mapping = "crs" ;
                sea_surface_wave_wavenumber_variance_spectral_density:ancillary_variables = "measurement_quality" ;
        double wave_signal(time) ; // optional
                wave_signal:long_name = "radar image spectral density of the wave signal" ;
                wave_signal:units = "1" ;
                wave_signal:coordinates = "time longitude latitude" ;
                wave_signal:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                wave_signal:grid_mapping = "crs" ;
                wave_signal:ancillary_variables = "measurement_quality" ;
        double background_noise(time) ; // optional
                background_noise:long_name = "radar image spectral density of the background noise" ;
                background_noise:units = "1" ;
                background_noise:coordinates = "time longitude latitude" ;
                background_noise:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                background_noise:grid_mapping = "crs" ;
                background_noise:ancillary_variables = "measurement_quality" ;
        ubyte measurement_quality(time) ; // recommended
                measurement_quality:long_name = "measurement quality (0: good, 1-63: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold wave_steepness_above_threshold invalid_peak number_of_temporal_neighbors_below_threshold rain_contamination" ;
                measurement_quality:valid_range = 0UB, 63UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:coordinates = "time longitude latitude" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:_FillValue = 255UB ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :featureType = "timeSeries" ; // recommended
                :geospatial_lat_max = 54.1702 ; // recommended
                :geospatial_lat_min = 54.1702 ; // recommended
                :geospatial_lon_max = 7.9050 ; // recommended
                :geospatial_lon_min = 7.9050 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE SPECTRA" ; // highly recommended
                :product_type = "wave_wavenumber_spectra" ;
                :summary = "Two-dimensional surface wave wavenumber spectra from a marine X-band radar at Coastal Research Station, retrieved from 240 s image sequences in analysis windows fixed to the Earth and averaged over the windows of each measurement." ; // highly recommended
                :time_coverage_end = "2023-08-31T17:59:59Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar surface wave two-dimensional wavenumber spectra from Coastal Research Station" ; // highly recommended
                :analysis_window_motion = "earth_fixed" ; // optional
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 3840. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_analysis_windows = 6 ; // recommended
                :number_of_images = 160 ; // recommended
data:
        station = "Coastal Research Station" ;
        longitude = 7.9050 ;
        latitude = 54.1702 ;

group: wave_calibration { ... } // recommended; as in the example under Wave calibration parameters
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf cr_2023-08-31-17_wave_wavenumber_spectra {
dimensions:
        time = 29 ;
        y_wave_wavenumber = 512 ;
        x_wave_wavenumber = 512 ;
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
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double x_wave_wavenumber(x_wave_wavenumber) ;
                x_wave_wavenumber:long_name = "offshore component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                x_wave_wavenumber:units = "m-1" ;
        double y_wave_wavenumber(y_wave_wavenumber) ;
                y_wave_wavenumber:long_name = "along-shore component of the wavenumber vector, pointing toward the direction from which the waves come" ;
                y_wave_wavenumber:units = "m-1" ;
        double longitude ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_wavenumber_variance_spectral_density(time, y_wave_wavenumber, x_wave_wavenumber) ;
                sea_surface_wave_wavenumber_variance_spectral_density:long_name = "wave energy density two dimensional wavenumber spectrum" ;
                sea_surface_wave_wavenumber_variance_spectral_density:units = "m4" ;
                sea_surface_wave_wavenumber_variance_spectral_density:coordinates = "time longitude latitude" ;
                sea_surface_wave_wavenumber_variance_spectral_density:grid_mapping = "crs" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "wave_wavenumber_spectra" ;
data:
        longitude = 7.9050 ;
        latitude = 54.1702 ;

}
```
