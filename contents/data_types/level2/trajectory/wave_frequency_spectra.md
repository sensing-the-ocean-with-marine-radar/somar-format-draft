---
title: Surface wave one-dimensional frequency spectra
layout: default
parent: Trajectory data
nav_order: 2
---

# Surface wave one-dimensional frequency spectra

One-dimensional frequency spectra give the (time-averaged) wave energy density, `sea_surface_wave_variance_spectral_density(time, wave_frequency)`, for each analysis window, together with the directional spread (`sea_surface_wave_directional_spread`) and mean wave direction (`sea_surface_wave_mean_from_direction`) in each frequency band.
They are derived from the [two-dimensional wavenumber spectra](wave_wavenumber_spectra.md) using the linear wave dispersion relation, which relates each wavenumber to its corresponding wave frequency.
As for the wavenumber spectra, files carry a `sea_surface_wave_significant_height_calibration_status` global attribute documenting the calibration source and date.

## Minimal example
```
netcdf or_2025-01-15-11_wave_spectrograms_average {
dimensions:
        time = 29 ;
        wave_frequency = 512 ;
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
        double wave_frequency(wave_frequency) ;
                wave_frequency:long_name = "wave frequency" ;
                wave_frequency:standard_name = "wave_frequency" ;
                wave_frequency:units = "s-1" ;
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
        float sea_surface_wave_variance_spectral_density(time, wave_frequency) ;
                sea_surface_wave_variance_spectral_density:long_name = "wave energy density frequency spectrum" ;
                sea_surface_wave_variance_spectral_density:standard_name = "sea_surface_wave_variance_spectral_density" ;
                sea_surface_wave_variance_spectral_density:units = "m2 s" ;
        float sea_surface_wave_directional_spread(time, wave_frequency) ;
                sea_surface_wave_directional_spread:long_name = "wave directional spread in each frequency band" ;
                sea_surface_wave_directional_spread:standard_name = "sea_surface_wave_directional_spread" ;
                sea_surface_wave_directional_spread:units = "degree" ;
        float sea_surface_wave_mean_from_direction(time, wave_frequency) ;
                sea_surface_wave_mean_from_direction:long_name = "mean wave direction in each frequency band" ;
                sea_surface_wave_mean_from_direction:standard_name = "sea_surface_wave_mean_from_direction" ;
                sea_surface_wave_mean_from_direction:units = "degree" ;
        ubyte measurement_quality(time) ;
                measurement_quality:long_name = "measurement quality (0: good, 1: bad)" ;
                measurement_quality:flag_meanings = "good bad" ;
                measurement_quality:flag_values = 0UB, 1UB ;

// global attributes:
                :sea_surface_wave_significant_height_calibration_status = "Calibrated on 2025/01/06 using MFWAM global wave data as reference" ;
                :title = "Marine X-band radar derived wave energy density frequency spectra, directional spread, and mean direction with quality control flag from R/V Ocean Research" ;
                :comment = "The wave energy spectral density, directional spread, and mean direction as function of frequency data are derived from the mean two dimensional wavenumber wave energy density spectrum using the linear wave dispersion relation." ;
                :contact = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13 SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :featureType = "trajectory" ;
}
```
