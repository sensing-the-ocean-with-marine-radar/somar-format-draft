---
title: Bathymetric maps
layout: default
parent: Gridded data
nav_order: 4
---

# Bathymetric maps

Bathymetric maps provide sea floor depth (`sea_floor_depth_below_sea_surface`) at a set of analysis locations along the platform trajectory, together with a standard error and a `measurement_quality` bit flag.
As for the [near-surface current maps](current_maps.md), each depth is retrieved through a least-squares fit that minimizes the distance between the wave signal found in a wavenumber-frequency spectrum, computed from a radar backscatter intensity image sequence within a local circular analysis window, and the ocean wave dispersion relation; here, however, the fit solves for water depth rather than current velocity, exploiting the depth-induced deviation from the deep-water dispersion relationship. Because this deviation only becomes detectable once the water depth is a small enough fraction of the dominant ocean wavelength, X-band radar bathymetry retrievals are limited to waters shallower than approximately 30% of the underlying ocean wavelength; `mean_wavenumber` reports the actual mean wavenumber of the wave signal used for a given measurement.
As for the current maps, analysis locations are stored as points indexed by a flat `measurement` dimension rather than as coordinates on a regular `x`/`y` grid, since the underlying analysis windows are placed on an overlapping, approximately (but not exactly) regular grid that follows the platform trajectory.

## Minimal example
```
netcdf or_2025-01-15-12_bathymetry {
dimensions:
        measurement = 1 ;
variables:
        char trajectory ;
                trajectory:cf_role = "trajectory_id" ;
                trajectory:long_name = "Bathymetry measurements along R/V Ocean Research trajectory" ;
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:authority_string = "EPSG:4326" ;
        double time(measurement) ;
                time:calendar = "standard" ;
                time:long_name = "start time of bathymetry measurement" ;
                time:standard_name = "time" ;
                time:units = "days since 2025-01-01T00:00:00Z" ;
        double longitude(measurement) ;
                longitude:long_name = "center longitude of bathymetry measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
                longitude:grid_mapping = "crs" ;
        double latitude(measurement) ;
                latitude:long_name = "center latitude of bathymetry measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
                latitude:grid_mapping = "crs" ;
        double sea_floor_depth_below_sea_surface(measurement) ;
                sea_floor_depth_below_sea_surface:long_name = "distance between sea surface and sea floor" ;
                sea_floor_depth_below_sea_surface:standard_name = "sea_floor_depth_below_sea_surface" ;
                sea_floor_depth_below_sea_surface:units = "m" ;
        double mean_wavenumber(measurement) ;
                mean_wavenumber:long_name = "mean wavenumber of the wave signal used by the bathymetry measurement" ;
                mean_wavenumber:units = "radian m-1" ;
        double sea_floor_depth_below_sea_surface_standard_error(measurement) ;
                sea_floor_depth_below_sea_surface_standard_error:long_name = "standard error of the bathymetry measurement" ;
                sea_floor_depth_below_sea_surface_standard_error:units = "m s-1" ;
        int64 number_of_wave_coordinates(measurement) ;
                number_of_wave_coordinates:long_name = "number of wave coordinates used by the bathmetry measurement" ;
                number_of_wave_coordinates:units = "1" ;
        ubyte measurement_quality(measurement) ;
                measurement_quality:long_name = "measurement quality (0: good, 1-127: bad)" ;
                measurement_quality:flag_meanings = "good_quality measurement_failed standard_error_above_threshold bathymetry_fit_boundaries_reached number_of_spatial_neighbors_below_threshold number_of_temporal_neighbors_below_threshold difference_from_all_temporal_neighbors_exceeds_threshold measurement_outside_area_of_validity" ;
                measurement_quality:valid_range = 0UB, 127UB ;
                measurement_quality:flag_values = 0UB, 1UB, 2UB, 4UB, 8UB, 16UB, 32UB, 64UB ;
                measurement_quality:standard_name = "quality_flag" ;

// global attributes:
                :title = "Marine X-band radar bathymetry measurements with quality control flag from R/V Ocean Research" ;
                :comment = "The bathymetry measurements are obtained through least-squares fits that minimize the distance between the wave signal found in marine X-band radar backscatter intensity wavenumber frequency spectra and the linear ocean wave dispersion shell. Here, the spectra are based on 12.0 min long radar backscatter intensity image sequences that are partitioned into analysis windows where all pixels outside of the circles that are inscribed in the analysis windows are set to zero. The resulting bathymetry maps have a fixed latitude spacing and a longitude spacing that is updated within 1-degree latitude bands to ensure an approximately constant grid resolution. The spatial overlap between neighboring analysis windows is 50.0% and the temporal overlap between consecutive analysis periods is 25.0%. Analysis windows with a spatiotemporal data coverage of <90.0% are disregarded. Segments of the radar field of view that are obstructed by platform superstructures are also disregarded. X-band radar bathymetry measurements are limited to waters that are shallower than ~30% of the underlying ocean wavelengths, which is where they sufficiently depart from the deep water dispersion relationship." ;
                :contact = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13 SOMaR-0.3-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :featureType = "trajectory" ;
}
```