---
title: Sea ice drift maps (L2a)
layout: default
parent: Level 2 data
nav_order: 5
---

# L2a: Sea ice drift maps

Sea ice drift maps provide the horizontal sea ice drift vector at a set of analysis locations along the platform trajectory, together with a `measurement_quality` bit flag.
Each drift vector is retrieved by cross correlating a pair of temporally averaged radar backscatter intensity images, computed within a local circular analysis window, that are separated by a short time lag; the offset between the two images at the correlation peak yields the drift vector.
Because the correlation is evaluated both forward and backward in time, two independent drift vector estimates are reported for each analysis window: `eastward_sea_ice_velocity`/`northward_sea_ice_velocity` from the forward correlation, with its corresponding `correlation_coefficient`, and `eastward_sea_ice_velocity_alternative`/`northward_sea_ice_velocity_alternative` from the backward correlation, with `correlation_coefficient_alternative`.
This cross-correlation method is blind to the actual presence or absence of sea ice in the analysis window; a high correlation coefficient together with good agreement between the forward and backward drift vectors is therefore used as an indicator that sea ice, rather than open water or noise, was tracked.
As for the [near-surface current maps](current_maps.md), the analysis windows of one measurement period form a map that spans the radar footprint, and all maps belonging to one file are stored as sibling NetCDF groups, one group per measurement period, named `time_<YYYYMMDDHHMMSS>`. Within each group, the variables are stored on a two-dimensional `(latitude, longitude)` grid, on which the cells in the corners and those of analysis windows without a result hold the `_FillValue`, and the coordinate variables `latitude` and `longitude` give the centers of the analysis windows (see [Georeferencing](../../metadata_attributes/georeferencing.md#positions-of-analysis-windows)); a processor whose analysis windows lie on a local grid uses the [local-grid form](current_maps.md#local-grid-form) instead; the radar position for the period may optionally be stored in the scalar variables `radar_longitude` and `radar_latitude`.

## Variables

Each `time_<YYYYMMDDHHMMSS>` group holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Coordinate reference system (see [Georeferencing](../../metadata_attributes/georeferencing.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double; `seconds since 1970-01-01T00:00:00Z` | Start time of sea ice drift measurement. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(longitude)`; `degrees_east` | Center longitude of sea ice drift measurement. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(latitude)`; `degrees_north` | Center latitude of sea ice drift measurement. |
| `eastward_sea_ice_velocity`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m s-1` | Eastward component of the sea ice velocity from forward cross correlation. |
| `northward_sea_ice_velocity`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m s-1` | Northward component of the sea ice velocity from forward cross correlation. |
| `correlation_coefficient`<br><small>SOMaR</small> | double `(latitude, longitude)`; dimensionless | Maximum Pearson coefficient from forward cross correlation. |
| `eastward_sea_ice_velocity_alternative`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m s-1` | Eastward component of the sea ice velocity from backward cross correlation. |
| `northward_sea_ice_velocity_alternative`<br><small>SOMaR</small> | double `(latitude, longitude)`; `m s-1` | Northward component of the sea ice velocity from backward cross correlation. |
| `correlation_coefficient_alternative`<br><small>SOMaR</small> | double `(latitude, longitude)`; dimensionless | Maximum Pearson coefficient from backward cross correlation. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(latitude, longitude)`; bit flags | Quality flag: 0 is good, and each bit that is set marks a failed check, as listed in `flag_meanings`. |
{: .variable-table }

## Minimal example
```
netcdf or_2025-08-23-12_sea_ice_drift {

// global attributes:
                :title = "Marine X-band radar sea ice drift measurements with quality control flag from R/V Ocean Research" ;
                :summary = "The sea ice drift vectors are obtained through cross correlation of pairs of 30.0 s averaged radar backscatter intensity images separated by 90.0 s. The images are partitioned into analysis windows. Pixels outside the circles inscribed within each analysis window are set to zero prior to processing. The locations of the Pearson correlation coefficient peaks from two-dimensional sliding window correlations forward and backward in time yield two sea ice drift vectors per analysis window. This method is blind to the presence or absence of sea ice within the analysis window. A good indicator for the presence of sea ice are high correlation coefficients (>0.75) and a good agreement between the two sea ice drift vectors (magnitude of vector difference <0.1 m s-1). The resulting sea ice drift maps have a fixed latitude spacing and a longitude spacing that is updated within 1-degree latitude bands to ensure an approximately constant grid resolution. Analysis windows with a spatiotemporal data coverage of <90.0% are disregarded. Segments of the radar field of view that are obstructed by platform superstructures are also disregarded." ;
                :creator_email = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :history = "20250823T130500Z: File creation time" ;
                :processing_level = "L2a" ;

group: time_20250823120031 {
  dimensions:
        latitude = 32 ;
        longitude = 32 ;
  variables:
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:authority_string = "EPSG:4326" ;
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of sea ice drift measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-08-23T12:00:31.417000Z" ;
        double longitude(longitude) ;
                longitude:long_name = "center longitude of sea ice drift measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(latitude) ;
                latitude:long_name = "center latitude of sea ice drift measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_ice_velocity(latitude, longitude) ;
                eastward_sea_ice_velocity:long_name = "eastward component of the sea ice velocity from forward cross correlation" ;
                eastward_sea_ice_velocity:standard_name = "eastward_sea_ice_velocity" ;
                eastward_sea_ice_velocity:units = "m s-1" ;
                eastward_sea_ice_velocity:grid_mapping = "crs" ;
                eastward_sea_ice_velocity:_FillValue = NaN ;
        double northward_sea_ice_velocity(latitude, longitude) ;
                northward_sea_ice_velocity:long_name = "northward component of the sea ice velocity from forward cross correlation" ;
                northward_sea_ice_velocity:standard_name = "northward_sea_ice_velocity" ;
                northward_sea_ice_velocity:units = "m s-1" ;
                northward_sea_ice_velocity:grid_mapping = "crs" ;
                northward_sea_ice_velocity:_FillValue = NaN ;
        double correlation_coefficient(latitude, longitude) ;
                correlation_coefficient:long_name = "maximum Pearson coefficient from forward cross correlation" ;
                correlation_coefficient:units = "1" ;
                correlation_coefficient:grid_mapping = "crs" ;
                correlation_coefficient:_FillValue = NaN ;
        double eastward_sea_ice_velocity_alternative(latitude, longitude) ;
                eastward_sea_ice_velocity_alternative:long_name = "eastward component of the sea ice velocity from backward cross correlation" ;
                eastward_sea_ice_velocity_alternative:units = "m s-1" ;
                eastward_sea_ice_velocity_alternative:grid_mapping = "crs" ;
                eastward_sea_ice_velocity_alternative:_FillValue = NaN ;
        double northward_sea_ice_velocity_alternative(latitude, longitude) ;
                northward_sea_ice_velocity_alternative:long_name = "northward component of the sea ice velocity from backward cross correlation" ;
                northward_sea_ice_velocity_alternative:units = "m s-1" ;
                northward_sea_ice_velocity_alternative:grid_mapping = "crs" ;
                northward_sea_ice_velocity_alternative:_FillValue = NaN ;
        double correlation_coefficient_alternative(latitude, longitude) ;
                correlation_coefficient_alternative:long_name = "maximum Pearson coefficient from backward cross correlation" ;
                correlation_coefficient_alternative:units = "1" ;
                correlation_coefficient_alternative:grid_mapping = "crs" ;
                correlation_coefficient_alternative:_FillValue = NaN ;
        ubyte measurement_quality(latitude, longitude) ;
                measurement_quality:long_name = "measurement quality (0: good, 1-7: bad)" ;
                measurement_quality:flag_meanings = "forward_and_backward_cross_correlation_results_too_different sea_ice_speed_to_high correlation_coefficient_too_low" ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:_FillValue = 255UB ;
  } // group time_20250823120031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per measurement period ...
}
```

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
