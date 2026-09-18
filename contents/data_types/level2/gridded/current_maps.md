---
title: Near-surface current maps
layout: default
parent: Gridded data
nav_order: 3
---

# Near-surface current maps

Near-surface current maps provide the horizontal near-surface current vector (`eastward_sea_water_velocity`, `northward_sea_water_velocity`) at a set of analysis locations along the platform trajectory, together with per-component standard errors and a `measurement_quality` bit flag.
Each current vector is retrieved through a least-squares fit that minimizes the distance between the wave signal found in a wavenumber-frequency spectrum, computed from a radar backscatter intensity image sequence within a local circular analysis window, and the linear ocean wave dispersion relation, exploiting the current-induced Doppler shift of the surface wave field.
Because the resulting current is a depth-weighted average, with the surface current carrying the greatest weight, the effective sensing depth depends on the wavenumber range of the wave signal used in the fit and can be approximated as 4-8% of the underlying ocean wavelength; `mean_wavenumber` reports the actual mean wavenumber of the wave signal used for a given measurement.
Because the analysis windows are placed on an overlapping, approximately (but not exactly) regular grid that follows the platform trajectory, analysis locations are stored as points indexed by a flat `measurement` dimension rather than as coordinates on a regular `x`/`y` grid, with `longitude` and `latitude` given as measurement-indexed variables.

## Minimal example
```
netcdf or_2025-01-15-11_currents {
dimensions:
        measurement = 4720 ;
variables:
        char trajectory ;
                trajectory:cf_role = "trajectory_id" ;
                trajectory:long_name = "Current measurements along R/V Ocean Research trajectory" ;
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:authority_string = "EPSG:4326" ;
        int64 measurement(measurement) ;
                measurement:long_name = "measurement identifier" ;
                measurement:units = "1" ;
        double time(measurement) ;
                time:calendar = "standard" ;
                time:long_name = "start time of current measurement" ;
                time:standard_name = "time" ;
                time:units = "days since 2025-01-01T00:00:00Z" ;
        double longitude(measurement) ;
                longitude:long_name = "center longitude of current measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
                longitude:grid_mapping = "crs" ;
        double latitude(measurement) ;
                latitude:long_name = "center latitude of current measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
                latitude:grid_mapping = "crs" ;
        double eastward_sea_water_velocity(measurement) ;
                eastward_sea_water_velocity:long_name = "eastward component of the near surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
        double northward_sea_water_velocity(measurement) ;
                northward_sea_water_velocity:long_name = "northward component of the near surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
        double mean_wavenumber(measurement) ;
                mean_wavenumber:long_name = "mean wavenumber of the wave signal used by the current measurement" ;
                mean_wavenumber:units = "radian m-1" ;
        double eastward_sea_water_velocity_standard_error(measurement) ;
                eastward_sea_water_velocity_standard_error:long_name = "standard error of the eastward component of the near surface current velocity" ;
                eastward_sea_water_velocity_standard_error:units = "m s-1" ;
        double northward_sea_water_velocity_standard_error(measurement) ;
                northward_sea_water_velocity_standard_error:long_name = "standard error of the northward component of the near surface current velocity" ;
                northward_sea_water_velocity_standard_error:units = "m s-1" ;
        int64 number_of_wave_coordinates(measurement) ;
                number_of_wave_coordinates:long_name = "number of wave coordinates used by the current measurement" ;
                number_of_wave_coordinates:units = "1" ;
        ubyte measurement_quality(measurement) ;
                measurement_quality:long_name = "measurement quality (0: good, 1-127: bad)" ;
                measurement_quality:flag_meanings = "good_quality measurement_failed standard_error_above_threshold current_fit_boundaries_reached number_of_spatial_neighbors_below_threshold difference_from_all_spatial_neighbors_exceeds_threshold number_of_temporal_neighbors_below_threshold difference_from_all_temporal_neighbors_exceeds_threshold" ;
                measurement_quality:valid_range = 0UB, 127UB ;
                measurement_quality:flag_values = 0UB, 1UB, 2UB, 4UB, 8UB, 16UB, 32UB, 64UB ;
                measurement_quality:standard_name = "quality_flag" ;

// global attributes:
                :title = "Marine X-band radar near-surface current measurements with quality control flag from R/V Ocean Research" ;
                :comment = "The near-surface current vectors are obtained through least-squares fits that minimize the distance between the wave signal found in marine X-band radar backscatter intensity wavenumber frequency spectra and the linear ocean wave dispersion shell. Here, the spectra are based on 12.00 min long radar backscatter intensity image sequences that are partitioned into analysis windows where all pixels outside of the circles that are inscribed in the analysis windows are set to zero. The resulting current maps have a fixed latitude spacing and a longitude spacing that is updated within 1-degree latitude bands to ensure an approximately constant grid resolution. The spatial overlap between neighboring analysis windows is 50.0% and the temporal overlap between consecutive analysis periods is 25.0%. Analysis windows with a spatiotemporal data coverage of <90.0% are disregarded. Segments of the radar field of view that are obstructed by platform superstructures are also disregarded. The effective depth of the radar currents is a weighted mean of the upper ocean with the surface current carrying the greatest weight. It can be approximated as 4-8% of the underlying ocean wavelength depending on the shape of the current profile." ;
                :contact = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13 SOMaR-0.3-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :featureType = "trajectory" ;
}
```

# Near-surface current profile maps

Near-surface current profile maps extend the near-surface current maps above by repeating the same dispersion-relation current fit for a set of distinct wavenumber bands rather than a single fixed wave-signal wavenumber range, providing an approximate vertical profile of near-surface current shear.
Each entry along the `measurement` dimension therefore corresponds to one (analysis location, wavenumber band) pair rather than to one analysis location alone, so the same location appears multiple times, once per wavenumber band for which a fit was attempted.
The lower bound of the wavenumber band used for a given measurement is given by `lower_wavenumber_bin_edge`, with the (fixed) band width given by the global attribute `wavenumber_bin_size`; as in the near-surface current maps, `mean_wavenumber` reports the actual mean wavenumber of the wave signal used in that particular fit, and since the effective sensing depth increases with wavelength, the wavenumber-dependence of the current fits amounts to a measure of upper-ocean vertical current shear.
All other variables (current components, standard errors, `number_of_wave_coordinates`, `measurement_quality`) are defined identically to the near-surface current maps above.

## Minimal example
```
netcdf or_2025-01-15-11_currents_profile {
dimensions:
        measurement = 27384 ;
variables:
        ... // as for near-surface current maps above (trajectory, crs, measurement, time, longitude, latitude,
            // eastward/northward_sea_water_velocity, mean_wavenumber, standard errors,
            // number_of_wave_coordinates, measurement_quality) ...
        double lower_wavenumber_bin_edge(measurement) ;
                lower_wavenumber_bin_edge:long_name = "lower edge of the wavenumber bin used by the current measurement" ;

// global attributes:
                :title = "Marine X-band radar near-surface current measurements with quality control flag from R/V Ocean Research" ;
                :wavenumber_bin_size = 0.0209584500796971 ;
                :comment = "... as for near-surface current maps above; since the effective depth increases with ocean wavelength, we obtain a measure of upper ocean vertical shear by performing current fits as a function of wavenumber." ;
                :contact = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13 SOMaR-0.3-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :featureType = "trajectory" ;
}
```