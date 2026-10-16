---
title: Bathymetric maps (L2a)
layout: default
parent: Level 2 products
grand_parent: SOMaR product types
nav_order: 4
---

# L2a: Bathymetric maps

Bathymetric maps (`bathymetry`, short `bathy`) provide sea floor depth (`sea_floor_depth_below_sea_surface`) at a set of analysis locations along the platform trajectory, together with a standard error and a `measurement_quality` bit flag.
As for the [near-surface current maps](current_maps.md), each depth is retrieved by a least-squares fit of the wave signal in the wavenumber-frequency spectrum of a local analysis window to the ocean wave dispersion relation; here, however, the fit solves for water depth rather than current velocity, exploiting the depth-induced deviation from the deep-water dispersion relation.
Because this deviation only becomes detectable once the water depth is a small enough fraction of the dominant ocean wavelength, marine radar bathymetry retrievals are limited to waters shallower than approximately 30% of the underlying ocean wavelength; `mean_wavenumber` reports the actual mean wavenumber of the wave signal used for a given measurement.
The maps are stored as described under [Map products](index.md#map-products): one group per measurement period, on a `(latitude, longitude)` grid or in the [local-grid form](current_maps.md#local-grid-form).

As the CF standard name implies, the depth is the water depth below the actual sea surface during the measurement period, as sensed by the waves, and therefore includes the tide and other sea level variations.
The depths are not tide-corrected; users who need depths relative to a fixed vertical datum, such as mean sea level, must apply the correction themselves.

## Variables

Each `time_<YYYYMMDDHHMMSS>` group holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required. Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of the measurement period. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(longitude)`; `degrees_east` | Required. Longitude of the centers of the analysis windows. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(latitude)`; `degrees_north` | Required. Latitude of the centers of the analysis windows. |
| `sea_floor_depth_below_sea_surface`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m` | Required. Water depth, from the sea surface to the sea floor. |
| `mean_wavenumber`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m-1` | Required. Mean wavenumber of the wave signal used in the fit. |
| `sea_floor_depth_below_sea_surface_standard_error`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m` | Optional. Standard error of the water depth. |
| `number_of_wave_coordinates`<br><small>SOMaR</small> | int `(latitude, longitude)`; `1` | Optional. Number of points of the wave signal in the wavenumber-frequency spectrum that were used in the fit. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(latitude, longitude)`; bit flags | Required. Quality flag. 0 is good; each bit that is set marks a failed check (see `flag_meanings` in the example). |
{: .variable-table }

## Minimal example
```
netcdf or_2025-01-15-12_bathymetry {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "bathymetry" ;
                :analysis_window_size = 1245. ;
                :analysis_window_spacing = 500. ;
                :measurement_period_duration = 240. ;
                :number_of_images = 160 ;

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
        int number_of_wave_coordinates(latitude, longitude) ;
                number_of_wave_coordinates:long_name = "number of wave coordinates used by the bathymetry measurement" ;
                number_of_wave_coordinates:units = "1" ;
                number_of_wave_coordinates:grid_mapping = "crs" ;
                number_of_wave_coordinates:_FillValue = -1 ;
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
