---
title: Surface wave one-dimensional frequency spectra (L2b)
layout: default
parent: Level 2 data
nav_order: 8
---

# L2b: Surface wave one-dimensional frequency spectra

One-dimensional frequency spectra give the (time-averaged) wave energy density, `sea_surface_wave_variance_spectral_density(time, wave_frequency)`, for each analysis window, together with the directional spread (`sea_surface_wave_directional_spread`) and mean wave direction (`sea_surface_wave_mean_from_direction`) in each frequency band.
They are derived from the [two-dimensional wavenumber spectra](wave_wavenumber_spectra.md) using the linear wave dispersion relation, which relates each wavenumber to its corresponding wave frequency.
The calibration parameters of the wave retrieval are recorded in the `wave_calibration` group (see [Calibration](wave_wavenumber_spectra.md#calibration)).
The `longitude` and `latitude` of each measurement give the mean position of the analysis windows that contribute to it (see [Georeferencing](../../metadata_attributes/georeferencing.md#positions-of-analysis-windows)); the radar position itself may optionally be stored in `radar_longitude` and `radar_latitude`.

## Variables

The file holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Coordinate reference system (see [Georeferencing](../../metadata_attributes/georeferencing.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Start time of each measurement. |
| `wave_frequency`<br><small>[CF][cf-names]</small> | double `(wave_frequency)`; `s-1` | Wave frequency. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_east` | Mean longitude of the analysis windows contributing to each measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_north` | Mean latitude of the analysis windows contributing to each measurement. |
| `sea_surface_wave_variance_spectral_density`<br><small>[CF][cf-names]</small> | float `(time, wave_frequency)`; `m2 s` | Wave energy density as a function of frequency. |
| `sea_surface_wave_directional_spread`<br><small>[CF][cf-names]</small> | float `(time, wave_frequency)`; `degree` | Directional spread of the waves in each frequency band. |
| `sea_surface_wave_mean_from_direction`<br><small>[CF][cf-names]</small> | float `(time, wave_frequency)`; `degree` | Mean direction the waves come from in each frequency band. |
| `measurement_quality`<br><small>SOMaR</small> | ubyte `(time)`; `0` or `1` | Quality flag: 0 is good, 1 is bad. |
{: .variable-table }

## Minimal example
```
netcdf or_2025-01-15-11_wave_spectrograms_average {
dimensions:
        time = 29 ;
        wave_frequency = 512 ;
variables:
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:authority_string = "EPSG:4326" ;
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
                sea_surface_wave_variance_spectral_density:coordinates = "longitude latitude" ;
                sea_surface_wave_variance_spectral_density:grid_mapping = "crs" ;
        float sea_surface_wave_directional_spread(time, wave_frequency) ;
                sea_surface_wave_directional_spread:long_name = "wave directional spread in each frequency band" ;
                sea_surface_wave_directional_spread:standard_name = "sea_surface_wave_directional_spread" ;
                sea_surface_wave_directional_spread:units = "degree" ;
                sea_surface_wave_directional_spread:coordinates = "longitude latitude" ;
                sea_surface_wave_directional_spread:grid_mapping = "crs" ;
        float sea_surface_wave_mean_from_direction(time, wave_frequency) ;
                sea_surface_wave_mean_from_direction:long_name = "mean wave direction in each frequency band" ;
                sea_surface_wave_mean_from_direction:standard_name = "sea_surface_wave_mean_from_direction" ;
                sea_surface_wave_mean_from_direction:units = "degree" ;
                sea_surface_wave_mean_from_direction:coordinates = "longitude latitude" ;
                sea_surface_wave_mean_from_direction:grid_mapping = "crs" ;
        ubyte measurement_quality(time) ;
                measurement_quality:long_name = "measurement quality (0: good, 1: bad)" ;
                measurement_quality:flag_meanings = "good bad" ;
                measurement_quality:flag_values = 0UB, 1UB ;
                measurement_quality:coordinates = "longitude latitude" ;
                measurement_quality:grid_mapping = "crs" ;

// global attributes:
                :title = "Marine X-band radar derived wave energy density frequency spectra, directional spread, and mean direction with quality control flag from R/V Ocean Research" ;
                :summary = "The wave energy spectral density, directional spread, and mean direction as function of frequency data are derived from the mean two dimensional wavenumber wave energy density spectrum using the linear wave dispersion relation." ;
                :creator_email = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :history = "20250115T120500Z: File creation time" ;
                :processing_level = "L2b" ;

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
        mtf_exponent = -1.2 ;
  } // group wave_calibration
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
