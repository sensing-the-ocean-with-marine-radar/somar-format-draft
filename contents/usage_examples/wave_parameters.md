---
title: Peak and mean wave parameters (L2b)
layout: default
parent: Usage examples
grand_parent: SOMaR product types
nav_order: 10
---

# L2b: Peak and mean wave parameters

Peak and mean wave parameters (`wave_parameters`) summarize each [two-dimensional wavenumber spectrum](wave_wavenumber_spectra.md) using standard bulk wave parameters: significant wave height (`sea_surface_wave_significant_height`), the peak wave period and peak wave direction (period and direction at the spectral maximum), and the mean wave period and mean wave direction.
To aid interpretation and quality assessment, the wave-signal and background-noise spectral densities are also reported (`wave_signal`, `background_noise`); their ratio is the signal-to-noise ratio from which the significant wave height is derived with `hs_predictor`, `hs_slope`, and `hs_intercept`. They are given together with the near-surface current vector obtained from the same analysis windows (see [Near-surface current maps](current_maps.md)) and a `measurement_quality` flag.
The calibration parameters of the wave retrieval are recorded in the `wave_calibration` group (see [Wave calibration parameters](../../metadata_attributes/wave_calibration.md)).
The analysis windows and the processing parameters are described under [Wave products](index.md#wave-products) and [Processing parameters](index.md#processing-parameters).
The `longitude` and `latitude` of each measurement give the mean position of the analysis windows that contribute to it (see [Georeferencing](../../georeferencing/index.md#positions-of-analysis-windows)); the radar position itself may optionally be stored in `radar_longitude` and `radar_latitude`.

## Variables

The file holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required. Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each measurement. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_east` | Required. Mean longitude of the analysis windows contributing to each measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_north` | Required. Mean latitude of the analysis windows contributing to each measurement. |
| `eastward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(time)`; `m s-1` | Optional. Eastward component of the near-surface current from the same analysis windows. |
| `northward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(time)`; `m s-1` | Optional. Northward component of the near-surface current from the same analysis windows. |
| `sea_surface_wave_significant_height`<br><small>[CF][cf-names]</small> | double `(time)`; `m` | Required. Significant wave height. |
| `sea_surface_wave_from_direction_at_variance_spectral_density_maximum`<br><small>[CF][cf-names]</small> | double `(time)`; `degree` | Required. Peak wave direction: the direction the waves come from at the spectral maximum. |
| `sea_surface_wave_period_at_variance_spectral_density_maximum`<br><small>[CF][cf-names]</small> | double `(time)`; `s` | Required. Peak wave period: the period at the spectral maximum. |
| `sea_surface_wave_mean_period`<br><small>[CF][cf-names]</small> | double `(time)`; `s` | Required. Mean wave period (e.g. $T_{m01}$ or $T_{m02}$; the spectral moment definition should be documented in a `comment` attribute). |
| `sea_surface_wave_from_direction`<br><small>[CF][cf-names]</small> | double `(time)`; `degree` | Required. Mean wave direction: the mean direction the waves come from (the definition should be documented in a `comment` attribute). |
| `wave_signal`<br><small>SOMaR</small> | double `(time)`; `1` | Optional. Spectral density of the wave signal in the radar images, used to derive the significant wave height. |
| `background_noise`<br><small>SOMaR</small> | double `(time)`; `1` | Optional. Spectral density of the background noise in the radar images, used to derive the significant wave height. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(time)`; `0` or `1` | Required. Quality flag: 0 is good, 1 is bad. |
{: .variable-table }

## Minimal example
```
netcdf or_2025-01-15-11_wave_parameters {
dimensions:
        time = 29 ;
variables:
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
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
        double eastward_sea_water_velocity(time) ;
                eastward_sea_water_velocity:long_name = "eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:coordinates = "longitude latitude" ;
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:ancillary_variables = "measurement_quality" ;
        double northward_sea_water_velocity(time) ;
                northward_sea_water_velocity:long_name = "northward component of the near-surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
                northward_sea_water_velocity:coordinates = "longitude latitude" ;
                northward_sea_water_velocity:grid_mapping = "crs" ;
                northward_sea_water_velocity:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_significant_height(time) ;
                sea_surface_wave_significant_height:long_name = "significant wave height" ;
                sea_surface_wave_significant_height:standard_name = "sea_surface_wave_significant_height" ;
                sea_surface_wave_significant_height:units = "m" ;
                sea_surface_wave_significant_height:coordinates = "longitude latitude" ;
                sea_surface_wave_significant_height:grid_mapping = "crs" ;
                sea_surface_wave_significant_height:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_from_direction_at_variance_spectral_density_maximum(time) ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:long_name = "peak wave direction" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_from_direction_at_variance_spectral_density_maximum" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:units = "degree" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:coordinates = "longitude latitude" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_period_at_variance_spectral_density_maximum(time) ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:long_name = "peak wave period" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_period_at_variance_spectral_density_maximum" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:units = "s" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:coordinates = "longitude latitude" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_mean_period(time) ;
                sea_surface_wave_mean_period:long_name = "mean wave period" ;
                sea_surface_wave_mean_period:standard_name = "sea_surface_wave_mean_period" ;
                sea_surface_wave_mean_period:units = "s" ;
                sea_surface_wave_mean_period:comment = "energy-weighted mean wave period Tm01 calculated from zeroth and first spectral moments" ;
                sea_surface_wave_mean_period:coordinates = "longitude latitude" ;
                sea_surface_wave_mean_period:grid_mapping = "crs" ;
                sea_surface_wave_mean_period:ancillary_variables = "measurement_quality" ;
        double sea_surface_wave_from_direction(time) ;
                sea_surface_wave_from_direction:long_name = "mean wave direction" ;
                sea_surface_wave_from_direction:standard_name = "sea_surface_wave_from_direction" ;
                sea_surface_wave_from_direction:units = "degree" ;
                sea_surface_wave_from_direction:comment = "energy-weighted mean direction the waves come from, calculated from the first directional moments of the spectrum" ;
                sea_surface_wave_from_direction:coordinates = "longitude latitude" ;
                sea_surface_wave_from_direction:grid_mapping = "crs" ;
                sea_surface_wave_from_direction:ancillary_variables = "measurement_quality" ;
        double wave_signal(time) ;
                wave_signal:long_name = "radar image spectral density of the wave signal" ;
                wave_signal:units = "1" ;
                wave_signal:coordinates = "longitude latitude" ;
                wave_signal:grid_mapping = "crs" ;
                wave_signal:ancillary_variables = "measurement_quality" ;
        double background_noise(time) ;
                background_noise:long_name = "radar image spectral density of the background noise" ;
                background_noise:units = "1" ;
                background_noise:coordinates = "longitude latitude" ;
                background_noise:grid_mapping = "crs" ;
                background_noise:ancillary_variables = "measurement_quality" ;
        ubyte measurement_quality(time) ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:long_name = "measurement quality (0: good, 1: bad)" ;
                measurement_quality:flag_meanings = "good bad" ;
                measurement_quality:flag_values = 0UB, 1UB ;
                measurement_quality:valid_range = 0UB, 1UB ;
                measurement_quality:_FillValue = 255UB ;
                measurement_quality:coordinates = "longitude latitude" ;
                measurement_quality:grid_mapping = "crs" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 15.0012 ;
                :geospatial_lat_min = 14.9478 ;
                :geospatial_lon_max = 145.9486 ;
                :geospatial_lon_min = 145.8631 ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :product_type = "wave_parameters" ;
                :time_coverage_end = "2025-01-15T11:59:59Z" ;
                :time_coverage_start = "2025-01-15T11:00:00Z" ;
                :title = "Marine X-band radar peak and mean wave parameters from R/V Ocean Research" ;
                :analysis_window_size = 3840. ;
                :number_of_analysis_windows = 6 ;
                :measurement_duration = 240. ;
                :number_of_images = 160 ;

group: wave_calibration { ... } // as in the example under Wave calibration parameters
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
