---
title: Surface wave one-dimensional frequency spectra (L2b)
layout: default
parent: Level 2 products
grand_parent: SOMaR product types
nav_order: 8
---

# L2b: Surface wave one-dimensional frequency spectra

One-dimensional frequency spectra (`wave_frequency_spectra`, short `wav_f1d`) give the (time-averaged) wave energy density, `sea_surface_wave_variance_spectral_density(time, wave_frequency)`, for each measurement, averaged over the analysis windows that contribute to it, together with the directional spread (`sea_surface_wave_directional_spread`) and mean wave direction (`sea_surface_wave_mean_from_direction`) in each frequency band.
They are derived from the [two-dimensional wavenumber spectra](wave_wavenumber_spectra.md) using the linear wave dispersion relation, which relates each wavenumber to its corresponding wave frequency.
The calibration parameters of the wave retrieval are recorded in the `wave_calibration` group (see [Wave calibration parameters](../../metadata_attributes/wave_calibration.md)).
The analysis windows and the processing parameters are described under [Wave products](index.md#wave-products) and [Processing parameters](index.md#processing-parameters).
The `longitude` and `latitude` of each measurement give the mean position of the analysis windows that contribute to it (see [Georeferencing](../../georeferencing/index.md#positions-of-analysis-windows)); the radar position itself may optionally be stored in `radar_longitude` and `radar_latitude`.

## Variables

The file holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required. Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each measurement. |
| `wave_frequency`<br><small>[CF][cf-names]</small> | double `(wave_frequency)`; `s-1` | Required. Wave frequency. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_east` | Required. Mean longitude of the analysis windows contributing to each measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_north` | Required. Mean latitude of the analysis windows contributing to each measurement. |
| `sea_surface_wave_variance_spectral_density`<br><small>[CF][cf-names]</small> | float `(time, wave_frequency)`; `m2 s` | Required. Wave energy density as a function of frequency. |
| `sea_surface_wave_directional_spread`<br><small>[CF][cf-names]</small> | float `(time, wave_frequency)`; `degree` | Optional. Directional spread of the waves in each frequency band. |
| `sea_surface_wave_mean_from_direction`<br><small>[CF][cf-names]</small> | float `(time, wave_frequency)`; `degree` | Optional. Mean direction the waves come from in each frequency band. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(time)`; `0` or `1` | Required. Quality flag: 0 is good, 1 is bad. |
{: .variable-table }

## Minimal example
```
netcdf or_2025-01-15-11_wave_frequency_spectra {
dimensions:
        time = 29 ;
        wave_frequency = 512 ;
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
                sea_surface_wave_variance_spectral_density:ancillary_variables = "measurement_quality" ;
        float sea_surface_wave_directional_spread(time, wave_frequency) ;
                sea_surface_wave_directional_spread:long_name = "wave directional spread in each frequency band" ;
                sea_surface_wave_directional_spread:standard_name = "sea_surface_wave_directional_spread" ;
                sea_surface_wave_directional_spread:units = "degree" ;
                sea_surface_wave_directional_spread:coordinates = "longitude latitude" ;
                sea_surface_wave_directional_spread:grid_mapping = "crs" ;
                sea_surface_wave_directional_spread:ancillary_variables = "measurement_quality" ;
        float sea_surface_wave_mean_from_direction(time, wave_frequency) ;
                sea_surface_wave_mean_from_direction:long_name = "mean wave direction in each frequency band" ;
                sea_surface_wave_mean_from_direction:standard_name = "sea_surface_wave_mean_from_direction" ;
                sea_surface_wave_mean_from_direction:units = "degree" ;
                sea_surface_wave_mean_from_direction:coordinates = "longitude latitude" ;
                sea_surface_wave_mean_from_direction:grid_mapping = "crs" ;
                sea_surface_wave_mean_from_direction:ancillary_variables = "measurement_quality" ;
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
                :product_type = "wave_frequency_spectra" ;
                :time_coverage_end = "2025-01-15T11:59:59Z" ;
                :time_coverage_start = "2025-01-15T11:00:00Z" ;
                :title = "Marine X-band radar surface wave one-dimensional frequency spectra from R/V Ocean Research" ;
                :analysis_window_size = 3840. ;
                :number_of_analysis_windows = 6 ;
                :measurement_period_duration = 240. ;
                :number_of_images = 160 ;

group: wave_calibration { ... } // as in the example under Wave calibration parameters
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
