---
title: Surface wave one-dimensional frequency spectra (L2b)
layout: default
parent: "Annex: Examples"
nav_order: 13
---

# L2b: Surface wave one-dimensional frequency spectra

{: .informative }
> An example of the product type `wave_frequency_spectra`, of the data type [`averaged_windows`](../data_types/averaged_windows.md), which defines its structure and variables (see [Annex: Examples](index.md)).

One-dimensional frequency spectra (`wave_frequency_spectra`) give the (time-averaged) wave energy density, `sea_surface_wave_variance_spectral_density(time, wave_frequency)`, for each measurement, averaged over the analysis windows that contribute to it, together with the directional spread ([`sea_surface_wave_directional_spread`](../data_types/product_variables.md#sea_surface_wave_directional_spread)) and mean wave direction ([`sea_surface_wave_mean_from_direction`](../data_types/product_variables.md#sea_surface_wave_mean_from_direction)) in each frequency band.
They are derived from the [two-dimensional wavenumber spectra](wave_wavenumber_spectra.md) using the linear wave dispersion relation, which relates each wavenumber to its corresponding wave frequency.
The frequencies are intrinsic, i.e. relative to the moving water, if this dispersion relation omits the current, or absolute, i.e. relative to the ground, if it includes the Doppler shift by the current; which of the two is given by [`wave_frequency_frame`](../metadata_attributes/processing_parameters.md#wave_frequency_frame).

## File contents

**Layout.** On a moving platform, the file holds a [trajectory](../data_types/averaged_windows.md#moving-and-fixed-platforms) along the dimension [`time`](../data_types/averaged_windows.md#time), with `longitude(time)` and `latitude(time)`; on a fixed platform, it holds a time series along the dimension `time`, with scalar [`longitude`](../data_types/averaged_windows.md#longitude) and [`latitude`](../data_types/averaged_windows.md#latitude).

| Item | Tier | Condition |
|---|---|---|
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`data_type`](../metadata_attributes/mandatory_global.md#data_type) `= "averaged_windows"` | Required | |
| [`product_type`](../metadata_attributes/optional_global.md#product_type) `= "wave_frequency_spectra"` | Recommended | |
| [`platform_is_mobile`](../metadata_attributes/mandatory_global.md#platform_is_mobile) `= "true"` | Required | moving platform |
| [`platform_is_mobile`](../metadata_attributes/mandatory_global.md#platform_is_mobile) `= "false"` | Required | fixed platform |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| [`featureType`](../metadata_attributes/optional_global.md#featureType) `= "trajectory"` or `"timeSeries"` | Recommended | |
| [`analysis_window_shape`](../metadata_attributes/processing_parameters.md#analysis_window_shape), [`analysis_window_size`](../metadata_attributes/processing_parameters.md#analysis_window_size), [`measurement_duration`](../metadata_attributes/processing_parameters.md#measurement_duration), [`number_of_analysis_windows`](../metadata_attributes/processing_parameters.md#number_of_analysis_windows), [`number_of_images`](../metadata_attributes/processing_parameters.md#number_of_images), [`wave_frequency_frame`](../metadata_attributes/processing_parameters.md#wave_frequency_frame) | Recommended | |
| [`analysis_window_motion`](../metadata_attributes/processing_parameters.md#analysis_window_motion), [`retrieval_method`](../metadata_attributes/processing_parameters.md#retrieval_method) | Optional | |
| **Variables** | | |
| [`time`](../data_types/averaged_windows.md#time), [`longitude`](../data_types/averaged_windows.md#longitude), [`latitude`](../data_types/averaged_windows.md#latitude) | Required | |
| [`time_bounds`](../data_types/averaged_windows.md#time_bounds) | Optional | |
| [`crs`](../data_types/averaged_windows.md#crs) | Required | rotated grid |
| [`crs`](../data_types/averaged_windows.md#crs) | Recommended | north-oriented grid |
| [`trajectory`](../data_types/averaged_windows.md#trajectory) | Recommended | moving platform |
| [`station`](../data_types/averaged_windows.md#station) | Recommended | fixed platform |
| [`platform_speed_wrt_ground`](../data_types/averaged_windows.md#platform_speed_wrt_ground), [`platform_course`](../data_types/averaged_windows.md#platform_course) | Required | `analysis_window_motion = "platform_fixed"` |
| [`radar_latitude`](../data_types/averaged_windows.md#radar_latitude), [`radar_longitude`](../data_types/averaged_windows.md#radar_longitude) | Optional | |
| [`wave_frequency`](../data_types/product_variables.md#wave_frequency), [`sea_surface_wave_variance_spectral_density`](../data_types/product_variables.md#sea_surface_wave_variance_spectral_density) | Required | |
| [`sea_surface_wave_directional_spread`](../data_types/product_variables.md#sea_surface_wave_directional_spread), [`sea_surface_wave_mean_from_direction`](../data_types/product_variables.md#sea_surface_wave_mean_from_direction) | Optional | |
| [`eastward_sea_water_velocity`](../data_types/averaged_windows.md#eastward_sea_water_velocity), [`northward_sea_water_velocity`](../data_types/averaged_windows.md#northward_sea_water_velocity) | Optional | north-oriented grid |
| [`sea_water_x_velocity`](../data_types/product_variables.md#sea_water_x_velocity), [`sea_water_y_velocity`](../data_types/product_variables.md#sea_water_y_velocity) | Optional | rotated grid |
| [`measurement_quality`](../data_types/averaged_windows.md#measurement_quality) | Recommended | |
| [`coordinates`](../metadata_attributes/variable_attributes.md#coordinates) `= "time longitude latitude"` on the data variables | Required | |
| [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) `= "crs"` on the data variables | Required | with `crs` |
| [`cell_methods`](../metadata_attributes/variable_attributes.md#cell_methods) `= "area: mean (comment: over the analysis windows of the measurement)"` on the spectrum and the near-surface current | Recommended | |
| **Groups** | | |
| [`wave_calibration`](../metadata_attributes/wave_calibration.md) | Recommended | |
{: .contents-table }

## Example

A radar on a moving platform.

```
netcdf or_2025-01-15-11_wave_frequency_spectra {
dimensions:
        time = 15 ;
        wave_frequency = 512 ;
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
        double wave_frequency(wave_frequency) ;
                wave_frequency:long_name = "wave frequency" ;
                wave_frequency:standard_name = "wave_frequency" ;
                wave_frequency:units = "s-1" ;
        double longitude(time) ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(time) ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        float sea_surface_wave_variance_spectral_density(time, wave_frequency) ;
                sea_surface_wave_variance_spectral_density:long_name = "wave energy density frequency spectrum" ;
                sea_surface_wave_variance_spectral_density:standard_name = "sea_surface_wave_variance_spectral_density" ;
                sea_surface_wave_variance_spectral_density:units = "m2 s" ;
                sea_surface_wave_variance_spectral_density:coordinates = "time longitude latitude" ;
                sea_surface_wave_variance_spectral_density:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                sea_surface_wave_variance_spectral_density:grid_mapping = "crs" ;
                sea_surface_wave_variance_spectral_density:ancillary_variables = "measurement_quality" ;
        float sea_surface_wave_directional_spread(time, wave_frequency) ; // optional
                sea_surface_wave_directional_spread:long_name = "wave directional spread in each frequency band" ;
                sea_surface_wave_directional_spread:standard_name = "sea_surface_wave_directional_spread" ;
                sea_surface_wave_directional_spread:units = "degree" ;
                sea_surface_wave_directional_spread:coordinates = "time longitude latitude" ;
                sea_surface_wave_directional_spread:grid_mapping = "crs" ;
                sea_surface_wave_directional_spread:ancillary_variables = "measurement_quality" ;
        float sea_surface_wave_mean_from_direction(time, wave_frequency) ; // optional
                sea_surface_wave_mean_from_direction:long_name = "mean wave direction in each frequency band" ;
                sea_surface_wave_mean_from_direction:standard_name = "sea_surface_wave_mean_from_direction" ;
                sea_surface_wave_mean_from_direction:units = "degree" ;
                sea_surface_wave_mean_from_direction:coordinates = "time longitude latitude" ;
                sea_surface_wave_mean_from_direction:grid_mapping = "crs" ;
                sea_surface_wave_mean_from_direction:ancillary_variables = "measurement_quality" ;
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
                :data_type = "averaged_windows" ;
                :featureType = "trajectory" ; // recommended
                :geospatial_lat_max = 15.0012 ; // recommended
                :geospatial_lat_min = 14.9478 ; // recommended
                :geospatial_lon_max = 145.9486 ; // recommended
                :geospatial_lon_min = 145.8631 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE SPECTRA" ; // highly recommended
                :platform_is_mobile = "true" ;
                :product_type = "wave_frequency_spectra" ; // recommended
                :summary = "One-dimensional surface wave frequency spectra, with mean wave direction and directional spread, from a marine X-band radar on board R/V Ocean Research, derived from two-dimensional wavenumber spectra with the linear dispersion relation." ; // highly recommended
                :time_coverage_end = "2025-01-15T12:00:00Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar surface wave one-dimensional frequency spectra from R/V Ocean Research" ; // highly recommended
                :analysis_window_motion = "earth_fixed" ; // optional
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 3840. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_analysis_windows = 6 ; // recommended
                :number_of_images = 160 ; // recommended
                :wave_frequency_frame = "intrinsic" ; // recommended
data:
        trajectory = "R/V Ocean Research" ;

group: wave_calibration { ... } // recommended; as in the example under Wave calibration parameters
}
```

## Example for a fixed platform

A radar on a fixed platform: the measurements form a [time series](../data_types/averaged_windows.md#moving-and-fixed-platforms), identified by [`station`](../data_types/averaged_windows.md#station) in place of the trajectory, with scalar [`longitude`](../data_types/averaged_windows.md#longitude) and [`latitude`](../data_types/averaged_windows.md#latitude) given under `data`.

```
netcdf ors_2023-08-31-17_wave_frequency_spectra {
dimensions:
        time = 15 ;
        wave_frequency = 512 ;
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
        double wave_frequency(wave_frequency) ;
                wave_frequency:long_name = "wave frequency" ;
                wave_frequency:standard_name = "wave_frequency" ;
                wave_frequency:units = "s-1" ;
        double longitude ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        float sea_surface_wave_variance_spectral_density(time, wave_frequency) ;
                sea_surface_wave_variance_spectral_density:long_name = "wave energy density frequency spectrum" ;
                sea_surface_wave_variance_spectral_density:standard_name = "sea_surface_wave_variance_spectral_density" ;
                sea_surface_wave_variance_spectral_density:units = "m2 s" ;
                sea_surface_wave_variance_spectral_density:coordinates = "time longitude latitude" ;
                sea_surface_wave_variance_spectral_density:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                sea_surface_wave_variance_spectral_density:grid_mapping = "crs" ;
                sea_surface_wave_variance_spectral_density:ancillary_variables = "measurement_quality" ;
        float sea_surface_wave_directional_spread(time, wave_frequency) ; // optional
                sea_surface_wave_directional_spread:long_name = "wave directional spread in each frequency band" ;
                sea_surface_wave_directional_spread:standard_name = "sea_surface_wave_directional_spread" ;
                sea_surface_wave_directional_spread:units = "degree" ;
                sea_surface_wave_directional_spread:coordinates = "time longitude latitude" ;
                sea_surface_wave_directional_spread:grid_mapping = "crs" ;
                sea_surface_wave_directional_spread:ancillary_variables = "measurement_quality" ;
        float sea_surface_wave_mean_from_direction(time, wave_frequency) ; // optional
                sea_surface_wave_mean_from_direction:long_name = "mean wave direction in each frequency band" ;
                sea_surface_wave_mean_from_direction:standard_name = "sea_surface_wave_mean_from_direction" ;
                sea_surface_wave_mean_from_direction:units = "degree" ;
                sea_surface_wave_mean_from_direction:coordinates = "time longitude latitude" ;
                sea_surface_wave_mean_from_direction:grid_mapping = "crs" ;
                sea_surface_wave_mean_from_direction:ancillary_variables = "measurement_quality" ;
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
                :data_type = "averaged_windows" ;
                :featureType = "timeSeries" ; // recommended
                :geospatial_lat_max = 54.1702 ; // recommended
                :geospatial_lat_min = 54.1702 ; // recommended
                :geospatial_lon_max = 7.9050 ; // recommended
                :geospatial_lon_min = 7.9050 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE SPECTRA" ; // highly recommended
                :platform_is_mobile = "false" ;
                :product_type = "wave_frequency_spectra" ; // recommended
                :summary = "One-dimensional surface wave frequency spectra, with mean wave direction and directional spread, from a marine X-band radar at Ocean Research Station, derived from two-dimensional wavenumber spectra with the linear dispersion relation." ; // highly recommended
                :time_coverage_end = "2023-08-31T18:00:00Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar surface wave one-dimensional frequency spectra from Ocean Research Station" ; // highly recommended
                :analysis_window_motion = "earth_fixed" ; // optional
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 3840. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_analysis_windows = 6 ; // recommended
                :number_of_images = 160 ; // recommended
                :wave_frequency_frame = "intrinsic" ; // recommended
data:
        station = "Ocean Research Station" ;
        longitude = 7.9050 ;
        latitude = 54.1702 ;

group: wave_calibration { ... } // recommended; as in the example under Wave calibration parameters
}
```

