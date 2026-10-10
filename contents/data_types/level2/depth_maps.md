---
title: Bathymetric maps (L2a)
layout: default
parent: Level 2 data
nav_order: 4
---

# L2a: Bathymetric maps

Bathymetric maps provide sea floor depth (`sea_floor_depth_below_sea_surface`) at a set of analysis locations along the platform trajectory, together with a standard error and a `measurement_quality` bit flag.
As for the [near-surface current maps](current_maps.md), each depth is retrieved through a least-squares fit that minimizes the distance between the wave signal found in a wavenumber-frequency spectrum, computed from a radar backscatter intensity image sequence within a local circular analysis window, and the ocean wave dispersion relation; here, however, the fit solves for water depth rather than current velocity, exploiting the depth-induced deviation from the deep-water dispersion relationship. Because this deviation only becomes detectable once the water depth is a small enough fraction of the dominant ocean wavelength, X-band radar bathymetry retrievals are limited to waters shallower than approximately 30% of the underlying ocean wavelength; `mean_wavenumber` reports the actual mean wavenumber of the wave signal used for a given measurement.
As for the [near-surface current maps](current_maps.md), the analysis windows of one measurement period form a map that spans the radar footprint, and all maps belonging to one file are stored as sibling NetCDF groups, one group per measurement period, named `time_<YYYYMMDDHHMMSS>`. Within each group, the variables are stored on a two-dimensional `(latitude, longitude)` grid, on which the cells in the corners and those of analysis windows without a result hold the `_FillValue`, and the coordinate variables `latitude` and `longitude` give the centers of the analysis windows (see [Georeferencing](../../metadata_attributes/georeferencing.md#positions-of-analysis-windows)); a processor whose analysis windows lie on a local grid uses the [local-grid form](current_maps.md#local-grid-form) instead; the radar position for the period may optionally be stored in the scalar variables `radar_longitude` and `radar_latitude`.

## Variables

Each `time_<YYYYMMDDHHMMSS>` group holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Coordinate reference system (see [Georeferencing](../../metadata_attributes/georeferencing.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double; `seconds since 1970-01-01T00:00:00Z` | Start time of the measurement period. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(longitude)`; `degrees_east` | Longitude of the centers of the analysis windows. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(latitude)`; `degrees_north` | Latitude of the centers of the analysis windows. |
| `sea_floor_depth_below_sea_surface`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m` | Water depth, from the sea surface to the sea floor. |
| `mean_wavenumber`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m-1` | Mean wavenumber of the wave signal used in the fit. |
| `sea_floor_depth_below_sea_surface_standard_error`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m` | Standard error of the water depth. |
| `number_of_wave_coordinates`<br><small>SOMaR</small> | int64 `(latitude, longitude)`; dimensionless | Number of points of the wave signal in the wavenumber-frequency spectrum that were used in the fit. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(latitude, longitude)`; bit flags | Quality flag. 0 is good; each bit that is set marks a failed check (see `flag_meanings` in the example). |
{: .variable-table }

## Minimal example
```
netcdf or_2025-01-15-12_bathymetry {

// global attributes:
                :title = "Marine X-band radar bathymetry measurements with quality control flag from R/V Ocean Research" ;
                :summary = "The bathymetry measurements are obtained through least-squares fits that minimize the distance between the wave signal found in marine X-band radar backscatter intensity wavenumber frequency spectra and the linear ocean wave dispersion shell. Here, the spectra are based on 4.0 min long radar backscatter intensity image sequences that are partitioned into analysis windows. Pixels outside the circles inscribed within each analysis window are set to zero prior to processing. The resulting bathymetry maps have a fixed latitude spacing and a longitude spacing that is updated within 1-degree latitude bands to ensure an approximately constant grid resolution. The spatial overlap between neighboring analysis windows is 50.0% and the temporal overlap between consecutive analysis periods is 25.0%. Analysis windows with a spatiotemporal data coverage of <90.0% are disregarded. Segments of the radar field of view that are obstructed by platform superstructures are also disregarded. X-band radar bathymetry measurements are limited to waters that are shallower than ~30% of the underlying ocean wavelengths, which is where they sufficiently depart from the deep water dispersion relationship." ;
                :creator_email = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :history = "20250115T130500Z: File creation time" ;
                :processing_level = "L2a" ;

group: time_20250115120031 {
  dimensions:
        latitude = 17 ;
        longitude = 17 ;
  variables:
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:authority_string = "EPSG:4326" ;
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of bathymetry measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T12:00:31.417000Z" ;
        double longitude(longitude) ;
                longitude:long_name = "center longitude of bathymetry measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(latitude) ;
                latitude:long_name = "center latitude of bathymetry measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double sea_floor_depth_below_sea_surface(latitude, longitude) ;
                sea_floor_depth_below_sea_surface:long_name = "distance between sea surface and sea floor" ;
                sea_floor_depth_below_sea_surface:standard_name = "sea_floor_depth_below_sea_surface" ;
                sea_floor_depth_below_sea_surface:units = "m" ;
                sea_floor_depth_below_sea_surface:grid_mapping = "crs" ;
                sea_floor_depth_below_sea_surface:_FillValue = NaN ;
        double mean_wavenumber(latitude, longitude) ;
                mean_wavenumber:long_name = "mean wavenumber of the wave signal used by the bathymetry measurement" ;
                mean_wavenumber:units = "m-1" ;
                mean_wavenumber:grid_mapping = "crs" ;
                mean_wavenumber:_FillValue = NaN ;
        double sea_floor_depth_below_sea_surface_standard_error(latitude, longitude) ;
                sea_floor_depth_below_sea_surface_standard_error:long_name = "standard error of the bathymetry measurement" ;
                sea_floor_depth_below_sea_surface_standard_error:units = "m" ;
                sea_floor_depth_below_sea_surface_standard_error:grid_mapping = "crs" ;
                sea_floor_depth_below_sea_surface_standard_error:_FillValue = NaN ;
        int64 number_of_wave_coordinates(latitude, longitude) ;
                number_of_wave_coordinates:long_name = "number of wave coordinates used by the bathymetry measurement" ;
                number_of_wave_coordinates:units = "1" ;
                number_of_wave_coordinates:grid_mapping = "crs" ;
                number_of_wave_coordinates:_FillValue = -1L ;
        ubyte measurement_quality(latitude, longitude) ;
                measurement_quality:long_name = "measurement quality (0: good, 1-127: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold bathymetry_fit_boundaries_reached number_of_spatial_neighbors_below_threshold number_of_temporal_neighbors_below_threshold difference_from_all_temporal_neighbors_exceeds_threshold measurement_outside_area_of_validity" ;
                measurement_quality:valid_range = 0UB, 127UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB, 64UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:_FillValue = 255UB ;
  } // group time_20250115120031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per measurement period ...
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
