---
title: Peak and mean wave parameters (L2b)
layout: default
parent: "Annex: Example products"
nav_order: 13
---

# L2b: Peak and mean wave parameters

{: .informative }
> This page is informative. The product type `wave_parameters` is one of the [spatially averaged products](../product_types/spatially_averaged.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../metadata_attributes/product_variables.md).

Peak and mean wave parameters (`wave_parameters`) summarize each [two-dimensional wavenumber spectrum](wave_wavenumber_spectra.md) using standard bulk wave parameters: significant wave height (`sea_surface_wave_significant_height`), the peak wave period and peak wave direction (period and direction at the spectral maximum), and the mean wave period and mean wave direction.
The peak and mean wave periods are intrinsic, i.e. relative to the moving water, or absolute, i.e. relative to the ground and including the Doppler shift by the current, as given by [`wave_frequency_frame`](../metadata_attributes/processing_parameters.md).
To aid interpretation and quality assessment, the quantities from which the significant wave height is derived may also be reported: the wave-signal and background-noise spectral densities (`wave_signal`, `background_noise`), whose ratio is the signal-to-noise ratio, for the signal-to-noise ratio method, or the mean square slope of the sea surface (`sea_surface_wave_mean_square_slope`) for the shadowing method; the calibration applies `hs_slope` and `hs_intercept` to the predictor `hs_predictor` computed from them. The wave parameters are given together with the near-surface current vector obtained from the same analysis windows, for platform-fixed windows after subtracting the platform velocity (see [Near-surface current maps](current_maps.md)) and a `measurement_quality` flag.

## Example

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
                eastward_sea_water_velocity:cell_methods = "area: mean" ; // recommended
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:ancillary_variables = "measurement_quality" ;
        double northward_sea_water_velocity(time) ; // optional
                northward_sea_water_velocity:long_name = "northward component of the near-surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
                northward_sea_water_velocity:coordinates = "time longitude latitude" ;
                northward_sea_water_velocity:cell_methods = "area: mean" ; // recommended
                northward_sea_water_velocity:grid_mapping = "crs" ;
                northward_sea_water_velocity:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_significant_height(time) ; // required: at least one of the five bulk parameters
                sea_surface_wave_significant_height:long_name = "significant wave height" ;
                sea_surface_wave_significant_height:standard_name = "sea_surface_wave_significant_height" ;
                sea_surface_wave_significant_height:units = "m" ;
                sea_surface_wave_significant_height:coordinates = "time longitude latitude" ;
                sea_surface_wave_significant_height:cell_methods = "area: mean" ; // recommended
                sea_surface_wave_significant_height:grid_mapping = "crs" ;
                sea_surface_wave_significant_height:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_from_direction_at_variance_spectral_density_maximum(time) ; // recommended
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:long_name = "peak wave direction" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_from_direction_at_variance_spectral_density_maximum" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:units = "degree" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:coordinates = "time longitude latitude" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:cell_methods = "area: mean" ; // recommended
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_period_at_variance_spectral_density_maximum(time) ; // recommended
                sea_surface_wave_period_at_variance_spectral_density_maximum:long_name = "peak wave period" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_period_at_variance_spectral_density_maximum" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:units = "s" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:coordinates = "time longitude latitude" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:cell_methods = "area: mean" ; // recommended
                sea_surface_wave_period_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_mean_period(time) ; // recommended
                sea_surface_wave_mean_period:long_name = "mean wave period" ;
                sea_surface_wave_mean_period:standard_name = "sea_surface_wave_mean_period" ;
                sea_surface_wave_mean_period:units = "s" ;
                sea_surface_wave_mean_period:comment = "energy-weighted mean wave period Tm01 calculated from zeroth and first spectral moments" ; // recommended
                sea_surface_wave_mean_period:coordinates = "time longitude latitude" ;
                sea_surface_wave_mean_period:cell_methods = "area: mean" ; // recommended
                sea_surface_wave_mean_period:grid_mapping = "crs" ;
                sea_surface_wave_mean_period:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_from_direction(time) ; // recommended
                sea_surface_wave_from_direction:long_name = "mean wave direction" ;
                sea_surface_wave_from_direction:standard_name = "sea_surface_wave_from_direction" ;
                sea_surface_wave_from_direction:units = "degree" ;
                sea_surface_wave_from_direction:comment = "energy-weighted mean direction the waves come from, calculated from the first directional moments of the spectrum" ; // recommended
                sea_surface_wave_from_direction:coordinates = "time longitude latitude" ;
                sea_surface_wave_from_direction:cell_methods = "area: mean" ; // recommended
                sea_surface_wave_from_direction:grid_mapping = "crs" ;
                sea_surface_wave_from_direction:ancillary_variables = "measurement_quality" ;
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
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN WAVES > SIGNIFICANT WAVE HEIGHT, EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE PERIOD, EARTH SCIENCE > OCEANS > OCEAN WAVES > WAVE DIRECTION" ; // highly recommended
                :platform_is_mobile = "true" ; // required: the platform moves
                :product_type = "wave_parameters" ;
                :summary = "Significant wave height and peak and mean wave periods and directions from a marine X-band radar on board R/V Ocean Research, derived from two-dimensional wavenumber spectra." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:59:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar peak and mean wave parameters from R/V Ocean Research" ; // highly recommended
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
