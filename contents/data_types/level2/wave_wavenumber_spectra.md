---
title: Surface wave two-dimensional wavenumber spectra (L2a)
layout: default
parent: Level 2 data
nav_order: 6
---

# L2a: Surface wave two-dimensional wavenumber spectra

Two-dimensional wavenumber spectra give the (time-averaged) wave energy density, `sea_surface_wave_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber)`, as a function of the two horizontal wavenumber components for each analysis window.
They are retrieved from the same dispersion-relation-based wavenumber-frequency analysis of local circular radar image analysis windows used for the [near-surface current retrieval](current_maps.md).
Following oceanographic convention, the wavenumber vectors point in the direction from which the waves are propagating.
Wavenumbers are cyclic, i.e. the reciprocal of the wavelength, in `m-1`.
The spectrum carries no `standard_name`: CF defines `sea_surface_wave_variance_spectral_density` for frequency spectra, in units of `m2 s`, to which the units of a wavenumber spectrum, `m4`, cannot be converted.
The Level 2b [two-dimensional frequency spectra](wave_frequency_direction_spectra.md), [one-dimensional frequency spectra](wave_frequency_spectra.md), and [peak and mean wave parameters](wave_parameters.md) are derived from these spectra.
Because the wave energy density is calibrated against a reference wave data set, files also carry a `sea_surface_wave_significant_height_calibration_status` global attribute documenting the calibration source and date.
The `longitude` and `latitude` of each measurement give the mean position of the analysis windows that contribute to it (see [Georeferencing](../../metadata_attributes/georeferencing.md#positions-of-analysis-windows)); the radar position itself may optionally be stored in `radar_longitude` and `radar_latitude`.

## Variables

The file holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Coordinate reference system (see [Georeferencing](../../metadata_attributes/georeferencing.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Start time of wave measurement. |
| `eastward_wave_wavenumber`<br><small>SOMaR</small> | double `(eastward_wave_wavenumber)`; `m-1` | Eastward component of the wave wavenumber. |
| `northward_wave_wavenumber`<br><small>SOMaR</small> | double `(northward_wave_wavenumber)`; `m-1` | Northward component of the wave wavenumber. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_east` | Mean longitude of wave measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_north` | Mean latitude of wave measurement. |
| `sea_surface_wave_variance_spectral_density`<br><small>SOMaR</small> | double `(time, northward_wave_wavenumber, eastward_wave_wavenumber)`; `m4` | Wave energy density two dimensional wavenumber spectrum. |
| `measurement_quality`<br><small>SOMaR</small> | ubyte `(time)`; `0` or `1` | Quality flag: 0 is good, 1 is bad. |
{: .variable-table }

In addition to the [shared global attributes](../../metadata_attributes/index.md), the file carries the following global attribute.

| Attribute | Values | Description |
|---|---|---|
| `sea_surface_wave_significant_height_calibration_status`<br><small>SOMaR</small> | String; free text | The reference wave data and the date against which the wave energy density was calibrated. |
{: .attribute-table }

## Minimal example
```
netcdf or_2025-01-15-11_wavenumber_spectra_average {
dimensions:
        time = 29 ;
        northward_wave_wavenumber = 512 ;
        eastward_wave_wavenumber = 512 ;
variables:
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:authority_string = "EPSG:4326" ;
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
        double sea_surface_wave_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber) ;
                sea_surface_wave_variance_spectral_density:long_name = "wave energy density two dimensional wavenumber spectrum" ;
                sea_surface_wave_variance_spectral_density:units = "m4" ;
                sea_surface_wave_variance_spectral_density:coordinates = "longitude latitude" ;
                sea_surface_wave_variance_spectral_density:grid_mapping = "crs" ;
        ubyte measurement_quality(time) ;
                measurement_quality:long_name = "measurement quality (0: good, 1: bad)" ;
                measurement_quality:flag_meanings = "good bad" ;
                measurement_quality:flag_values = 0UB, 1UB ;
                measurement_quality:coordinates = "longitude latitude" ;
                measurement_quality:grid_mapping = "crs" ;

// global attributes:
                :sea_surface_wave_significant_height_calibration_status = "Calibrated on 2025/01/06 using MFWAM global wave data as reference" ;
                :title = "Marine X-band radar derived wave energy density 2D wavenumber spectra with quality control flag from R/V Ocean Research" ;
                :summary = "The wave retrieval is based on 4.0 min long marine X-band radar image sequences that are partitioned into 6 analysis windows of 512 by 512 pixels. Pixels outside the circles inscribed within each analysis window are set to zero prior to processing. The analysis windows are spread across the radar field of view, geostationary, and placed at a range with maximum data coverage. The radar image sequences within each analysis window are transformed to wavenumber frequency space, dispersion filtered, integrated over frequency, multiplied with an empirical modulation transfer function, and rescaled using radar specific calibration parameters to obtain a two dimensional wavenumber wave energy density spectrum. Here, the mean two dimensional wavenumber wave energy density spectra are given. The wavenumber vectors point in the direction from which the waves are propagating." ;
                :creator_email = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :history = "20250115T120500Z: File creation time" ;
                :processing_level = "L2a" ;
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
