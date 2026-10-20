---
title: Surface wave two-dimensional wavenumber spectra (L2a)
layout: default
parent: Level 2 products
grand_parent: SOMaR product types
nav_order: 7
---

# L2a: Surface wave two-dimensional wavenumber spectra

Two-dimensional wavenumber spectra (`wave_wavenumber_spectra`) give the (time-averaged) wave energy density, `sea_surface_wave_wavenumber_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber)`, as a function of the two horizontal wavenumber components for each measurement, averaged over the analysis windows that contribute to it.
They are retrieved from the wavenumber-frequency spectra of local radar image analysis windows, as used for the [near-surface current retrieval](current_maps.md), by keeping the wave signal that follows the dispersion relation (Young et al. [1985](../../references/index.md#young-1985)).
By SOMaR convention, consistent with the from-direction used by the frequency-direction spectra, the wavenumber vectors point toward the direction from which the waves come, i.e. opposite to the direction of propagation.
Wavenumbers are cyclic, i.e. the reciprocal of the wavelength, in `m-1`.
The spectrum carries no `standard_name`: CF defines `sea_surface_wave_variance_spectral_density` for frequency spectra, in units of `m2 s`, to which the units of a wavenumber spectrum, `m4`, cannot be converted; the variable name, `sea_surface_wave_wavenumber_variance_spectral_density`, is chosen so as not to be mistaken for that standard name.
The Level 2b [frequency-direction spectra](wave_frequency_direction_spectra.md), [one-dimensional frequency spectra](wave_frequency_spectra.md), and [peak and mean wave parameters](wave_parameters.md) are derived from these spectra.
The wave energy density is calibrated, typically against a reference wave data set; the parameters of this calibration are recorded in the `wave_calibration` group (see [Wave calibration parameters](../../metadata_attributes/wave_calibration.md)).
The quantities from which the calibration derives the significant wave height may be stored as for the [wave parameters](wave_parameters.md): `wave_signal` and `background_noise` for the signal-to-noise ratio method, or `sea_surface_wave_mean_square_slope` for the shadowing method.
The analysis windows and the processing parameters are described under [Wave products](index.md#wave-products) and [Processing parameters](index.md#processing-parameters).
The `longitude` and `latitude` of each measurement give the mean position of the analysis windows that contribute to it (see [Georeferencing](../../georeferencing/index.md#positions-of-analysis-windows)); the radar position itself may optionally be stored in `radar_longitude` and `radar_latitude`.

## Variables

The file holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required. Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each measurement. |
| `eastward_wave_wavenumber`<br><small>SOMaR</small> | double `(eastward_wave_wavenumber)`; `m-1` | Required. Eastward wavenumber component, pointing in the direction the waves come from. |
| `northward_wave_wavenumber`<br><small>SOMaR</small> | double `(northward_wave_wavenumber)`; `m-1` | Required. Northward wavenumber component, pointing in the direction the waves come from. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_east` | Required. Mean longitude of the analysis windows contributing to each measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_north` | Required. Mean latitude of the analysis windows contributing to each measurement. |
| `sea_surface_wave_wavenumber_variance_spectral_density`<br><small>SOMaR</small> | double `(time, northward_wave_wavenumber, eastward_wave_wavenumber)`; `m4` | Required. Wave energy density as a function of the two wavenumber components. |
| `wave_signal`<br><small>SOMaR</small> | double `(time)`; `1` | Optional. Spectral density of the wave signal in the radar images, used by the signal-to-noise ratio method to derive the significant wave height. |
| `background_noise`<br><small>SOMaR</small> | double `(time)`; `1` | Optional. Spectral density of the background noise in the radar images, used by the signal-to-noise ratio method to derive the significant wave height. |
| `sea_surface_wave_mean_square_slope`<br><small>[CF][cf-names]</small> | double `(time)`; `1` | Optional. Mean square slope of the sea surface, used by the shadowing method to derive the significant wave height. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(time)`; bit flags | Required. Quality flag. 0 is good; each bit that is set marks a failed check (see [Quality flags](index.md#quality-flags)). |
{: .variable-table }


## Minimal example
```
netcdf or_2025-01-15-11_wave_wavenumber_spectra {
dimensions:
        time = 29 ;
        northward_wave_wavenumber = 512 ;
        eastward_wave_wavenumber = 512 ;
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
                sea_surface_wave_wavenumber_variance_spectral_density:coordinates = "longitude latitude" ;
                sea_surface_wave_wavenumber_variance_spectral_density:grid_mapping = "crs" ;
                sea_surface_wave_wavenumber_variance_spectral_density:ancillary_variables = "measurement_quality" ;
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
                measurement_quality:long_name = "measurement quality (0: good, 1-63: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold wave_steepness_above_threshold invalid_peak number_of_temporal_neighbors_below_threshold rain_contamination" ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB ;
                measurement_quality:valid_range = 0UB, 63UB ;
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
                :product_type = "wave_wavenumber_spectra" ;
                :time_coverage_end = "2025-01-15T11:59:59Z" ;
                :time_coverage_start = "2025-01-15T11:00:00Z" ;
                :title = "Marine X-band radar surface wave two-dimensional wavenumber spectra from R/V Ocean Research" ;
                :analysis_window_size = 3840. ;
                :number_of_analysis_windows = 6 ;
                :measurement_duration = 240. ;
                :number_of_images = 160 ;

group: wave_calibration { ... } // as in the example under Wave calibration parameters
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
