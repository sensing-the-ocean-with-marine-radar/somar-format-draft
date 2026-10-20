---
title: Sea ice drift maps (L2a)
layout: default
parent: "Level 2: Geophysical quantities"
grand_parent: SOMaR product types
nav_order: 6
---

# L2a: Sea ice drift maps

Sea ice drift maps (`sea_ice_drift`) provide the horizontal sea ice drift vector at a set of analysis locations along the platform trajectory, together with a `measurement_quality` bit flag.
Each drift vector is retrieved from the displacement of the backscatter pattern between two radar images, which may be temporally averaged, separated by a short time lag.
The method is named by [`retrieval_method`](index.md#retrieval-methods): for example, cross-correlation of the two images within a local analysis window, where the offset at the correlation peak yields the drift vector (`cross_correlation`; Lund et al. [2018](../../references/index.md#lund-2018)), or optical flow (`optical_flow`; Thomson et al. [2021](../../references/index.md#thomson-2021)).
If the retrieval is also carried out backward in time, two independent drift vector estimates are reported for each location: `eastward_sea_ice_velocity`/`northward_sea_ice_velocity` from the forward retrieval and `eastward_sea_ice_velocity_backward`/`northward_sea_ice_velocity_backward` from the backward retrieval.
A cross-correlation reports the peak correlation coefficients of both, `correlation_coefficient` and `correlation_coefficient_backward`.
The cross-correlation method is blind to the actual presence or absence of sea ice in the analysis window; a high correlation coefficient together with good agreement between the forward and backward drift vectors is therefore used as an indicator that sea ice, rather than open water or noise, was tracked.
The maps are stored as described under [Map products](index.md#map-products): one group per measurement period, on a `(latitude, longitude)` grid or in the [local-grid form](current_maps.md#local-grid-form).

As for the [near-surface currents](current_maps.md), the drift vector is given relative to the ground, with the platform motion removed, and points in the direction toward which the ice drifts.

## Variables

Each `time_<YYYYMMDDHHMMSS>` group holds the following variables.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Required. Coordinate reference system (see [Georeferencing](../../georeferencing/index.md#coordinate-reference-system-variables)). |
| `time`<br><small>[CF][cf-names]</small> | double; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of the measurement period. |
| `longitude`<br><small>[CF][cf-names]</small> | double `(longitude)`; `degrees_east` | Required. Longitude of the centers of the analysis windows. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(latitude)`; `degrees_north` | Required. Latitude of the centers of the analysis windows. |
| `eastward_sea_ice_velocity`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m s-1` | Required. Eastward component of the sea ice drift, from the forward retrieval. |
| `northward_sea_ice_velocity`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m s-1` | Required. Northward component of the sea ice drift, from the forward retrieval. |
| `correlation_coefficient`<br><small>SOMaR</small> | double `(latitude, longitude)`; `1` | Optional. Peak Pearson correlation coefficient of the forward cross-correlation. |
| `eastward_sea_ice_velocity_backward`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m s-1` | Optional. Eastward component of the sea ice drift, from the backward retrieval. |
| `northward_sea_ice_velocity_backward`<br><small>[CF][cf-names]</small> | double `(latitude, longitude)`; `m s-1` | Optional. Northward component of the sea ice drift, from the backward retrieval. |
| `correlation_coefficient_backward`<br><small>SOMaR</small> | double `(latitude, longitude)`; `1` | Optional. Peak Pearson correlation coefficient of the backward cross-correlation. |
| `measurement_quality`<br><small>[CF][cf-names]</small> | ubyte `(latitude, longitude)`; bit flags | Required. Quality flag. 0 is good; each bit that is set marks a failed check (see [Quality flags](index.md#quality-flags)). |
{: .variable-table }

In addition to the [shared global attributes](../../metadata_attributes/index.md) and the [processing parameters of map products](index.md#processing-parameters), the file carries the following global attribute.
Since each drift vector is obtained from just two images, which `time_lag` and, if the images are averaged, the shared processing parameter [`averaging_duration`](index.md#processing-parameters) describe, the map attribute `number_of_images` is omitted.

| Attribute | Values | Description |
|---|---|---|
| `time_lag`<br><small>SOMaR</small> | Number; `s` | Required. The time between the two correlated images. |
{: .attribute-table }

## Minimal example
```
netcdf or_2025-08-23-12_sea_ice_drift {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 78.9987 ;
                :geospatial_lat_min = 78.9012 ;
                :geospatial_lon_max = 5.2276 ;
                :geospatial_lon_min = 4.8123 ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :product_type = "sea_ice_drift" ;
                :time_coverage_end = "2025-08-23T12:59:59Z" ;
                :time_coverage_start = "2025-08-23T12:00:00Z" ;
                :title = "Marine X-band radar sea ice drift maps from R/V Ocean Research" ;
                :analysis_window_shape = "circle" ;
                :analysis_window_size = 720. ;
                :analysis_window_spacing = 500. ;
                :measurement_duration = 120. ;
                :retrieval_method = "cross_correlation" ;
                :time_lag = 90. ;
                :averaging_duration = 30. ;

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
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
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
                eastward_sea_ice_velocity:long_name = "eastward component of the sea ice velocity from forward cross-correlation" ;
                eastward_sea_ice_velocity:standard_name = "eastward_sea_ice_velocity" ;
                eastward_sea_ice_velocity:units = "m s-1" ;
                eastward_sea_ice_velocity:grid_mapping = "crs" ;
                eastward_sea_ice_velocity:_FillValue = NaN ;
        double northward_sea_ice_velocity(latitude, longitude) ;
                northward_sea_ice_velocity:long_name = "northward component of the sea ice velocity from forward cross-correlation" ;
                northward_sea_ice_velocity:standard_name = "northward_sea_ice_velocity" ;
                northward_sea_ice_velocity:units = "m s-1" ;
                northward_sea_ice_velocity:grid_mapping = "crs" ;
                northward_sea_ice_velocity:_FillValue = NaN ;
        double correlation_coefficient(latitude, longitude) ;
                correlation_coefficient:long_name = "maximum Pearson coefficient from forward cross-correlation" ;
                correlation_coefficient:units = "1" ;
                correlation_coefficient:grid_mapping = "crs" ;
                correlation_coefficient:_FillValue = NaN ;
        double eastward_sea_ice_velocity_backward(latitude, longitude) ;
                eastward_sea_ice_velocity_backward:long_name = "eastward component of the sea ice velocity from backward cross-correlation" ;
                eastward_sea_ice_velocity_backward:standard_name = "eastward_sea_ice_velocity" ;
                eastward_sea_ice_velocity_backward:units = "m s-1" ;
                eastward_sea_ice_velocity_backward:grid_mapping = "crs" ;
                eastward_sea_ice_velocity_backward:_FillValue = NaN ;
        double northward_sea_ice_velocity_backward(latitude, longitude) ;
                northward_sea_ice_velocity_backward:long_name = "northward component of the sea ice velocity from backward cross-correlation" ;
                northward_sea_ice_velocity_backward:standard_name = "northward_sea_ice_velocity" ;
                northward_sea_ice_velocity_backward:units = "m s-1" ;
                northward_sea_ice_velocity_backward:grid_mapping = "crs" ;
                northward_sea_ice_velocity_backward:_FillValue = NaN ;
        double correlation_coefficient_backward(latitude, longitude) ;
                correlation_coefficient_backward:long_name = "maximum Pearson coefficient from backward cross-correlation" ;
                correlation_coefficient_backward:units = "1" ;
                correlation_coefficient_backward:grid_mapping = "crs" ;
                correlation_coefficient_backward:_FillValue = NaN ;
        ubyte measurement_quality(latitude, longitude) ;
                measurement_quality:long_name = "measurement quality (0: good, 1-7: bad)" ;
                measurement_quality:flag_meanings = "forward_and_backward_cross_correlation_results_too_different sea_ice_speed_too_high correlation_coefficient_too_low" ;
                measurement_quality:valid_range = 0UB, 7UB ;
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
