---
title: Peak and mean wave parameters (L2b)
layout: default
parent: "Annex: Example products"
nav_order: 14
---

# L2b: Peak and mean wave parameters

{: .informative }
> This page is informative. The product type `wave_parameters` is one of the [spatially averaged products](../product_types/spatially_averaged.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md). The [file contents](#file-contents) summarize these definitions for this product; where they differ, the definitions apply.

Peak and mean wave parameters (`wave_parameters`) summarize each [two-dimensional wavenumber spectrum](wave_wavenumber_spectra.md) using standard bulk wave parameters: significant wave height ([`sea_surface_wave_significant_height`](../product_types/product_variables.md#sea_surface_wave_significant_height)), the peak wave period and peak wave direction (period and direction at the spectral maximum), and the mean wave period and mean wave direction.
The peak and mean wave periods are intrinsic, i.e. relative to the moving water, or absolute, i.e. relative to the ground and including the Doppler shift by the current, as given by [`wave_frequency_frame`](../metadata_attributes/processing_parameters.md#wave_frequency_frame).
To aid interpretation and quality assessment, the quantities from which the significant wave height is derived may also be reported: the wave-signal and background-noise spectral densities ([`wave_signal`](../product_types/product_variables.md#wave_signal), [`background_noise`](../product_types/product_variables.md#background_noise)), whose ratio is the signal-to-noise ratio, for the signal-to-noise ratio method, or the mean square slope of the sea surface ([`sea_surface_wave_mean_square_slope`](../product_types/product_variables.md#sea_surface_wave_mean_square_slope)) for the shadowing method; the calibration applies [`hs_slope`](../metadata_attributes/wave_calibration.md#hs_slope) and [`hs_intercept`](../metadata_attributes/wave_calibration.md#hs_intercept) to the predictor [`hs_predictor`](../metadata_attributes/wave_calibration.md#hs_predictor) computed from them. The wave parameters are given together with the near-surface current vector obtained from the same analysis windows, for platform-fixed windows after correcting for the platform velocity (see [Near-surface current maps](current_maps.md)) and a `measurement_quality` flag.

## File contents

**Layout.** On a moving platform, the file holds a [trajectory](../product_types/spatially_averaged.md#moving-and-fixed-platforms) along the dimension `time`, with `longitude(time)` and `latitude(time)`; on a fixed platform, it holds a time series along the dimension `time`, with scalar `longitude` and `latitude`.

A file of this product holds the following items; each links to its definition, and the condition, where one is given, states when the tier applies.

| Item | Tier | Condition |
|---|---|---|
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`product_type`](../metadata_attributes/mandatory_global.md#product_type) `= "wave_parameters"` | Required | |
| [`platform_is_mobile`](../metadata_attributes/optional_global.md#platform_is_mobile) `= "true"` | Required | moving platform |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| [`featureType`](../metadata_attributes/optional_global.md#featureType) `= "trajectory"` or `"timeSeries"` | Recommended | |
| [`analysis_window_shape`](../metadata_attributes/processing_parameters.md#analysis_window_shape), [`analysis_window_size`](../metadata_attributes/processing_parameters.md#analysis_window_size), [`measurement_duration`](../metadata_attributes/processing_parameters.md#measurement_duration), [`number_of_analysis_windows`](../metadata_attributes/processing_parameters.md#number_of_analysis_windows), [`number_of_images`](../metadata_attributes/processing_parameters.md#number_of_images), [`wave_frequency_frame`](../metadata_attributes/processing_parameters.md#wave_frequency_frame) | Recommended | |
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
| [`sea_surface_wave_significant_height`](../product_types/product_variables.md#sea_surface_wave_significant_height), [`sea_surface_wave_from_direction_at_variance_spectral_density_maximum`](../product_types/product_variables.md#sea_surface_wave_from_direction_at_variance_spectral_density_maximum), [`sea_surface_wave_period_at_variance_spectral_density_maximum`](../product_types/product_variables.md#sea_surface_wave_period_at_variance_spectral_density_maximum), [`sea_surface_wave_mean_period`](../product_types/product_variables.md#sea_surface_wave_mean_period), [`sea_surface_wave_from_direction`](../product_types/product_variables.md#sea_surface_wave_from_direction) | Recommended; at least one required | |
| [`eastward_sea_water_velocity`](../product_types/spatially_averaged.md#eastward_sea_water_velocity), [`northward_sea_water_velocity`](../product_types/spatially_averaged.md#northward_sea_water_velocity) | Optional | north-oriented grid |
| [`sea_water_x_velocity`](../product_types/product_variables.md#sea_water_x_velocity), [`sea_water_y_velocity`](../product_types/product_variables.md#sea_water_y_velocity) | Optional | rotated grid |
| [`wave_signal`](../product_types/product_variables.md#wave_signal), [`background_noise`](../product_types/product_variables.md#background_noise), [`sea_surface_wave_mean_square_slope`](../product_types/product_variables.md#sea_surface_wave_mean_square_slope) | Optional | |
| [`measurement_quality`](../product_types/spatially_averaged.md#measurement_quality) | Recommended | |
| [`coordinates`](../metadata_attributes/variable_attributes.md#coordinates) `= "time longitude latitude"` on the data variables | Required | |
| [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) `= "crs"` on the data variables | Required | with `crs` |
| [`cell_methods`](../metadata_attributes/variable_attributes.md#cell_methods) `= "area: mean (comment: over the analysis windows of the measurement)"` on the means over the analysis windows | Recommended | |
| [`comment`](../metadata_attributes/variable_attributes.md#comment) on `sea_surface_wave_mean_period` and `sea_surface_wave_from_direction`, defining the mean | Recommended | |
| **Groups** | | |
| [`wave_calibration`](../metadata_attributes/wave_calibration.md) | Recommended | |
{: .contents-table }

## Example

A radar on a moving platform.

```
netcdf or_2025-01-15-11_wave_parameters {
dimensions:
        time = 29 ;
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
        double longitude(time) ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(time) ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_water_velocity(time) ; // optional
                eastward_sea_water_velocity:long_name = "eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:coordinates = "time longitude latitude" ;
                eastward_sea_water_velocity:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:ancillary_variables = "measurement_quality" ;
        double northward_sea_water_velocity(time) ; // optional
                northward_sea_water_velocity:long_name = "northward component of the near-surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
                northward_sea_water_velocity:coordinates = "time longitude latitude" ;
                northward_sea_water_velocity:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                northward_sea_water_velocity:grid_mapping = "crs" ;
                northward_sea_water_velocity:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_significant_height(time) ; // required: at least one of the five bulk parameters
                sea_surface_wave_significant_height:long_name = "significant wave height" ;
                sea_surface_wave_significant_height:standard_name = "sea_surface_wave_significant_height" ;
                sea_surface_wave_significant_height:units = "m" ;
                sea_surface_wave_significant_height:coordinates = "time longitude latitude" ;
                sea_surface_wave_significant_height:grid_mapping = "crs" ;
                sea_surface_wave_significant_height:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_from_direction_at_variance_spectral_density_maximum(time) ; // recommended
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:long_name = "peak wave direction" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_from_direction_at_variance_spectral_density_maximum" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:units = "degree" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:coordinates = "time longitude latitude" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_period_at_variance_spectral_density_maximum(time) ; // recommended
                sea_surface_wave_period_at_variance_spectral_density_maximum:long_name = "peak wave period" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_period_at_variance_spectral_density_maximum" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:units = "s" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:coordinates = "time longitude latitude" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_mean_period(time) ; // recommended
                sea_surface_wave_mean_period:long_name = "mean wave period" ;
                sea_surface_wave_mean_period:standard_name = "sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment" ;
                sea_surface_wave_mean_period:units = "s" ;
                sea_surface_wave_mean_period:comment = "energy-weighted mean wave period Tm01 calculated from zeroth and first spectral moments" ; // recommended
                sea_surface_wave_mean_period:coordinates = "time longitude latitude" ;
                sea_surface_wave_mean_period:grid_mapping = "crs" ;
                sea_surface_wave_mean_period:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_from_direction(time) ; // recommended
                sea_surface_wave_from_direction:long_name = "mean wave direction" ;
                sea_surface_wave_from_direction:standard_name = "sea_surface_wave_from_direction" ;
                sea_surface_wave_from_direction:units = "degree" ;
                sea_surface_wave_from_direction:comment = "energy-weighted mean direction the waves come from, calculated from the first directional moments of the spectrum" ; // recommended
                sea_surface_wave_from_direction:coordinates = "time longitude latitude" ;
                sea_surface_wave_from_direction:grid_mapping = "crs" ;
                sea_surface_wave_from_direction:ancillary_variables = "measurement_quality" ;
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
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN WAVES > SIGNIFICANT WAVE HEIGHT, EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE PERIOD, EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE DIRECTION" ; // highly recommended
                :platform_is_mobile = "true" ;
                :product_type = "wave_parameters" ;
                :summary = "Significant wave height and peak and mean wave periods and directions from a marine X-band radar on board R/V Ocean Research, derived from two-dimensional wavenumber spectra." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:59:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar peak and mean wave parameters from R/V Ocean Research" ; // highly recommended
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

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2025-01-15-11_wave_parameters {
dimensions:
        time = 29 ;
variables:
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude(time) ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(time) ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_significant_height(time) ; // required: at least one of the five bulk parameters
                sea_surface_wave_significant_height:long_name = "significant wave height" ;
                sea_surface_wave_significant_height:standard_name = "sea_surface_wave_significant_height" ;
                sea_surface_wave_significant_height:units = "m" ;
                sea_surface_wave_significant_height:coordinates = "time longitude latitude" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :platform_is_mobile = "true" ;
                :product_type = "wave_parameters" ;

}
```

## Example for a fixed platform

A radar on a fixed platform: the measurements form a [time series](../product_types/spatially_averaged.md#moving-and-fixed-platforms), identified by [`station`](../product_types/spatially_averaged.md#station) in place of the trajectory, with scalar [`longitude`](../product_types/spatially_averaged.md#longitude) and [`latitude`](../product_types/spatially_averaged.md#latitude) given under `data`.

```
netcdf or_2023-08-31-17_wave_parameters {
dimensions:
        time = 29 ;
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
        double longitude ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_water_velocity(time) ; // optional
                eastward_sea_water_velocity:long_name = "eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:coordinates = "time longitude latitude" ;
                eastward_sea_water_velocity:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:ancillary_variables = "measurement_quality" ;
        double northward_sea_water_velocity(time) ; // optional
                northward_sea_water_velocity:long_name = "northward component of the near-surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
                northward_sea_water_velocity:coordinates = "time longitude latitude" ;
                northward_sea_water_velocity:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                northward_sea_water_velocity:grid_mapping = "crs" ;
                northward_sea_water_velocity:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_significant_height(time) ; // required: at least one of the five bulk parameters
                sea_surface_wave_significant_height:long_name = "significant wave height" ;
                sea_surface_wave_significant_height:standard_name = "sea_surface_wave_significant_height" ;
                sea_surface_wave_significant_height:units = "m" ;
                sea_surface_wave_significant_height:coordinates = "time longitude latitude" ;
                sea_surface_wave_significant_height:grid_mapping = "crs" ;
                sea_surface_wave_significant_height:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_from_direction_at_variance_spectral_density_maximum(time) ; // recommended
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:long_name = "peak wave direction" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_from_direction_at_variance_spectral_density_maximum" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:units = "degree" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:coordinates = "time longitude latitude" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_period_at_variance_spectral_density_maximum(time) ; // recommended
                sea_surface_wave_period_at_variance_spectral_density_maximum:long_name = "peak wave period" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_period_at_variance_spectral_density_maximum" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:units = "s" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:coordinates = "time longitude latitude" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_mean_period(time) ; // recommended
                sea_surface_wave_mean_period:long_name = "mean wave period" ;
                sea_surface_wave_mean_period:standard_name = "sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment" ;
                sea_surface_wave_mean_period:units = "s" ;
                sea_surface_wave_mean_period:comment = "energy-weighted mean wave period Tm01 calculated from zeroth and first spectral moments" ; // recommended
                sea_surface_wave_mean_period:coordinates = "time longitude latitude" ;
                sea_surface_wave_mean_period:grid_mapping = "crs" ;
                sea_surface_wave_mean_period:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_from_direction(time) ; // recommended
                sea_surface_wave_from_direction:long_name = "mean wave direction" ;
                sea_surface_wave_from_direction:standard_name = "sea_surface_wave_from_direction" ;
                sea_surface_wave_from_direction:units = "degree" ;
                sea_surface_wave_from_direction:comment = "energy-weighted mean direction the waves come from, calculated from the first directional moments of the spectrum" ; // recommended
                sea_surface_wave_from_direction:coordinates = "time longitude latitude" ;
                sea_surface_wave_from_direction:grid_mapping = "crs" ;
                sea_surface_wave_from_direction:ancillary_variables = "measurement_quality" ;
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
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN WAVES > SIGNIFICANT WAVE HEIGHT, EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE PERIOD, EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE DIRECTION" ; // highly recommended
                :product_type = "wave_parameters" ;
                :summary = "Significant wave height and peak and mean wave periods and directions from a marine X-band radar at Ocean Research Station, derived from two-dimensional wavenumber spectra." ; // highly recommended
                :time_coverage_end = "2023-08-31T17:59:59Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar peak and mean wave parameters from Ocean Research Station" ; // highly recommended
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

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2023-08-31-17_wave_parameters {
dimensions:
        time = 29 ;
variables:
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_significant_height(time) ; // required: at least one of the five bulk parameters
                sea_surface_wave_significant_height:long_name = "significant wave height" ;
                sea_surface_wave_significant_height:standard_name = "sea_surface_wave_significant_height" ;
                sea_surface_wave_significant_height:units = "m" ;
                sea_surface_wave_significant_height:coordinates = "time longitude latitude" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "wave_parameters" ;
data:
        longitude = 7.9050 ;
        latitude = 54.1702 ;

}
```

## Example for a rotated grid

A radar on a fixed platform at a coastal site, whose vector components are given along the axes of a [rotated local grid](../georeferencing/index.md#rotated-local-grids) centered on the radar antenna: its axes follow the convention of Argus and CIRN, `x` cross-shore, positive offshore, and `y` along-shore, at a coast whose offshore normal points to 110°, so that the azimuth of the y axis is 20°. The [`crs`](../product_types/spatially_averaged.md#crs) gives `grid_mapping_name = "rotated_azimuthal_equidistant"` and [`azimuth_of_y_axis`](../metadata_attributes/variable_attributes.md#azimuth_of_y_axis), while `longitude` and `latitude` remain geographic coordinates, and the near-surface current is given in [`sea_water_x_velocity`](../product_types/product_variables.md#sea_water_x_velocity) and [`sea_water_y_velocity`](../product_types/product_variables.md#sea_water_y_velocity) in place of its eastward and northward components; the wave directions remain bearings from true north.

```
netcdf cr_2023-08-31-17_wave_parameters {
dimensions:
        time = 29 ;
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
                crs:comment = "Argus/CIRN axes: x cross-shore, positive offshore; y along-shore" ;
        string station ; // recommended
                station:long_name = "name of the radar station" ;
                station:cf_role = "timeseries_id" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_water_x_velocity(time) ; // optional
                sea_water_x_velocity:long_name = "offshore component of the near-surface current velocity" ;
                sea_water_x_velocity:standard_name = "sea_water_x_velocity" ;
                sea_water_x_velocity:units = "m s-1" ;
                sea_water_x_velocity:coordinates = "time longitude latitude" ;
                sea_water_x_velocity:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                sea_water_x_velocity:grid_mapping = "crs" ;
                sea_water_x_velocity:ancillary_variables = "measurement_quality" ;
        double sea_water_y_velocity(time) ; // optional
                sea_water_y_velocity:long_name = "along-shore component of the near-surface current velocity" ;
                sea_water_y_velocity:standard_name = "sea_water_y_velocity" ;
                sea_water_y_velocity:units = "m s-1" ;
                sea_water_y_velocity:coordinates = "time longitude latitude" ;
                sea_water_y_velocity:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                sea_water_y_velocity:grid_mapping = "crs" ;
                sea_water_y_velocity:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_significant_height(time) ; // required: at least one of the five bulk parameters
                sea_surface_wave_significant_height:long_name = "significant wave height" ;
                sea_surface_wave_significant_height:standard_name = "sea_surface_wave_significant_height" ;
                sea_surface_wave_significant_height:units = "m" ;
                sea_surface_wave_significant_height:coordinates = "time longitude latitude" ;
                sea_surface_wave_significant_height:grid_mapping = "crs" ;
                sea_surface_wave_significant_height:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_from_direction_at_variance_spectral_density_maximum(time) ; // recommended
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:long_name = "peak wave direction" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_from_direction_at_variance_spectral_density_maximum" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:units = "degree" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:coordinates = "time longitude latitude" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_period_at_variance_spectral_density_maximum(time) ; // recommended
                sea_surface_wave_period_at_variance_spectral_density_maximum:long_name = "peak wave period" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_period_at_variance_spectral_density_maximum" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:units = "s" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:coordinates = "time longitude latitude" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_mean_period(time) ; // recommended
                sea_surface_wave_mean_period:long_name = "mean wave period" ;
                sea_surface_wave_mean_period:standard_name = "sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment" ;
                sea_surface_wave_mean_period:units = "s" ;
                sea_surface_wave_mean_period:comment = "energy-weighted mean wave period Tm01 calculated from zeroth and first spectral moments" ; // recommended
                sea_surface_wave_mean_period:coordinates = "time longitude latitude" ;
                sea_surface_wave_mean_period:grid_mapping = "crs" ;
                sea_surface_wave_mean_period:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_from_direction(time) ; // recommended
                sea_surface_wave_from_direction:long_name = "mean wave direction" ;
                sea_surface_wave_from_direction:standard_name = "sea_surface_wave_from_direction" ;
                sea_surface_wave_from_direction:units = "degree" ;
                sea_surface_wave_from_direction:comment = "energy-weighted mean direction the waves come from, calculated from the first directional moments of the spectrum" ; // recommended
                sea_surface_wave_from_direction:coordinates = "time longitude latitude" ;
                sea_surface_wave_from_direction:grid_mapping = "crs" ;
                sea_surface_wave_from_direction:ancillary_variables = "measurement_quality" ;
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
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN WAVES > SIGNIFICANT WAVE HEIGHT, EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE PERIOD, EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE DIRECTION" ; // highly recommended
                :product_type = "wave_parameters" ;
                :summary = "Significant wave height and peak and mean wave periods and directions from a marine X-band radar at Coastal Research Station, derived from two-dimensional wavenumber spectra." ; // highly recommended
                :time_coverage_end = "2023-08-31T17:59:59Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar peak and mean wave parameters from Coastal Research Station" ; // highly recommended
                :analysis_window_motion = "earth_fixed" ; // optional
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 3840. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_analysis_windows = 6 ; // recommended
                :number_of_images = 160 ; // recommended
                :wave_frequency_frame = "intrinsic" ; // recommended
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
netcdf cr_2023-08-31-17_wave_parameters {
dimensions:
        time = 29 ;
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
                crs:comment = "Argus/CIRN axes: x cross-shore, positive offshore; y along-shore" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_significant_height(time) ; // required: at least one of the five bulk parameters
                sea_surface_wave_significant_height:long_name = "significant wave height" ;
                sea_surface_wave_significant_height:standard_name = "sea_surface_wave_significant_height" ;
                sea_surface_wave_significant_height:units = "m" ;
                sea_surface_wave_significant_height:coordinates = "time longitude latitude" ;
                sea_surface_wave_significant_height:grid_mapping = "crs" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "wave_parameters" ;
data:
        longitude = 7.9050 ;
        latitude = 54.1702 ;

}
```
