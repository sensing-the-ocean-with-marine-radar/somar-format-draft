---
title: Surface wave spectra and parameters
layout: default
parent: Trajectory data
nav_order: 1
---

# Surface wave spectra and parameters

Surface wave products describe the sea state along the platform trajectory, retrieved from a dispersion-relation-based wavenumber-frequency analysis of local circular radar image analysis windows.
They come as wave energy density spectra, which resolve the wave field across wavenumber, frequency, and direction, and as peak and mean wave parameters, which condense each spectrum into standard bulk quantities such as significant wave height and peak wave period.
All surface wave files carry one value or spectrum per analysis window, with `time`, `longitude`, and `latitude` coordinates and a `measurement_quality` flag.

## Surface wave energy density spectra

Surface wave energy density spectra describe the distribution of wave energy across wavenumber, frequency, and/or direction, retrieved from the same dispersion-relation-based wavenumber-frequency analysis of local circular radar image analysis windows used for the [near-surface current retrieval](../gridded/current_maps.md).
SOMaR provides two complementary representations of the (time-averaged) wave energy spectrum for each analysis window:

1. The two-dimensional wavenumber spectrum, `sea_surface_wave_variance_spectral_density(time, northward_wave_wavenumber, eastward_wave_wavenumber)`, giving the wave energy density as a function of the two horizontal wavenumber components. Following oceanographic convention, the wavenumber vectors point in the direction from which the waves are propagating.
2. The one-dimensional frequency spectrogram, `sea_surface_wave_variance_spectral_density(time, wave_frequency)`, together with the directional spread (`sea_surface_wave_directional_spread`) and mean wave direction (`sea_surface_wave_mean_from_direction`) in each frequency band, all derived from the two-dimensional wavenumber spectrum.

Because the wave energy density is calibrated against a reference wave data set, files also carry a `sea_surface_wave_significant_height_calibration_status` global attribute documenting the calibration source and date.

### Minimal example: two-dimensional wavenumber spectrum
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

### Minimal example: one-dimensional frequency spectrogram
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
                :comment = "The wave energy spectral density, directional spread, and mean direction as function of frequency data are derived from the mean two dimensional wavenumber wave energy density spectrum described for the wavenumber spectra above." ;
                :contact = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13 SOMaR-0.3-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :featureType = "trajectory" ;
}
```

## Peak and mean wave parameters

Peak and mean wave parameters summarize each wave energy density spectrum above using standard bulk wave parameters: significant wave height (`sea_surface_wave_significant_height`), the peak wave period and peak wave direction (period and direction at the spectral maximum), and the mean wave period.
To aid interpretation and quality assessment, the wave-signal and background-noise spectral densities used to derive the significant wave height are also reported (`wave_signal`, `background_noise`), together with the near-surface current vector obtained from the same analysis window (see [Near-surface current maps](../gridded/current_maps.md)) and a `measurement_quality` flag.
As for the wave spectra, a `sea_surface_wave_significant_height_calibration_status` global attribute documents the calibration source and date against which the significant wave height retrieval was calibrated.

### Minimal example
```
netcdf or_2025-01-15-11_wave_parameters_average {
dimensions:
        time = 29 ;
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
        double eastward_sea_water_velocity(time) ;
                eastward_sea_water_velocity:long_name = "eastward component of the near surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
        double northward_sea_water_velocity(time) ;
                northward_sea_water_velocity:long_name = "northward component of the near surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
        double sea_surface_wave_significant_height(time) ;
                sea_surface_wave_significant_height:long_name = "significant wave height" ;
                sea_surface_wave_significant_height:standard_name = "sea_surface_wave_significant_height" ;
                sea_surface_wave_significant_height:units = "m" ;
        double sea_surface_wave_from_direction_at_variance_spectral_density_maximum(time) ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:long_name = "peak wave direction" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_from_direction_at_variance_spectral_density_maximum" ;
                sea_surface_wave_from_direction_at_variance_spectral_density_maximum:units = "degree" ;
        double sea_surface_wave_period_at_variance_spectral_density_maximum(time) ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:long_name = "peak wave period" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:standard_name = "sea_surface_wave_period_at_variance_spectral_density_maximum" ;
                sea_surface_wave_period_at_variance_spectral_density_maximum:units = "s" ;
        double sea_surface_wave_mean_period(time) ;
                sea_surface_wave_mean_period:long_name = "mean wave period" ;
                sea_surface_wave_mean_period:standard_name = "sea_surface_wave_mean_period" ;
                sea_surface_wave_mean_period:units = "s" ;
        double wave_signal(time) ;
                wave_signal:long_name = "radar image spectral density of the wave signal" ;
                wave_signal:units = "1" ;
        double background_noise(time) ;
                background_noise:long_name = "radar image spectral density of the background noise" ;
                background_noise:units = "1" ;
        ubyte measurement_quality(time) ;
                measurement_quality:long_name = "measurement quality (0: good, 1: bad)" ;
                measurement_quality:flag_meanings = "good bad" ;
                measurement_quality:flag_values = 0UB, 1UB ;

// global attributes:
                :sea_surface_wave_significant_height_calibration_status = "Calibrated on 2025/01/06 using MFWAM global wave data as reference" ;
                :title = "Marine X-band radar derived mean and peak wave parameters with quality control flag from R/V Ocean Research" ;
                :comment = "The mean and peak wave parameters are derived from the mean two dimensional wavenumber wave energy density spectrum described for the wave energy density spectra above." ;
                :contact = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13 SOMaR-0.3-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :featureType = "trajectory" ;
}
```