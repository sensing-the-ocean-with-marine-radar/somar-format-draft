---
title: Near-surface current maps (L2a)
layout: default
parent: Level 2 data
nav_order: 3
---

# L2a: Near-surface current maps

Near-surface current maps provide the horizontal near-surface current vector (`eastward_sea_water_velocity`, `northward_sea_water_velocity`) at a set of analysis locations along the platform trajectory, together with per-component standard errors and a `measurement_quality` bit flag.
Each current vector is retrieved through a least-squares fit that minimizes the distance between the wave signal found in a wavenumber-frequency spectrum, computed from a radar backscatter intensity image sequence within a local circular analysis window, and the linear ocean wave dispersion relation, exploiting the current-induced Doppler shift of the surface wave field.
Because the resulting current is a depth-weighted average, with the surface current carrying the greatest weight, the effective sensing depth depends on the wavenumber range of the wave signal used in the fit and can be approximated as 4-8% of the underlying ocean wavelength; `mean_wavenumber` reports the actual mean wavenumber of the wave signal used for a given measurement. Wavenumbers are cyclic, i.e. the reciprocal of the wavelength, in `m-1`.
The analysis windows of one measurement period form a map that spans the radar footprint, and with a moving vessel the area covered changes from one period to the next.
All maps belonging to one file are therefore stored as sibling NetCDF groups, one group per measurement period, named `time_<YYYYMMDDHHMMSS>` after the start time of that period, as for the [roughness images](roughness_images.md).
Within each group, the variables are stored on a two-dimensional grid with the dimensions `(latitude, longitude)`, and the scalar variable `time` gives the start time of the period.
Since the radar footprint is circular, the cells in the corners of the grid hold the `_FillValue`, as do the cells of analysis windows without a result.
The coordinate variables `latitude` and `longitude` give the centers of the analysis windows. They are one-dimensional because the windows lie on an Earth-fixed lattice with a single longitude spacing per measurement period, so that each map is a rectangular grid in longitude and latitude (see [Georeferencing](../../metadata_attributes/georeferencing.md#positions-of-analysis-windows)). A processor whose analysis windows lie on a local grid around the radar instead uses the [local-grid form](#local-grid-form) of a group.
The radar position for the period may optionally be stored in the scalar variables `radar_longitude` and `radar_latitude`.

## Variables

Each `time_<YYYYMMDDHHMMSS>` group holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Coordinate reference system (see [Georeferencing](../../metadata_attributes/georeferencing.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double; `seconds since 1970-01-01T00:00:00Z` | Start time of the measurement period. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(longitude)`; `degrees_east` | Longitude of the centers of the analysis windows. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(latitude)`; `degrees_north` | Latitude of the centers of the analysis windows. |
| `eastward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m s-1` | Eastward component of the near-surface current. |
| `northward_sea_water_velocity`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m s-1` | Northward component of the near-surface current. |
| `mean_wavenumber`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m-1` | Mean wavenumber of the wave signal used in the fit, which indicates the effective sensing depth. |
| `eastward_sea_water_velocity_standard_error`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m s-1` | Standard error of the eastward component. |
| `northward_sea_water_velocity_standard_error`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m s-1` | Standard error of the northward component. |
| `number_of_wave_coordinates`<br><small>SOMaR</small> | int64 `(latitude, longitude)`; dimensionless | Number of points of the wave signal in the wavenumber-frequency spectrum that were used in the fit. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(latitude, longitude)`; bit flags | Quality flag. 0 is good; each bit that is set marks a failed check (see `flag_meanings` in the example). |
{: .variable-table }

## Minimal example
```
netcdf or_2025-01-15-11_currents {

// global attributes:
                :title = "Marine X-band radar near-surface current measurements with quality control flag from R/V Ocean Research" ;
                :summary = "The near-surface current vectors are obtained through least-squares fits that minimize the distance between the wave signal found in marine X-band radar backscatter intensity wavenumber frequency spectra and the linear ocean wave dispersion shell. Here, the spectra are based on 4.0 min long radar backscatter intensity image sequences that are partitioned into analysis windows. Pixels outside the circles inscribed within each analysis window are set to zero prior to processing. The resulting current maps have a fixed latitude spacing and a longitude spacing that is updated within 1-degree latitude bands to ensure an approximately constant grid resolution. The spatial overlap between neighboring analysis windows is 50.0% and the temporal overlap between consecutive analysis periods is 25.0%. Analysis windows with a spatiotemporal data coverage of <90.0% are disregarded. Segments of the radar field of view that are obstructed by platform superstructures are also disregarded. The effective depth of the radar currents is a weighted mean of the upper ocean with the surface current carrying the greatest weight. It can be approximated as 4-8% of the underlying ocean wavelength depending on the shape of the current profile." ;
                :creator_email = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :history = "20250115T120500Z: File creation time" ;
                :processing_level = "L2a" ;

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
                crs:authority_string = "EPSG:4326" ;
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
                eastward_sea_water_velocity:long_name = "eastward component of the near surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:_FillValue = NaN ;
        double northward_sea_water_velocity(latitude, longitude) ;
                northward_sea_water_velocity:long_name = "northward component of the near surface current velocity" ;
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
                eastward_sea_water_velocity_standard_error:long_name = "standard error of the eastward component of the near surface current velocity" ;
                eastward_sea_water_velocity_standard_error:units = "m s-1" ;
                eastward_sea_water_velocity_standard_error:grid_mapping = "crs" ;
                eastward_sea_water_velocity_standard_error:_FillValue = NaN ;
        double northward_sea_water_velocity_standard_error(latitude, longitude) ;
                northward_sea_water_velocity_standard_error:long_name = "standard error of the northward component of the near surface current velocity" ;
                northward_sea_water_velocity_standard_error:units = "m s-1" ;
                northward_sea_water_velocity_standard_error:grid_mapping = "crs" ;
                northward_sea_water_velocity_standard_error:_FillValue = NaN ;
        int64 number_of_wave_coordinates(latitude, longitude) ;
                number_of_wave_coordinates:long_name = "number of wave coordinates used by the current measurement" ;
                number_of_wave_coordinates:units = "1" ;
                number_of_wave_coordinates:grid_mapping = "crs" ;
                number_of_wave_coordinates:_FillValue = -1L ;
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
                eastward_sea_water_velocity:long_name = "eastward component of the near surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:coordinates = "longitude latitude" ;
                eastward_sea_water_velocity:_FillValue = NaN ;
        ... // all other data variables likewise on (y, x), with grid_mapping and coordinates ...
  } // group time_20250115110031
```

## Near-surface current profile maps

Near-surface current profile maps extend the near-surface current maps above by repeating the same dispersion-relation current fit for a set of distinct wavenumber bands rather than a single fixed wave-signal wavenumber range, providing an approximate vertical profile of near-surface current shear.
The variables therefore have an additional dimension `wavenumber_bin`, i.e. `(wavenumber_bin, latitude, longitude)`, with one layer per wavenumber band; cells for which no fit was attempted hold the `_FillValue`.
The lower bound of each wavenumber band is given by `lower_wavenumber_bin_edge`, which has the dimension `wavenumber_bin`, with the (fixed) band width given by the global attribute `wavenumber_bin_size`, both in `m-1`; as in the near-surface current maps, `mean_wavenumber` reports the actual mean wavenumber of the wave signal used in that particular fit, and since the effective sensing depth increases with wavelength, the wavenumber-dependence of the current fits amounts to a measure of upper-ocean vertical current shear.
All other variables (current components, standard errors, `number_of_wave_coordinates`, `measurement_quality`) are defined identically to the near-surface current maps above.

### Variables

The variables are those of the near-surface current maps, with the additional dimension `wavenumber_bin`, and the following variable.

| Variable | Values | Description |
|---|---|---|
| `lower_wavenumber_bin_edge`<br><small>SOMaR</small> | double `(wavenumber_bin)`; `m-1` | Lower edge of each wavenumber band. |
{: .variable-table }

In addition to the [shared global attributes](../../metadata_attributes/index.md), the file carries the following global attribute.

| Attribute | Values | Description |
|---|---|---|
| `wavenumber_bin_size`<br><small>SOMaR</small> | Number; `m-1` | The width of the wavenumber bands. |
{: .attribute-table }

### Minimal example
```
netcdf or_2025-01-15-11_currents_profile {

// global attributes:
                :title = "Marine X-band radar near-surface current measurements with quality control flag from R/V Ocean Research" ;
                :wavenumber_bin_size = 0.00333564095198152 ;
                :summary = "... as for near-surface current maps above; since the effective depth increases with ocean wavelength, we obtain a measure of upper ocean vertical shear by performing current fits as a function of wavenumber." ;
                :creator_email = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :history = "20250115T120500Z: File creation time" ;
                :processing_level = "L2a" ;

group: time_20250115110031 {
  dimensions:
        wavenumber_bin = 6 ;
        latitude = 17 ;
        longitude = 17 ;
  variables:
        ... // crs, time, longitude, and latitude as for near-surface current maps above;
            // eastward/northward_sea_water_velocity, mean_wavenumber, standard errors,
            // number_of_wave_coordinates, and measurement_quality on (wavenumber_bin, latitude, longitude) ...
        double lower_wavenumber_bin_edge(wavenumber_bin) ;
                lower_wavenumber_bin_edge:long_name = "lower edge of the wavenumber bin used by the current measurement" ;
                lower_wavenumber_bin_edge:units = "m-1" ;
                lower_wavenumber_bin_edge:grid_mapping = "crs" ;
  } // group time_20250115110031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per measurement period ...
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
