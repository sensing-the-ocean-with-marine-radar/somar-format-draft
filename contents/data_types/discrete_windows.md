---
title: discrete_windows (L2)
layout: default
parent: SOMaR data types
nav_order: 7
---

# discrete_windows (L2)

Files of the data type `discrete_windows` give one value set for each of a set of analysis windows that keep their own positions but do not form a regular lattice fixed to the Earth, such as windows fixed to the platform at a constant bearing and range, or windows placed upwind of the platform.
They differ from [gridded windows](gridded_windows.md), whose windows form a regular lattice that stays fixed to the Earth, and from [averaged windows](averaged_windows.md), which merge the results of their windows into one value set per measurement.
No product type has this data type yet; the [example](#example) on this page shows near-surface currents retrieved in windows fixed to the platform.

## Windows

A file holds a sequence of measurements along the dimension `time`, each with the results of the same set of analysis windows along the dimension `window`, all in the root group.
The data variables have the dimensions `(time, window)`, followed by any dimensions of their own, such as `(time, window, wave_frequency)`; a window without a result in a measurement holds the [`_FillValue`](../metadata_attributes/variable_attributes.md#_FillValue).
The structure is the same from a moving and from a fixed platform, as stated by [`platform_is_mobile`](../metadata_attributes/mandatory_global.md#platform_is_mobile); from a fixed platform, the positions of windows fixed to the Earth repeat from one measurement to the next.

The variables `longitude` and `latitude`, with the dimensions `(time, window)`, give the position of the center of each window in each measurement, averaged over the measurement period if the window moves with the platform.
Whether the windows are fixed to the Earth or move with the platform is given by [`analysis_window_motion`](../metadata_attributes/processing_parameters.md#analysis_window_motion); windows that move with the platform require the mean velocity of the platform, as for [averaged windows](averaged_windows.md#measurements), in `platform_speed_wrt_ground` and `platform_course`.
The placement of the windows is left to the processor and should be described in the [`comment`](../metadata_attributes/optional_global.md#comment) global attribute; their range and bearing from the radar may also be stored in `window_range` and `window_bearing`.

## Variables

The file holds the following variables in the root group, in addition to those of its product.
The data variables of a product are defined under [Product variables](product_variables.md), where `(…)` stands for the dimensions `(time, window)`.

| Variable | Values | Description |
|---|---|---|
| `crs`<br><small>[CF][cf]</small> | char | Recommended. Coordinate reference system (see [Georeferencing](../georeferencing/index.md#coordinate-reference-system-variables)). Without it, `latitude` and `longitude` refer to WGS 84. |
| `time`<br><small>[CF][cf-names]</small> | double `(time)`; `seconds since 1970-01-01T00:00:00Z` | Required. Start time of each measurement. Carries `bounds = "time_bounds"` where `time_bounds` is present. |
| `time_bounds`<br><small>[CF][cf-bounds]</small> | double `(time, nv)`; `seconds since 1970-01-01T00:00:00Z` | Optional. Start and end of each measurement period, along the dimension `nv` of size 2 ([CF][cf-bounds] section 7.1). |
| `longitude`<br><small>[CF][cf-names]</small> | double `(time, window)`; `degrees_east` | Required. Longitude of the center of each analysis window, averaged over the measurement period if the window moves with the platform. |
| `latitude`<br><small>[CF][cf-names]</small> | double `(time, window)`; `degrees_north` | Required. Latitude of the center of each analysis window, averaged over the measurement period if the window moves with the platform. |
| `window_range`<br><small>SOMaR</small> | double `(time, window)` or `(window)`; `m` | Optional. Distance from the radar antenna at the start of the measurement to the center of each analysis window, as given by `longitude` and `latitude`; with the dimension `window` alone where it is the same in every measurement. |
| `window_bearing`<br><small>SOMaR</small> | double `(time, window)` or `(window)`; `degree` | Optional. Direction from the radar antenna at the start of the measurement to the center of each analysis window, clockwise from true north; with the dimension `window` alone where it is the same in every measurement. |
| `platform_speed_wrt_ground`<br><small>[CF][cf-names]</small> | double `(time)`; `m s-1` | Required if [`analysis_window_motion`](../metadata_attributes/processing_parameters.md#analysis_window_motion) is `platform_fixed`; omitted otherwise. Mean speed over ground of the platform during each measurement (see [Averaged windows](averaged_windows.md#measurements)). |
| `platform_course`<br><small>[CF][cf-names]</small> | double `(time)`; `degree` | Required if [`analysis_window_motion`](../metadata_attributes/processing_parameters.md#analysis_window_motion) is `platform_fixed`; omitted otherwise. Mean course of the platform during each measurement. |
| `radar_longitude`<br><small>SOMaR</small> | double `(time)`; `degrees_east` | Optional. Longitude of the radar antenna at the start of each measurement, from which the range and bearing of each analysis window can be recovered. |
| `radar_latitude`<br><small>SOMaR</small> | double `(time)`; `degrees_north` | Optional. Latitude of the radar antenna at the start of each measurement, from which the range and bearing of each analysis window can be recovered. |
| `measurement_quality`<br><small>SOMaR</small> | ubyte `(time, window)`; bit flags | Recommended. Quality flag of each window in each measurement. 0 is good; each bit that is set marks a failed check (see [Quality flags](../metadata_attributes/quality_flags.md)). |
{: .variable-table }

The data variables carry `coordinates = "longitude latitude"`, and `grid_mapping = "crs"` if the file holds a `crs`.
The processing parameters of discrete windows are recorded in global attributes (see [Processing parameters](../metadata_attributes/processing_parameters.md)).

## Example

A radar on a ship, with four circular analysis windows fixed to the platform at a constant range and at bearings relative to the heading of the ship, in which the near-surface current is retrieved.
The file has no [`product_type`](../metadata_attributes/optional_global.md#product_type), since no product type has this data type yet.

```
netcdf or_2025-01-15-11_discrete_windows {
dimensions:
        time = 15 ;
        window = 4 ;
variables:
        char crs ; // recommended
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of current measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude(time, window) ;
                longitude:long_name = "mean longitude of analysis window center during the measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(time, window) ;
                latitude:long_name = "mean latitude of analysis window center during the measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double window_range(window) ; // optional
                window_range:long_name = "distance from radar antenna to analysis window center" ;
                window_range:units = "m" ;
        double window_bearing(time, window) ; // optional
                window_bearing:long_name = "direction from radar antenna to analysis window center, clockwise from true north" ;
                window_bearing:units = "degree" ;
        double platform_speed_wrt_ground(time) ;
                platform_speed_wrt_ground:long_name = "mean platform speed over ground during the measurement" ;
                platform_speed_wrt_ground:standard_name = "platform_speed_wrt_ground" ;
                platform_speed_wrt_ground:units = "m s-1" ;
        double platform_course(time) ;
                platform_course:long_name = "mean platform course during the measurement" ;
                platform_course:standard_name = "platform_course" ;
                platform_course:units = "degree" ;
        double eastward_sea_water_velocity(time, window) ;
                eastward_sea_water_velocity:long_name = "eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:coordinates = "longitude latitude" ;
                eastward_sea_water_velocity:grid_mapping = "crs" ;
                eastward_sea_water_velocity:_FillValue = NaN ;
        double northward_sea_water_velocity(time, window) ;
                northward_sea_water_velocity:long_name = "northward component of the near-surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
                northward_sea_water_velocity:coordinates = "longitude latitude" ;
                northward_sea_water_velocity:grid_mapping = "crs" ;
                northward_sea_water_velocity:_FillValue = NaN ;
        ubyte measurement_quality(time, window) ; // recommended
                measurement_quality:long_name = "measurement quality (0: good, 1-127: bad)" ;
                measurement_quality:flag_meanings = "measurement_failed standard_error_above_threshold current_fit_boundaries_reached number_of_spatial_neighbors_below_threshold difference_from_all_spatial_neighbors_exceeds_threshold number_of_temporal_neighbors_below_threshold difference_from_all_temporal_neighbors_exceeds_threshold" ;
                measurement_quality:valid_range = 0UB, 127UB ;
                measurement_quality:flag_masks = 1UB, 2UB, 4UB, 8UB, 16UB, 32UB, 64UB ;
                measurement_quality:standard_name = "quality_flag" ;
                measurement_quality:coordinates = "longitude latitude" ;
                measurement_quality:grid_mapping = "crs" ;
                measurement_quality:_FillValue = 255UB ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :comment = "Four analysis windows fixed to the platform at 1500 m range, at bearings of 45, 135, 225, and 315 degrees relative to the heading of the ship" ; // recommended
                :data_type = "discrete_windows" ;
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > OCEAN CURRENTS > SURFACE CURRENTS" ; // highly recommended
                :platform_is_mobile = "true" ;
                :processing_level = "L2a" ; // recommended
                :summary = "Near-surface current vectors from a marine X-band radar on board R/V Ocean Research, retrieved in four analysis windows fixed to the platform by least-squares fits of the dispersion relation to the wave signal in the wavenumber-frequency spectra of 240 s image sequences." ; // highly recommended
                :time_coverage_end = "2025-01-15T12:00:31Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:31Z" ; // recommended
                :title = "Marine X-band radar near-surface currents in platform-fixed analysis windows from R/V Ocean Research" ; // highly recommended
                :analysis_window_motion = "platform_fixed" ; // required: the default is earth_fixed
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 1245. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_images = 160 ; // recommended
                :retrieval_method = "dispersion_relation_least_squares_fit" ; // recommended
}
```

## Products

No product type has the data type `discrete_windows` yet (see [Adding a data type or product type](index.md#adding-a-data-type-or-product-type)).
A file of this data type therefore omits [`product_type`](../metadata_attributes/optional_global.md#product_type) and carries the data variables defined under [Product variables](product_variables.md) with the dimensions `(time, window)`.

[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cf-names]: https://cfconventions.org/Data/cf-standard-names/95/build/cf-standard-name-table.html
[cf-bounds]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#cell-boundaries
