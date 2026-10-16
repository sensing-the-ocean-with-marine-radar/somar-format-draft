---
title: Peak and mean wave parameters (L2b)
layout: default
parent: Level 2 products
grand_parent: SOMaR product types
nav_order: 9
---

# L2b: Peak and mean wave parameters

Peak and mean wave parameters (`wave_parameters`, short `wav_params`) summarize each [two-dimensional wavenumber spectrum](wave_wavenumber_spectra.md) using standard bulk wave parameters: significant wave height (`sea_surface_wave_significant_height`), the peak wave period and peak wave direction (period and direction at the spectral maximum), and the mean wave period.
To aid interpretation and quality assessment, the wave-signal and background-noise spectral densities are also reported (`wave_signal`, `background_noise`); their ratio is the signal-to-noise ratio from which the significant wave height is derived with `hs_slope` and `hs_intercept`. They are given together with the near-surface current vector obtained from the same analysis windows (see [Near-surface current maps](current_maps.md)) and a `measurement_quality` flag.
The calibration parameters of the wave retrieval are recorded in the `wave_calibration` group (see [Calibration](wave_wavenumber_spectra.md#calibration)).
The `longitude` and `latitude` of each measurement give the mean position of the analysis windows that contribute to it (see [Georeferencing](../../georeferencing/index.md#positions-of-analysis-windows)); the radar position itself may optionally be stored in `radar_longitude` and `radar_latitude`.

## Variables

The file holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Start time of each measurement. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_east` | Mean longitude of the analysis windows contributing to each measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_north` | Mean latitude of the analysis windows contributing to each measurement. |
| `eastward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(time)`; `m s-1` | Eastward component of the near-surface current from the same analysis windows. |
| `northward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(time)`; `m s-1` | Northward component of the near-surface current from the same analysis windows. |
| `sea_surface_wave_significant_height`<br><small>[CF][cf-names]</small> | double `(time)`; `m` | Significant wave height. |
| `sea_surface_wave_from_direction_at_variance_spectral_density_maximum`<br><small>[CF][cf-names]</small> | double `(time)`; `degree` | Peak wave direction: the direction the waves come from at the spectral maximum. |
| `sea_surface_wave_period_at_variance_spectral_density_maximum`<br><small>[CF][cf-names]</small> | double `(time)`; `s` | Peak wave period: the period at the spectral maximum. |
| `sea_surface_wave_mean_period`<br><small>[CF][cf-names]</small> | double `(time)`; `s` | Mean wave period (e.g. $T_{m01}$ or $T_{m02}$; the spectral moment definition should be documented in a `comment` attribute). |
| `wave_signal`<br><small>SOMaR</small> | double `(time)`; `1` | Spectral density of the wave signal in the radar images, used to derive the significant wave height. |
| `background_noise`<br><small>SOMaR</small> | double `(time)`; `1` | Spectral density of the background noise in the radar images, used to derive the significant wave height. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(time)`; `0` or `1` | Quality flag: 0 is good, 1 is bad. |
{: .variable-table }

## Minimal example
```
netcdf or_2025-01-15-11_wave_parameters_average {
dimensions:
        time = 29 ;
variables:
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
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
                :product_type = "wave_parameters" ;

group: wave_calibration {
  variables:
        double hs_intercept ;
                hs_intercept:units = "m" ;
                hs_intercept:long_name = "intercept of the significant wave height calibration" ;
        double hs_slope ;
                hs_slope:units = "m" ;
                hs_slope:long_name = "slope of the significant wave height calibration" ;
        string hs_predictor ;
                hs_predictor:long_name = "quantity to which the significant wave height calibration is applied" ;
        string mtf_form ;
                mtf_form:long_name = "form of the modulation transfer function" ;
                mtf_form:references = "Nieto Borge, J. C., G. Rodriguez Rodriguez, K. Hessner, and P. Izquierdo Gonzalez (2004), Inversion of marine radar images for surface wave analysis, J. Atmos. Oceanic Technol., 21(8), 1291-1300, doi:10.1175/1520-0426(2004)021<1291:IOMRIF>2.0.CO;2" ;
        double mtf_exponent ;
                mtf_exponent:units = "1" ;
                mtf_exponent:long_name = "exponent of the power-law modulation transfer function" ;

  // group attributes:
                :calibration_reference = "MFWAM global wave data" ;
                :calibration_date = "2025-01-06" ;
  data:
        hs_intercept = 0.1 ;
        hs_slope = 1.5 ;
        hs_predictor = "sqrt_signal_to_noise_ratio" ;
        mtf_form = "power_law" ;
        mtf_exponent = 1.2 ;
  } // group wave_calibration
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
