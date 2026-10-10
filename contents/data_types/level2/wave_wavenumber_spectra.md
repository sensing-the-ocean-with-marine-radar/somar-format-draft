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
The wave energy density is calibrated against a reference wave data set; the parameters of this calibration are recorded in the `wave_calibration` group (see [Calibration](#calibration)).
The `longitude` and `latitude` of each measurement give the mean position of the analysis windows that contribute to it (see [Georeferencing](../../metadata_attributes/georeferencing.md#positions-of-analysis-windows)); the radar position itself may optionally be stored in `radar_longitude` and `radar_latitude`.

## Variables

The file holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Coordinate reference system (see [Georeferencing](../../metadata_attributes/georeferencing.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Start time of each measurement. |
| `eastward_wave_wavenumber`<br><small>SOMaR</small> | double `(eastward_wave_wavenumber)`; `m-1` | Eastward wavenumber component, pointing in the direction the waves come from. |
| `northward_wave_wavenumber`<br><small>SOMaR</small> | double `(northward_wave_wavenumber)`; `m-1` | Northward wavenumber component, pointing in the direction the waves come from. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_east` | Mean longitude of the analysis windows contributing to each measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time)`; `degrees_north` | Mean latitude of the analysis windows contributing to each measurement. |
| `sea_surface_wave_variance_spectral_density`<br><small>SOMaR</small> | double `(time, northward_wave_wavenumber, eastward_wave_wavenumber)`; `m4` | Wave energy density as a function of the two wavenumber components. |
| `measurement_quality`<br><small>SOMaR</small> | ubyte `(time)`; `0` or `1` | Quality flag: 0 is good, 1 is bad. |
{: .variable-table }

## Calibration

Two steps of the wave retrieval rely on empirical parameters, which differ between processors. They are recorded in a group named `wave_calibration` in the root group, so that the calibration can be reproduced from the file.

- The **modulation transfer function** M(k) converts the radar image spectrum into the uncalibrated wave energy density spectrum, which is the image spectrum divided by the squared magnitude of M(k). For the form `"power_law"`, that squared magnitude is proportional to k^β, where k is the wavenumber and β is given by `mtf_exponent`; a positive β thus reduces the energy at high wavenumbers.
- The **significant wave height calibration** converts the signal-to-noise ratio, i.e. the ratio of the `wave_signal` to the `background_noise` reported with the [wave parameters](wave_parameters.md), into the significant wave height: Hs = `hs_intercept` + `hs_slope` × P, where the predictor P named by `hs_predictor` is typically the square root of the signal-to-noise ratio.

| Variable | Values | Description |
|---|---|---|
| `hs_intercept`<br><small>SOMaR</small> | double; `m` | Intercept of the significant wave height calibration. |
| `hs_slope`<br><small>SOMaR</small> | double; `m` | Slope of the significant wave height calibration. |
| `hs_predictor`<br><small>SOMaR</small> | string; `"sqrt_signal_to_noise_ratio"`, `"signal_to_noise_ratio"`, or `"other"` | The quantity to which the slope and intercept are applied. |
| `mtf_form`<br><small>SOMaR</small> | string; `"power_law"`, `"none"`, or `"other"` | The form of the modulation transfer function. |
| `mtf_exponent`<br><small>SOMaR</small> | double; dimensionless | For `"power_law"`: the exponent β. Omitted otherwise. |
{: .variable-table }

A processor that uses a different predictor or a different form of the modulation transfer function sets the variable to `"other"` and describes its method in a `comment` attribute of that variable; a `references` attribute gives the publication.

The group carries the following attributes.

| Attribute | Values | Description |
|---|---|---|
| `calibration_reference`<br><small>SOMaR</small> | String; free text | The reference wave data against which the calibration was derived. |
| `calibration_date`<br><small>SOMaR</small> | String; ISO 8601 date | The date of the calibration. |
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
                :title = "Marine X-band radar derived wave energy density 2D wavenumber spectra with quality control flag from R/V Ocean Research" ;
                :summary = "The wave retrieval is based on 4.0 min long marine X-band radar image sequences that are partitioned into 6 analysis windows of 512 by 512 pixels. Pixels outside the circles inscribed within each analysis window are set to zero prior to processing. The analysis windows are spread across the radar field of view, geostationary, and placed at a range with maximum data coverage. The radar image sequences within each analysis window are transformed to wavenumber frequency space, dispersion filtered, integrated over frequency, multiplied with an empirical modulation transfer function, and rescaled using radar specific calibration parameters to obtain a two dimensional wavenumber wave energy density spectrum. Here, the mean two dimensional wavenumber wave energy density spectra are given. The wavenumber vectors point in the direction from which the waves are propagating." ;
                :creator_email = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :history = "20250115T120500Z: File creation time" ;
                :processing_level = "L2a" ;

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
