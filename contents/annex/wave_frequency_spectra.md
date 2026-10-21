---
title: Surface wave one-dimensional frequency spectra (L2b)
layout: default
parent: "Annex: Example products"
nav_order: 12
---

# L2b: Surface wave one-dimensional frequency spectra

{: .informative }
> This page is informative. The product type `wave_frequency_spectra` is one of the [spatially averaged products](../product_types/level2/spatially_averaged.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Level 2 variables](../metadata_attributes/level2_variables.md).

One-dimensional frequency spectra (`wave_frequency_spectra`) give the (time-averaged) wave energy density, `sea_surface_wave_variance_spectral_density(time, wave_frequency)`, for each measurement, averaged over the analysis windows that contribute to it, together with the directional spread (`sea_surface_wave_directional_spread`) and mean wave direction (`sea_surface_wave_mean_from_direction`) in each frequency band.
They are derived from the [two-dimensional wavenumber spectra](wave_wavenumber_spectra.md) using the linear wave dispersion relation, which relates each wavenumber to its corresponding wave frequency.
The frequencies are intrinsic, i.e. relative to the moving water, if this dispersion relation omits the current, or absolute, i.e. relative to the ground, if it includes the Doppler shift by the current; which of the two is given by [`wave_frequency_frame`](../product_types/level2/index.md#processing-parameters).

## Example

```
netcdf or_2025-01-15-11_wave_frequency_spectra {
dimensions:
        time = 29 ;
        wave_frequency = 512 ;
variables:
        char crs ; // recommended
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
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
                sea_surface_wave_variance_spectral_density:cell_methods = "area: mean" ; // recommended
                sea_surface_wave_variance_spectral_density:grid_mapping = "crs" ;
                sea_surface_wave_variance_spectral_density:ancillary_variables = "measurement_quality" ;
        float sea_surface_wave_directional_spread(time, wave_frequency) ; // optional
                sea_surface_wave_directional_spread:long_name = "wave directional spread in each frequency band" ;
                sea_surface_wave_directional_spread:standard_name = "sea_surface_wave_directional_spread" ;
                sea_surface_wave_directional_spread:units = "degree" ;
                sea_surface_wave_directional_spread:coordinates = "time longitude latitude" ;
                sea_surface_wave_directional_spread:cell_methods = "area: mean" ; // recommended
                sea_surface_wave_directional_spread:grid_mapping = "crs" ;
                sea_surface_wave_directional_spread:ancillary_variables = "measurement_quality" ;
        float sea_surface_wave_mean_from_direction(time, wave_frequency) ; // optional
                sea_surface_wave_mean_from_direction:long_name = "mean wave direction in each frequency band" ;
                sea_surface_wave_mean_from_direction:standard_name = "sea_surface_wave_mean_from_direction" ;
                sea_surface_wave_mean_from_direction:units = "degree" ;
                sea_surface_wave_mean_from_direction:coordinates = "time longitude latitude" ;
                sea_surface_wave_mean_from_direction:cell_methods = "area: mean" ; // recommended
                sea_surface_wave_mean_from_direction:grid_mapping = "crs" ;
                sea_surface_wave_mean_from_direction:ancillary_variables = "measurement_quality" ;
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
                :product_type = "wave_frequency_spectra" ;
                :summary = "One-dimensional surface wave frequency spectra, with mean wave direction and directional spread, from a marine X-band radar on board R/V Ocean Research, derived from two-dimensional wavenumber spectra with the linear dispersion relation." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:59:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar surface wave one-dimensional frequency spectra from R/V Ocean Research" ; // highly recommended
                :analysis_window_motion = "earth_fixed" ; // optional
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 3840. ; // recommended
                :number_of_analysis_windows = 6 ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_images = 160 ; // recommended
                :wave_frequency_frame = "intrinsic" ; // recommended

group: wave_calibration { ... } // recommended; as in the example under Wave calibration parameters
}
```
