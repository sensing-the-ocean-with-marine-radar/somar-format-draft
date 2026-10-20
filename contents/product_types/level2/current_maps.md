---
title: Near-surface current maps (L2a)
layout: default
parent: "Level 2: Geophysical quantities"
grand_parent: SOMaR product types
nav_order: 3
---

# L2a: Near-surface current maps

Near-surface current maps (`currents`) provide the horizontal near-surface current vector (`eastward_sea_water_velocity`, `northward_sea_water_velocity`) at a set of analysis locations along the platform trajectory, together with optional diagnostics of the retrieval and a `measurement_quality` bit flag.
As the CF standard names imply, the current vector is given relative to the ground, with the platform motion removed, and points in the direction toward which the water flows.
Each current vector is retrieved from the current-induced Doppler shift of the surface wave field, i.e. from the deviation of the wave signal in a wavenumber-frequency spectrum, computed from a radar image sequence within a local analysis window, from the linear ocean wave dispersion relation of still water.
The method is named by [`retrieval_method`](index.md#retrieval-methods): for example, a least-squares fit that minimizes the distance between the wave signal and the dispersion relation (`dispersion_relation_least_squares_fit`; Young et al. [1985](../../references/index.md#young-1985); Senet et al. [2001](../../references/index.md#senet-2001)), or the maximization of the normalized scalar product between the spectrum and a filter following the dispersion relation (`normalized_scalar_product`; Serafino et al. [2010](../../references/index.md#serafino-2010)).
The diagnostics of the retrieval depend on the method: a least-squares fit yields standard errors and `number_of_wave_coordinates`, while other methods may report a `signal_to_noise_ratio`.
Because the resulting current is a depth-weighted average, with the surface current carrying the greatest weight (Stewart and Joy [1974](../../references/index.md#stewart-joy-1974)), the effective sensing depth depends on the wavenumber range of the wave signal used in the retrieval and can be approximated as 4–8% of the underlying ocean wavelength; `mean_wavenumber` reports the actual mean wavenumber of the wave signal used for a given measurement. Wavenumbers are cyclic, i.e. the reciprocal of the wavelength, in `m-1`.
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
| `mean_wavenumber`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m-1` | Required. Mean wavenumber of the wave signal used in the retrieval, which indicates the effective sensing depth. |
| `eastward_sea_water_velocity_standard_error`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m s-1` | Optional. Standard error of the eastward component, e.g. from a least-squares fit. |
| `northward_sea_water_velocity_standard_error`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m s-1` | Optional. Standard error of the northward component, e.g. from a least-squares fit. |
| `number_of_wave_coordinates`<br><small>SOMaR</small> | int `(latitude, longitude)`; `1` | Optional. Number of points of the wave signal in the wavenumber-frequency spectrum that were used in a least-squares fit. |
| `signal_to_noise_ratio`<br><small>SOMaR</small> | double `(latitude, longitude)`; `1` | Optional. Signal-to-noise ratio of the current retrieval, as defined by the method; the definition is given in a `comment` attribute. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(latitude, longitude)`; bit flags | Required. Quality flag. 0 is good; each bit that is set marks a failed check (see [Quality flags](index.md#quality-flags)). |
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
                :analysis_window_shape = "circle" ;
                :analysis_window_size = 1245. ;
                :analysis_window_spacing = 500. ;
                :measurement_duration = 240. ;
                :number_of_images = 160 ;
                :retrieval_method = "dispersion_relation_least_squares_fit" ;

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
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
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
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
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

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
