---
title: Surface wave two-dimensional wavenumber spectra
layout: default
parent: Trajectory data
nav_order: 1
---

# Surface wave two-dimensional wavenumber spectra

Two-dimensional wavenumber spectra give the (time-averaged) wave energy density, `sea_surface_wave_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber)`, as a function of the two horizontal wavenumber components for each analysis window.
They are retrieved from the same dispersion-relation-based wavenumber-frequency analysis of local circular radar image analysis windows used for the [near-surface current retrieval](../gridded/current_maps.md).
Following oceanographic convention, the wavenumber vectors point in the direction from which the waves are propagating.
The [one-dimensional frequency spectra](wave_frequency_spectra.md) and the [peak and mean wave parameters](wave_parameters.md) are derived from these spectra.
Because the wave energy density is calibrated against a reference wave data set, files also carry a `sea_surface_wave_significant_height_calibration_status` global attribute documenting the calibration source and date.

## Minimal example
```
netcdf or_2025-01-15-11_wavenumber_spectra_average {
dimensions:
        time = 29 ;
        northward_wave_wavenumber = 512 ;
        eastward_wave_wavenumber = 512 ;
variables:
        char trajectory ;
                trajectory:cf_role = "trajectory_id" ;
                trajectory:long_name = "Wave measurements along R/V Ocean Research trajectory" ;
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:authority_string = "EPSG:4326" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of wave measurement" ;
                time:standard_name = "time" ;
                time:units = "days since 2025-01-01T00:00:00Z" ;
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
                longitude:grid_mapping = "crs" ;
        double latitude(time) ;
                latitude:long_name = "mean latitude of wave measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
                latitude:grid_mapping = "crs" ;
        double sea_surface_wave_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber) ;
                sea_surface_wave_variance_spectral_density:long_name = "wave energy density two dimensional wavenumber spectrum" ;
                sea_surface_wave_variance_spectral_density:standard_name = "sea_surface_wave_variance_spectral_density" ;
                sea_surface_wave_variance_spectral_density:units = "m3" ;
        ubyte measurement_quality(time) ;
                measurement_quality:long_name = "measurement quality (0: good, 1: bad)" ;
                measurement_quality:flag_meanings = "good bad" ;
                measurement_quality:flag_values = 0UB, 1UB ;

// global attributes:
                :sea_surface_wave_significant_height_calibration_status = "Calibrated on 2025/01/06 using MFWAM global wave data as reference" ;
                :title = "Marine X-band radar derived wave energy density 2D wavenumber spectra with quality control flag from R/V Ocean Research" ;
                :comment = "The wave retrieval is based on 4.0 min long marine X-band radar image sequences that are partitioned into 512 by 512 pixel analysis windows where all pixels outside of the circles that are inscribed in the analysis windows are set to zero. The analysis windows are spread across the radar field of view, geostationary, and placed at a range with maximum data coverage. The radar image sequences within each analysis window are transformed to wavenumber frequency space, dispersion filtered, integrated over frequency, multiplied with an empirical modulation transfer function, and rescaled using radar specific calibration parameters to obtain a two dimensional wavenumber wave energy density spectrum. Here, the mean two dimensional wavenumber wave energy density spectra are given. The wavenumber vectors point in the direction from which the waves are propagating." ;
                :contact = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13 SOMaR-0.3-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :featureType = "trajectory" ;
}
```
