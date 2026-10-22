---
title: Surface wave frequency-direction spectra (L2b)
layout: default
parent: "Annex: Example products"
nav_order: 12
---

# L2b: Surface wave frequency-direction spectra

{: .informative }
> This page is informative. The product type `wave_frequency_direction_spectra` is one of the [spatially averaged products](../product_types/spatially_averaged.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md). The [file contents](#file-contents) summarize these definitions for this product; where they differ, the definitions apply.

Frequency-direction spectra (`wave_frequency_direction_spectra`) give the (time-averaged) wave energy density, `sea_surface_wave_directional_variance_spectral_density(time, wave_frequency, sea_surface_wave_from_direction)`, as a function of wave frequency and wave direction for each measurement, averaged over the analysis windows that contribute to it.
They are derived from the [two-dimensional wavenumber spectra](wave_wavenumber_spectra.md) using the linear wave dispersion relation, which relates each wavenumber to its corresponding wave frequency.
The frequencies are intrinsic, i.e. relative to the moving water, if this dispersion relation omits the current, or absolute, i.e. relative to the ground, if it includes the Doppler shift by the current; which of the two is given by [`wave_frequency_frame`](../metadata_attributes/processing_parameters.md#wave_frequency_frame).
Integrating over direction yields the [one-dimensional frequency spectra](wave_frequency_spectra.md).

## File contents

**Layout.** On a moving platform, the file holds a [trajectory](../product_types/spatially_averaged.md#moving-and-fixed-platforms) along the dimension `time`, with `longitude(time)` and `latitude(time)`; on a fixed platform, it holds a time series along the dimension `time`, with scalar `longitude` and `latitude`.

A file of this product holds the following items; each links to its definition, and the condition, where one is given, states when the tier applies.

| Item | Tier | Condition |
|---|---|---|
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`product_type`](../metadata_attributes/mandatory_global.md#product_type) `= "wave_frequency_direction_spectra"` | Required | |
| [`platform_is_mobile`](../metadata_attributes/optional_global.md#platform_is_mobile) `= "true"` | Required | moving platform |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| [`featureType`](../metadata_attributes/optional_global.md#featureType) `= "trajectory"` or `"timeSeries"` | Recommended | |
| [`analysis_window_shape`](../metadata_attributes/processing_parameters.md#analysis_window_shape), [`analysis_window_size`](../metadata_attributes/processing_parameters.md#analysis_window_size), [`measurement_duration`](../metadata_attributes/processing_parameters.md#measurement_duration), [`number_of_analysis_windows`](../metadata_attributes/processing_parameters.md#number_of_analysis_windows), [`number_of_images`](../metadata_attributes/processing_parameters.md#number_of_images), [`wave_frequency_frame`](../metadata_attributes/processing_parameters.md#wave_frequency_frame) | Recommended | |
| [`analysis_window_motion`](../metadata_attributes/processing_parameters.md#analysis_window_motion), [`retrieval_method`](../metadata_attributes/processing_parameters.md#retrieval_method) | Optional | |
| **Variables** | | |
| [`time`](../product_types/spatially_averaged.md#time), [`longitude`](../product_types/spatially_averaged.md#longitude), [`latitude`](../product_types/spatially_averaged.md#latitude) | Required | |
| [`time_bounds`](../product_types/spatially_averaged.md#time_bounds) | Optional | |
| [`crs`](../product_types/spatially_averaged.md#crs) | Recommended | |
| [`trajectory`](../product_types/spatially_averaged.md#trajectory) | Recommended | moving platform |
| [`station`](../product_types/spatially_averaged.md#station) | Recommended | fixed platform |
| [`platform_speed_wrt_ground`](../product_types/spatially_averaged.md#platform_speed_wrt_ground), [`platform_course`](../product_types/spatially_averaged.md#platform_course) | Required | `analysis_window_motion = "platform_fixed"` |
| [`radar_latitude`](../product_types/spatially_averaged.md#radar_latitude), [`radar_longitude`](../product_types/spatially_averaged.md#radar_longitude) | Optional | |
| [`wave_frequency`](../product_types/product_variables.md#wave_frequency), [`sea_surface_wave_from_direction`](../product_types/product_variables.md#sea_surface_wave_from_direction), [`sea_surface_wave_directional_variance_spectral_density`](../product_types/product_variables.md#sea_surface_wave_directional_variance_spectral_density) | Required | |
| [`eastward_sea_water_velocity`](../product_types/spatially_averaged.md#eastward_sea_water_velocity), [`northward_sea_water_velocity`](../product_types/spatially_averaged.md#northward_sea_water_velocity) | Optional | |
| [`measurement_quality`](../product_types/spatially_averaged.md#measurement_quality) | Recommended | |
| [`coordinates`](../metadata_attributes/variable_attributes.md#coordinates) `= "time longitude latitude"` on the data variables | Required | |
| [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) `= "crs"` on the data variables | Required | with `crs` |
| [`cell_methods`](../metadata_attributes/variable_attributes.md#cell_methods) `= "area: mean (comment: over the analysis windows of the measurement)"` on the spectrum and the near-surface current | Recommended | |
| **Groups** | | |
| [`wave_calibration`](../metadata_attributes/wave_calibration.md) | Recommended | |
{: .contents-table }

## Example

The example below is illustrative; it is not yet based on an existing NetCDF file.

```
netcdf or_2025-01-15-11_wave_frequency_direction_spectra {
dimensions:
        time = 29 ;
        wave_frequency = 512 ;
        sea_surface_wave_from_direction = 360 ;
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
        double sea_surface_wave_from_direction(sea_surface_wave_from_direction) ;
                sea_surface_wave_from_direction:long_name = "direction from which the waves come" ;
                sea_surface_wave_from_direction:standard_name = "sea_surface_wave_from_direction" ;
                sea_surface_wave_from_direction:units = "degree" ;
        double longitude(time) ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(time) ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_directional_variance_spectral_density(time, wave_frequency, sea_surface_wave_from_direction) ;
                sea_surface_wave_directional_variance_spectral_density:long_name = "wave energy density two dimensional frequency spectrum" ;
                sea_surface_wave_directional_variance_spectral_density:standard_name = "sea_surface_wave_directional_variance_spectral_density" ;
                sea_surface_wave_directional_variance_spectral_density:units = "m2 s degree-1" ;
                sea_surface_wave_directional_variance_spectral_density:coordinates = "time longitude latitude" ;
                sea_surface_wave_directional_variance_spectral_density:cell_methods = "area: mean (comment: over the analysis windows of the measurement)" ; // recommended
                sea_surface_wave_directional_variance_spectral_density:grid_mapping = "crs" ;
                sea_surface_wave_directional_variance_spectral_density:ancillary_variables = "measurement_quality" ;
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
                :product_type = "wave_frequency_direction_spectra" ;
                :summary = "Surface wave frequency-direction spectra from a marine X-band radar on board R/V Ocean Research, derived from two-dimensional wavenumber spectra with the linear dispersion relation." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:59:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar surface wave frequency-direction spectra from R/V Ocean Research" ; // highly recommended
                :analysis_window_motion = "earth_fixed" ; // optional
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 3840. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_analysis_windows = 6 ; // recommended
                :number_of_images = 160 ; // recommended
                :wave_frequency_frame = "intrinsic" ; // recommended

group: wave_calibration { ... } // recommended; as in the example under Wave calibration parameters
}
```

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2025-01-15-11_wave_frequency_direction_spectra {
dimensions:
        time = 29 ;
        wave_frequency = 512 ;
        sea_surface_wave_from_direction = 360 ;
variables:
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double wave_frequency(wave_frequency) ;
                wave_frequency:long_name = "wave frequency" ;
                wave_frequency:standard_name = "wave_frequency" ;
                wave_frequency:units = "s-1" ;
        double sea_surface_wave_from_direction(sea_surface_wave_from_direction) ;
                sea_surface_wave_from_direction:long_name = "direction from which the waves come" ;
                sea_surface_wave_from_direction:standard_name = "sea_surface_wave_from_direction" ;
                sea_surface_wave_from_direction:units = "degree" ;
        double longitude(time) ;
                longitude:long_name = "mean longitude of wave measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(time) ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_surface_wave_directional_variance_spectral_density(time, wave_frequency, sea_surface_wave_from_direction) ;
                sea_surface_wave_directional_variance_spectral_density:long_name = "wave energy density two dimensional frequency spectrum" ;
                sea_surface_wave_directional_variance_spectral_density:standard_name = "sea_surface_wave_directional_variance_spectral_density" ;
                sea_surface_wave_directional_variance_spectral_density:units = "m2 s degree-1" ;
                sea_surface_wave_directional_variance_spectral_density:coordinates = "time longitude latitude" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :platform_is_mobile = "true" ;
                :product_type = "wave_frequency_direction_spectra" ;

}
```
