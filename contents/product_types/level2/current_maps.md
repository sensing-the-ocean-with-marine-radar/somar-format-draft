---
title: Near-surface current maps (L2a)
layout: default
parent: Level 2 products
grand_parent: SOMaR product types
nav_order: 3
---

# L2a: Near-surface current maps

Near-surface current maps (`currents`, short `cur`) provide the horizontal near-surface current vector (`eastward_sea_water_velocity`, `northward_sea_water_velocity`) at a set of analysis locations along the platform trajectory, together with per-component standard errors and a `measurement_quality` bit flag.
As the CF standard names imply, the current vector is given relative to the ground, with the platform motion removed, and points in the direction toward which the water flows.
Each current vector is retrieved through a least-squares fit that minimizes the distance between the wave signal found in a wavenumber-frequency spectrum, computed from a radar backscatter intensity image sequence within a local circular analysis window, and the linear ocean wave dispersion relation, exploiting the current-induced Doppler shift of the surface wave field.
Because the resulting current is a depth-weighted average, with the surface current carrying the greatest weight, the effective sensing depth depends on the wavenumber range of the wave signal used in the fit and can be approximated as 4–8% of the underlying ocean wavelength; `mean_wavenumber` reports the actual mean wavenumber of the wave signal used for a given measurement. Wavenumbers are cyclic, i.e. the reciprocal of the wavelength, in `m-1`.
The maps are stored as described under [Map products](index.md#map-products): one group per measurement period, on a `(latitude, longitude)` grid or in the [local-grid form](#local-grid-form).

## Variables

Each `time_<YYYYMMDDHHMMSS>` group holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required. Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of the measurement period. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(longitude)`; `degrees_east` | Required. Longitude of the centers of the analysis windows. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(latitude)`; `degrees_north` | Required. Latitude of the centers of the analysis windows. |
| `eastward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m s-1` | Required. Eastward component of the near-surface current. |
| `northward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m s-1` | Required. Northward component of the near-surface current. |
| `mean_wavenumber`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m-1` | Required. Mean wavenumber of the wave signal used in the fit, which indicates the effective sensing depth. |
| `eastward_sea_water_velocity_standard_error`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m s-1` | Optional. Standard error of the eastward component. |
| `northward_sea_water_velocity_standard_error`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m s-1` | Optional. Standard error of the northward component. |
| `number_of_wave_coordinates`<br><small>SOMaR</small> | int `(latitude, longitude)`; `1` | Optional. Number of points of the wave signal in the wavenumber-frequency spectrum that were used in the fit. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(latitude, longitude)`; bit flags | Required. Quality flag. 0 is good; each bit that is set marks a failed check (see `flag_meanings` in the example). |
{: .variable-table }

## Minimal example
```
netcdf or_2025-01-15-11_currents {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 15.03 ;
                :geospatial_lat_min = 14.9265 ;
                :geospatial_lon_max = 145.96815 ;
                :geospatial_lon_min = 145.8426 ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :product_type = "currents" ;
                :time_coverage_end = "2025-01-15T11:59:59Z" ;
                :time_coverage_start = "2025-01-15T11:00:00Z" ;
                :title = "Marine X-band radar near-surface current maps from R/V Ocean Research" ;
                :analysis_window_size = 1245. ;
                :analysis_window_spacing = 500. ;
                :measurement_period_duration = 240. ;
                :number_of_images = 160 ;

group: time_20250115110031 {
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
                time:long_name = "start time of current measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T11:00:31.417000Z" ;
        double longitude(longitude) ;
                longitude:long_name = "center longitude of current measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(latitude) ;
                latitude:long_name = "center latitude of current measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_water_velocity(latitude, longitude) ;
                eastward_sea_water_velocity:long_name = "eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:_FillValue = NaN ;
        double northward_sea_water_velocity(latitude, longitude) ;
                northward_sea_water_velocity:long_name = "northward component of the near-surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
                northward_sea_water_velocity:grid_mapping = "crs" ;
                northward_sea_water_velocity:_FillValue = NaN ;
        double mean_wavenumber(latitude, longitude) ;
                mean_wavenumber:long_name = "mean wavenumber of the wave signal used by the current measurement" ;
                mean_wavenumber:units = "m-1" ;
                mean_wavenumber:grid_mapping = "crs" ;
                mean_wavenumber:_FillValue = NaN ;
        double eastward_sea_water_velocity_standard_error(latitude, longitude) ;
                eastward_sea_water_velocity_standard_error:long_name = "standard error of the eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity_standard_error:units = "m s-1" ;
                eastward_sea_water_velocity_standard_error:grid_mapping = "crs" ;
                eastward_sea_water_velocity_standard_error:_FillValue = NaN ;
        double northward_sea_water_velocity_standard_error(latitude, longitude) ;
                northward_sea_water_velocity_standard_error:long_name = "standard error of the northward component of the near-surface current velocity" ;
                northward_sea_water_velocity_standard_error:units = "m s-1" ;
                northward_sea_water_velocity_standard_error:grid_mapping = "crs" ;
                northward_sea_water_velocity_standard_error:_FillValue = NaN ;
        int number_of_wave_coordinates(latitude, longitude) ;
                number_of_wave_coordinates:long_name = "number of wave coordinates used by the current measurement" ;
                number_of_wave_coordinates:units = "1" ;
                number_of_wave_coordinates:grid_mapping = "crs" ;
                number_of_wave_coordinates:_FillValue = -1 ;
        ubyte measurement_quality(latitude, longitude) ;
                measurement_quality:long_name = "measurement quality (0: good, 1-127: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold current_fit_boundaries_reached number_of_spatial_neighbors_below_threshold difference_from_all_spatial_neighbors_exceeds_threshold number_of_temporal_neighbors_below_threshold difference_from_all_temporal_neighbors_exceeds_threshold" ;
                measurement_quality:valid_range = 0UB, 127UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB, 64UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:_FillValue = 255UB ;
  } // group time_20250115110031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per measurement period ...
}
```

## Local-grid form

A processor whose analysis windows lie on a local grid around the radar stores the grid itself, as the [roughness images](roughness_images.md) do: `x` and `y` give the distance in meters east and north of the radar, and `crs` describes the local projection centered on the position of the radar antenna for that period.
`longitude` and `latitude` remain mandatory, as two-dimensional variables, so that every file gives the geographic position of each analysis window.
Only the variables that differ from the example above are shown:

```
// excerpt: only the variables that differ
group: time_20250115110031 {
  dimensions:
        y = 17 ;
        x = 17 ;
  variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 145.868167860183 ;
                crs:latitude_of_projection_origin = 14.9952749946079 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:projected_crs_name = "WGS 84 / origin of coordinate system is radar location at measurement start time" ;
                crs:geographic_crs_name = "WGS 84" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
        double x(x) ;
                x:long_name = "eastward distance from radar position at measurement start time" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from radar position at measurement start time" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        double longitude(y, x) ;
                longitude:long_name = "center longitude of current measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(y, x) ;
                latitude:long_name = "center latitude of current measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_water_velocity(y, x) ;
                eastward_sea_water_velocity:long_name = "eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:coordinates = "longitude latitude" ;
                eastward_sea_water_velocity:_FillValue = NaN ;
        ... // all other data variables likewise on (y, x), with grid_mapping and coordinates ...
  } // group time_20250115110031
```

## Near-surface current profile maps

Near-surface current profile maps (`currents_profile`, short `cur_profile`) extend the near-surface current maps above by repeating the same dispersion-relation current fit for a set of distinct wavenumber bands rather than a single fixed wave-signal wavenumber range, providing an approximate vertical profile of near-surface current shear.
The variables therefore have an additional dimension `wavenumber_bin`, i.e. `(wavenumber_bin, latitude, longitude)`, with one layer per wavenumber band; cells for which no fit was attempted hold the `_FillValue`.
The coordinate variable `wavenumber_bin` gives the center of each wavenumber band, and its `bounds` attribute names the variable `wavenumber_bin_bounds`, which holds the lower and upper edge of each band ([CF][cf], section 7.1), both in `m-1`, so the bands need not be of equal width; as in the near-surface current maps, `mean_wavenumber` reports the actual mean wavenumber of the wave signal used in that particular fit, and since the effective sensing depth increases with wavelength, the wavenumber-dependence of the current fits amounts to a measure of upper-ocean vertical current shear.
All other variables (current components, standard errors, `number_of_wave_coordinates`, `measurement_quality`) are defined identically to the near-surface current maps above.

### Variables

The variables are those of the near-surface current maps, with the additional dimension `wavenumber_bin`, and the following variables.

| Variable | Values | Description |
|---|---|---|
| `wavenumber_bin`<br><small>SOMaR</small> | double `(wavenumber_bin)`; `m-1` | Required. Center of each wavenumber band; its `bounds` attribute is `"wavenumber_bin_bounds"`. |
| `wavenumber_bin_bounds`<br><small>SOMaR</small> | double `(wavenumber_bin, nv)`; `m-1` | Required. Lower and upper edge of each wavenumber band, with `nv = 2` ([CF][cf], section 7.1). |
{: .variable-table }

### Minimal example
```
netcdf or_2025-01-15-11_currents_profile {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 15.03 ;
                :geospatial_lat_min = 14.9265 ;
                :geospatial_lon_max = 145.96815 ;
                :geospatial_lon_min = 145.8426 ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :product_type = "currents_profile" ;
                :time_coverage_end = "2025-01-15T11:59:59Z" ;
                :time_coverage_start = "2025-01-15T11:00:00Z" ;
                :title = "Marine X-band radar near-surface current profile maps from R/V Ocean Research" ;
                :analysis_window_size = 1245. ;
                :analysis_window_spacing = 500. ;
                :measurement_period_duration = 240. ;
                :number_of_images = 160 ;

group: time_20250115110031 {
  dimensions:
        wavenumber_bin = 13 ;
        nv = 2 ;
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
                time:long_name = "start time of current measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T11:00:31.417000Z" ;
        double wavenumber_bin(wavenumber_bin) ;
                wavenumber_bin:long_name = "center of the wavenumber band used by the current measurement" ;
                wavenumber_bin:units = "m-1" ;
                wavenumber_bin:bounds = "wavenumber_bin_bounds" ;
        double wavenumber_bin_bounds(wavenumber_bin, nv) ;
        double longitude(longitude) ;
                longitude:long_name = "center longitude of current measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(latitude) ;
                latitude:long_name = "center latitude of current measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_water_velocity(wavenumber_bin, latitude, longitude) ;
                eastward_sea_water_velocity:long_name = "eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:_FillValue = NaN ;
        double northward_sea_water_velocity(wavenumber_bin, latitude, longitude) ;
                northward_sea_water_velocity:long_name = "northward component of the near-surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
                northward_sea_water_velocity:grid_mapping = "crs" ;
                northward_sea_water_velocity:_FillValue = NaN ;
        double mean_wavenumber(wavenumber_bin, latitude, longitude) ;
                mean_wavenumber:long_name = "mean wavenumber of the wave signal used by the current measurement" ;
                mean_wavenumber:units = "m-1" ;
                mean_wavenumber:grid_mapping = "crs" ;
                mean_wavenumber:_FillValue = NaN ;
        double eastward_sea_water_velocity_standard_error(wavenumber_bin, latitude, longitude) ;
                eastward_sea_water_velocity_standard_error:long_name = "standard error of the eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity_standard_error:units = "m s-1" ;
                eastward_sea_water_velocity_standard_error:grid_mapping = "crs" ;
                eastward_sea_water_velocity_standard_error:_FillValue = NaN ;
        double northward_sea_water_velocity_standard_error(wavenumber_bin, latitude, longitude) ;
                northward_sea_water_velocity_standard_error:long_name = "standard error of the northward component of the near-surface current velocity" ;
                northward_sea_water_velocity_standard_error:units = "m s-1" ;
                northward_sea_water_velocity_standard_error:grid_mapping = "crs" ;
                northward_sea_water_velocity_standard_error:_FillValue = NaN ;
        int number_of_wave_coordinates(wavenumber_bin, latitude, longitude) ;
                number_of_wave_coordinates:long_name = "number of wave coordinates used by the current measurement" ;
                number_of_wave_coordinates:units = "1" ;
                number_of_wave_coordinates:grid_mapping = "crs" ;
                number_of_wave_coordinates:_FillValue = -1 ;
        ubyte measurement_quality(wavenumber_bin, latitude, longitude) ;
                measurement_quality:long_name = "measurement quality (0: good, 1-127: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold current_fit_boundaries_reached number_of_spatial_neighbors_below_threshold difference_from_all_spatial_neighbors_exceeds_threshold number_of_temporal_neighbors_below_threshold difference_from_all_temporal_neighbors_exceeds_threshold" ;
                measurement_quality:valid_range = 0UB, 127UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB, 64UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:_FillValue = 255UB ;
  } // group time_20250115110031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per measurement period ...
}
```

In this example the 13 bands are contiguous and of equal width, covering wavelengths from 60 m down to 16.7 m; the upper edge of each band is the lower edge of the next.
The values of the band variables are:

```
// excerpt: data of the wavenumber band variables
data:

 wavenumber_bin = 0.018346, 0.021681, 0.025017, 0.028353, 0.031688, 0.035024,
    0.038360, 0.041695, 0.045031, 0.048367, 0.051702, 0.055038, 0.058374 ;

 wavenumber_bin_bounds =
  0.016678, 0.020014,
  0.020014, 0.023349,
  0.023349, 0.026685,
  0.026685, 0.030021,
  0.030021, 0.033356,
  0.033356, 0.036692,
  0.036692, 0.040028,
  0.040028, 0.043363,
  0.043363, 0.046699,
  0.046699, 0.050035,
  0.050035, 0.053370,
  0.053370, 0.056706,
  0.056706, 0.060042 ;
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
