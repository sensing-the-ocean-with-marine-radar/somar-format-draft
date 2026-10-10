---
title: Surface wave two-dimensional frequency spectra (L2b)
layout: default
parent: Level 2 data
nav_order: 7
---

# L2b: Surface wave two-dimensional frequency spectra

Two-dimensional frequency spectra give the (time-averaged) wave energy density, `sea_surface_wave_directional_variance_spectral_density(time, wave_frequency, sea_surface_wave_from_direction)`, as a function of wave frequency and wave direction for each analysis window.
They are derived from the [two-dimensional wavenumber spectra](wave_wavenumber_spectra.md) using the linear wave dispersion relation, which relates each wavenumber to its corresponding wave frequency.
Following oceanographic convention, the wave direction is the direction from which the waves are propagating.
Integrating over direction yields the [one-dimensional frequency spectra](wave_frequency_spectra.md).
The calibration parameters of the wave retrieval are recorded in the `wave_calibration` group (see [Calibration](wave_wavenumber_spectra.md#calibration)).
The `longitude` and `latitude` of each measurement give the mean position of the analysis windows that contribute to it (see [Georeferencing](../../metadata_attributes/georeferencing.md#positions-of-analysis-windows)); the radar position itself may optionally be stored in `radar_longitude` and `radar_latitude`.

## Variables

The file holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Coordinate reference system (see [Georeferencing](../../metadata_attributes/georeferencing.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Start time of each measurement. |
| `wave_frequency`<br><small>[CF][cf-names]</small> | double `(wave_frequency)`; `s-1` | Wave frequency. |
| `sea_surface_wave_from_direction`<br><small>[CF][cf-names]</small> | double `(sea_surface_wave_from_direction)`; `degree` | Direction the waves come from. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_east` | Mean longitude of the analysis windows contributing to each measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_north` | Mean latitude of the analysis windows contributing to each measurement. |
| `sea_surface_wave_directional_variance_spectral_density`<br><small>[CF][cf-names]</small> | double `(time, wave_frequency, sea_surface_wave_from_direction)`; `m2 s degree-1` | Wave energy density as a function of frequency and direction. |
| `measurement_quality`<br><small>SOMaR</small> | ubyte `(time)`; `0` or `1` | Quality flag: 0 is good, 1 is bad. |
{: .variable-table }

## Minimal example

The example below is illustrative; it is not yet based on an existing NetCDF file.

```
netcdf or_2025-01-15-11_frequency_direction_spectra_average {
dimensions:
        time = 29 ;
        wave_frequency = 512 ;
        sea_surface_wave_from_direction = 360 ;
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
        double sea_surface_wave_from_direction(sea_surface_wave_from_direction) ;
                sea_surface_wave_from_direction:long_name = "direction from which the waves are propagating" ;
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
                sea_surface_wave_directional_variance_spectral_density:coordinates = "longitude latitude" ;
                sea_surface_wave_directional_variance_spectral_density:grid_mapping = "crs" ;
        ubyte measurement_quality(time) ;
                measurement_quality:long_name = "measurement quality (0: good, 1: bad)" ;
                measurement_quality:flag_meanings = "good bad" ;
                measurement_quality:flag_values = 0UB, 1UB ;
                measurement_quality:coordinates = "longitude latitude" ;
                measurement_quality:grid_mapping = "crs" ;

// global attributes:
                :title = "Marine X-band radar derived wave energy density 2D frequency spectra with quality control flag from R/V Ocean Research" ;
                :summary = "The two dimensional frequency wave energy density spectra are derived from the mean two dimensional wavenumber wave energy density spectrum using the linear wave dispersion relation. The wave direction is the direction from which the waves are propagating." ;
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
