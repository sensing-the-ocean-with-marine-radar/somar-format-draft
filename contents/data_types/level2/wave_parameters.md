---
title: Peak and mean wave parameters (L2b)
layout: default
parent: Level 2 data
nav_order: 9
---

# L2b: Peak and mean wave parameters

Peak and mean wave parameters summarize each [two-dimensional wavenumber spectrum](wave_wavenumber_spectra.md) using standard bulk wave parameters: significant wave height (`sea_surface_wave_significant_height`), the peak wave period and peak wave direction (period and direction at the spectral maximum), and the mean wave period.
To aid interpretation and quality assessment, the wave-signal and background-noise spectral densities used to derive the significant wave height are also reported (`wave_signal`, `background_noise`), together with the near-surface current vector obtained from the same analysis window (see [Near-surface current maps](current_maps.md)) and a `measurement_quality` flag.
As for the wave spectra, a `sea_surface_wave_significant_height_calibration_status` global attribute documents the calibration source and date against which the significant wave height retrieval was calibrated.
The `longitude` and `latitude` of each measurement give the mean position of the analysis windows that contribute to it (see [Georeferencing](../../metadata_attributes/georeferencing.md#positions-of-analysis-windows)); the radar position itself may optionally be stored in `radar_longitude` and `radar_latitude`.

## Variables

The file holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Coordinate reference system (see [Georeferencing](../../metadata_attributes/georeferencing.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Start time of each measurement. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_east` | Mean longitude of the analysis windows contributing to each measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_north` | Mean latitude of the analysis windows contributing to each measurement. |
| `eastward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(time)`; `m s-1` | Eastward component of the near-surface current from the same analysis windows. |
| `northward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(time)`; `m s-1` | Northward component of the near-surface current from the same analysis windows. |
| `sea_surface_wave_significant_height`<br><small>[CF][cf-names]</small> | double `(time)`; `m` | Significant wave height. |
| `sea_surface_wave_from_direction_at_variance_spectral_density_maximum`<br><small>[CF][cf-names]</small> | double `(time)`; `degree` | Peak wave direction: the direction the waves come from at the spectral maximum. |
| `sea_surface_wave_period_at_variance_spectral_density_maximum`<br><small>[CF][cf-names]</small> | double `(time)`; `s` | Peak wave period: the period at the spectral maximum. |
| `sea_surface_wave_mean_period`<br><small>[CF][cf-names]</small> | double `(time)`; `s` | Mean wave period. |
| `wave_signal`<br><small>SOMaR</small> | double `(time)`; dimensionless | Spectral density of the wave signal in the radar images, used to derive the significant wave height. |
| `background_noise`<br><small>SOMaR</small> | double `(time)`; dimensionless | Spectral density of the background noise in the radar images, used to derive the significant wave height. |
| `measurement_quality`<br><small>SOMaR</small> | ubyte `(time)`; `0` or `1` | Quality flag: 0 is good, 1 is bad. |
{: .variable-table }

In addition to the [shared global attributes](../../metadata_attributes/index.md), the file carries the following global attribute.

| Attribute | Values | Description |
|---|---|---|
| `sea_surface_wave_significant_height_calibration_status`<br><small>SOMaR</small> | String; free text | The reference wave data and the date against which the wave energy density was calibrated. |
{: .attribute-table }

## Minimal example
```
netcdf or_2025-01-15-11_wave_parameters_average {
dimensions:
        time = 29 ;
variables:
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:authority_string = "EPSG:4326" ;
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
                eastward_sea_water_velocity:long_name = "eastward component of the near surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:coordinates = "longitude latitude" ;
                eastward_sea_water_velocity:grid_mapping = "crs" ;
        double northward_sea_water_velocity(time) ;
                northward_sea_water_velocity:long_name = "northward component of the near surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
                northward_sea_water_velocity:coordinates = "longitude latitude" ;
                northward_sea_water_velocity:grid_mapping = "crs" ;
        double sea_surface_wave_significant_height(time) ;
                sea_surface_wave_significant_height:long_name = "significant wave height" ;
                sea_surface_wave_significant_height:standard_name = "sea_surface_wave_significant_height" ;
                sea_surface_wave_significant_height:units = "m" ;
                sea_surface_wave_significant_height:coordinates = "longitude latitude" ;
                sea_surface_wave_significant_height:grid_mapping = "crs" ;
        double sea_surface_wave_from_direction_at_variance_spectral_density_maximum(time) ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:long_name = "peak wave direction" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_from_direction_at_variance_spectral_density_maximum" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:units = "degree" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:coordinates = "longitude latitude" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
        double sea_surface_wave_period_at_variance_spectral_density_maximum(time) ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:long_name = "peak wave period" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_period_at_variance_spectral_density_maximum" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:units = "s" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:coordinates = "longitude latitude" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:grid_mapping = "crs" ;
        double sea_surface_wave_mean_period(time) ;
                sea_surface_wave_mean_period:long_name = "mean wave period" ;
                sea_surface_wave_mean_period:standard_name = "sea_surface_wave_mean_period" ;
                sea_surface_wave_mean_period:units = "s" ;
                sea_surface_wave_mean_period:coordinates = "longitude latitude" ;
                sea_surface_wave_mean_period:grid_mapping = "crs" ;
        double wave_signal(time) ;
                wave_signal:long_name = "radar image spectral density of the wave signal" ;
                wave_signal:units = "1" ;
                wave_signal:coordinates = "longitude latitude" ;
                wave_signal:grid_mapping = "crs" ;
        double background_noise(time) ;
                background_noise:long_name = "radar image spectral density of the background noise" ;
                background_noise:units = "1" ;
                background_noise:coordinates = "longitude latitude" ;
                background_noise:grid_mapping = "crs" ;
        ubyte measurement_quality(time) ;
                measurement_quality:long_name = "measurement quality (0: good, 1: bad)" ;
                measurement_quality:flag_meanings = "good bad" ;
                measurement_quality:flag_values = 0UB, 1UB ;
                measurement_quality:coordinates = "longitude latitude" ;
                measurement_quality:grid_mapping = "crs" ;

// global attributes:
                :sea_surface_wave_significant_height_calibration_status = "Calibrated on 2025/01/06 using MFWAM global wave data as reference" ;
                :title = "Marine X-band radar derived mean and peak wave parameters with quality control flag from R/V Ocean Research" ;
                :summary = "The mean and peak wave parameters are derived from the mean two dimensional wavenumber wave energy density spectrum." ;
                :creator_email = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :history = "20250115T120500Z: File creation time" ;
                :processing_level = "L2b" ;
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
