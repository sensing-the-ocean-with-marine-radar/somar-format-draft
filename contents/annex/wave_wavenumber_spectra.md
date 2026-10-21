---
title: Surface wave two-dimensional wavenumber spectra (L2a)
layout: default
parent: "Annex: Example products"
nav_order: 10
---

# L2a: Surface wave two-dimensional wavenumber spectra

{: .informative }
> This page is informative. The product type `wave_wavenumber_spectra` is one of the [spatially averaged products](../product_types/spatially_averaged.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md).

Two-dimensional wavenumber spectra (`wave_wavenumber_spectra`) give the (time-averaged) wave energy density, `sea_surface_wave_wavenumber_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber)`, as a function of the two horizontal wavenumber components for each measurement, averaged over the analysis windows that contribute to it.
They are retrieved from the wavenumber-frequency spectra of local radar image analysis windows, as used for the [near-surface current retrieval](current_maps.md), by keeping the wave signal that follows the dispersion relation (Young et al. [1985](../references/index.md#young-1985)).
The Level 2b [frequency-direction spectra](wave_frequency_direction_spectra.md), [one-dimensional frequency spectra](wave_frequency_spectra.md), and [peak and mean wave parameters](wave_parameters.md) are derived from these spectra.
The wave energy density is calibrated, typically against a reference wave data set (see [Wave calibration parameters](../metadata_attributes/wave_calibration.md)).
The quantities from which the calibration derives the significant wave height may be stored as for the [wave parameters](wave_parameters.md): `wave_signal` and `background_noise` for the signal-to-noise ratio method, or `sea_surface_wave_mean_square_slope` for the shadowing method.

## Example

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
                eastward_wave_wavenumber:long_name = "eastward component of the wave wavenumber" ;
                eastward_wave_wavenumber:units = "m-1" ;
        double northward_wave_wavenumber(northward_wave_wavenumber) ;
                northward_wave_wavenumber:long_name = "northward component of the wave wavenumber" ;
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
                sea_surface_wave_wavenumber_variance_spectral_density:cell_methods = "area: mean" ; // recommended
                sea_surface_wave_wavenumber_variance_spectral_density:grid_mapping = "crs" ;
                sea_surface_wave_wavenumber_variance_spectral_density:ancillary_variables = "measurement_quality" ;
        double wave_signal(time) ; // optional
                wave_signal:long_name = "radar image spectral density of the wave signal" ;
                wave_signal:units = "1" ;
                wave_signal:coordinates = "time longitude latitude" ;
                wave_signal:cell_methods = "area: mean" ; // recommended
                wave_signal:grid_mapping = "crs" ;
                wave_signal:ancillary_variables = "measurement_quality" ;
        double background_noise(time) ; // optional
                background_noise:long_name = "radar image spectral density of the background noise" ;
                background_noise:units = "1" ;
                background_noise:coordinates = "time longitude latitude" ;
                background_noise:cell_methods = "area: mean" ; // recommended
                background_noise:grid_mapping = "crs" ;
                background_noise:ancillary_variables = "measurement_quality" ;
        ubyte measurement_quality(time) ; // recommended
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:long_name = "measurement quality (0: good, 1-63: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold wave_steepness_above_threshold invalid_peak number_of_temporal_neighbors_below_threshold rain_contamination" ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB ;
                measurement_quality:valid_range = 0UB, 63UB ;
                measurement_quality:_FillValue = 255UB ;
                measurement_quality:coordinates = "time longitude latitude" ;
                measurement_quality:grid_mapping = "crs" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :featureType = "trajectory" ; // recommended
                :geospatial_lat_max = 15.0012 ; // recommended
                :geospatial_lat_min = 14.9478 ; // recommended
                :geospatial_lon_max = 145.9486 ; // recommended
                :geospatial_lon_min = 145.8631 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE SPECTRA" ; // highly recommended
                :platform_is_mobile = "true" ; // required: the platform moves
                :product_type = "wave_wavenumber_spectra" ;
                :summary = "Two-dimensional surface wave wavenumber spectra from a marine X-band radar on board R/V Ocean Research, retrieved from 240 s image sequences in analysis windows fixed to the Earth and averaged over the windows of each measurement." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:59:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar surface wave two-dimensional wavenumber spectra from R/V Ocean Research" ; // highly recommended
                :analysis_window_motion = "earth_fixed" ; // optional
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 3840. ; // recommended
                :number_of_analysis_windows = 6 ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_images = 160 ; // recommended

group: wave_calibration { ... } // recommended; as in the example under Wave calibration parameters
}
```
