---
title: Near-surface current profile maps (L2a)
layout: default
parent: "Annex: Example products"
nav_order: 8
---

# L2a: Near-surface current profile maps

{: .informative }
> This page is informative. The product type `currents_profile` is one of the [gridded products](../product_types/gridded.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md). The [file contents](#file-contents) summarize these definitions for this product; where they differ, the definitions apply.

Near-surface current profile maps (`currents_profile`) extend the [near-surface current maps](current_maps.md) by repeating the same current retrieval for a set of distinct wavenumber bands rather than a single wavenumber range; since the effective sensing depth decreases with increasing wavenumber, the resulting currents provide an approximate vertical profile of the upper-ocean current and thus of its vertical shear (Lund et al. [2015](../references/index.md#lund-2015); Campana et al. [2016](../references/index.md#campana-2016)).
The data variables therefore have an additional dimension [`wavenumber_bin`](../product_types/product_variables.md#wavenumber_bin), with one layer per wavenumber band, whose edges are given by [`wavenumber_bin_bounds`](../product_types/product_variables.md#wavenumber_bin_bounds), so that the bands need not be of equal width; cells for which no retrieval was attempted or for which the retrieval failed hold the [`_FillValue`](../metadata_attributes/variable_attributes.md#_FillValue).
As in the current maps, [`mean_wavenumber`](../product_types/product_variables.md#mean_wavenumber) reports the actual mean wavenumber of the wave signal used in each retrieval.

## File contents

A file of this product holds the following items; each links to its definition, and the condition, where one is given, states when the tier applies.

| Item | Tier | Condition |
|---|---|---|
| **Layout** | | |
| one [time-bounded grid](../product_types/gridded.md#time-bounded-grids) per measurement, each in a `time_<YYYYMMDDHHMMSS>` group | Required | moving platform |
| one [single grid](../product_types/gridded.md#fixed-platform) in the root group, with the leading dimension `time` | Required | fixed platform |
| the [geographic grid](../product_types/gridded.md#geographic-grid) `(latitude, longitude)` or the [local grid](../product_types/gridded.md#local-grid) `(y, x)` | Required | |
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`product_type`](../metadata_attributes/mandatory_global.md#product_type) `= "currents_profile"` | Required | |
| [`platform_is_mobile`](../metadata_attributes/optional_global.md#platform_is_mobile) `= "true"` | Required | moving platform |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| [`analysis_window_shape`](../metadata_attributes/processing_parameters.md#analysis_window_shape), [`analysis_window_size`](../metadata_attributes/processing_parameters.md#analysis_window_size), [`analysis_window_spacing`](../metadata_attributes/processing_parameters.md#analysis_window_spacing), [`measurement_duration`](../metadata_attributes/processing_parameters.md#measurement_duration), [`number_of_images`](../metadata_attributes/processing_parameters.md#number_of_images), [`retrieval_method`](../metadata_attributes/processing_parameters.md#retrieval_method) | Recommended | |
| **Variables of each grid** | | |
| [`time`](../product_types/gridded.md#variables-time) | Required | |
| [`time_iso_8601`](../metadata_attributes/variable_attributes.md#time_iso_8601) on `time` | Optional | moving platform |
| [`time_bounds`](../product_types/gridded.md#time_bounds) | Optional | |
| [`latitude`](../product_types/gridded.md#variables-latitude), [`longitude`](../product_types/gridded.md#variables-longitude) | Required | |
| [`x`](../product_types/gridded.md#variables-x), [`y`](../product_types/gridded.md#variables-y) | Required | local grid |
| [`crs`](../product_types/gridded.md#variables-crs) | Required | local grid |
| [`crs`](../product_types/gridded.md#variables-crs) | Recommended | geographic grid |
| [`radar_latitude`](../product_types/gridded.md#radar_latitude), [`radar_longitude`](../product_types/gridded.md#radar_longitude) | Optional | |
| [`wavenumber_bin`](../product_types/product_variables.md#wavenumber_bin), [`wavenumber_bin_bounds`](../product_types/product_variables.md#wavenumber_bin_bounds); all data variables, `measurement_quality` included, have the dimension `wavenumber_bin` before those of the grid | Required | |
| [`eastward_sea_water_velocity`](../product_types/product_variables.md#eastward_sea_water_velocity), [`northward_sea_water_velocity`](../product_types/product_variables.md#northward_sea_water_velocity) | Required | |
| [`mean_wavenumber`](../product_types/product_variables.md#mean_wavenumber) | Recommended | |
| [`eastward_sea_water_velocity_standard_error`](../product_types/product_variables.md#eastward_sea_water_velocity_standard_error), [`northward_sea_water_velocity_standard_error`](../product_types/product_variables.md#northward_sea_water_velocity_standard_error), [`number_of_fitted_spectral_points`](../product_types/product_variables.md#number_of_fitted_spectral_points), [`signal_to_noise_ratio`](../product_types/product_variables.md#signal_to_noise_ratio) | Optional | |
| [`measurement_quality`](../product_types/gridded.md#measurement_quality) | Recommended | |
| [`coordinates`](../metadata_attributes/variable_attributes.md#coordinates) `= "longitude latitude"` on the data variables | Required | local grid |
| [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) `= "crs"` on the data variables | Required | with `crs` |
{: .contents-table }

## Example

```
netcdf or_2025-01-15-11_currents_profile {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 15.03 ; // recommended
                :geospatial_lat_min = 14.9265 ; // recommended
                :geospatial_lon_max = 145.96815 ; // recommended
                :geospatial_lon_min = 145.8426 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > OCEAN CURRENTS > CURRENT PROFILES, EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > OCEAN CURRENTS > VERTICAL CURRENT SHEAR" ; // highly recommended
                :platform_is_mobile = "true" ;
                :product_type = "currents_profile" ;
                :summary = "Near-surface current profiles from a marine X-band radar on board R/V Ocean Research, retrieved by least-squares fits of the dispersion relation to the wave signal in separate wavenumber bands, which sense different depths." ; // highly recommended
                :time_coverage_end = "2025-01-15T12:00:00.775429Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:31.417000Z" ; // recommended
                :title = "Marine X-band radar near-surface current profile maps from R/V Ocean Research" ; // highly recommended
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 1245. ; // recommended
                :analysis_window_spacing = 500. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_images = 160 ; // recommended
                :retrieval_method = "dispersion_relation_least_squares_fit" ; // recommended

group: time_20250115110031 {
  dimensions:
        wavenumber_bin = 13 ;
        nv = 2 ;
        latitude = 17 ;
        longitude = 17 ;
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
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of current measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T11:00:31.417000Z" ; // optional
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
        double mean_wavenumber(wavenumber_bin, latitude, longitude) ; // recommended
                mean_wavenumber:long_name = "mean wavenumber of the wave signal used by the current measurement" ;
                mean_wavenumber:units = "m-1" ;
                mean_wavenumber:grid_mapping = "crs" ;
                mean_wavenumber:_FillValue = NaN ;
        double eastward_sea_water_velocity_standard_error(wavenumber_bin, latitude, longitude) ; // optional
                eastward_sea_water_velocity_standard_error:long_name = "standard error of the eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity_standard_error:units = "m s-1" ;
                eastward_sea_water_velocity_standard_error:grid_mapping = "crs" ;
                eastward_sea_water_velocity_standard_error:_FillValue = NaN ;
        double northward_sea_water_velocity_standard_error(wavenumber_bin, latitude, longitude) ; // optional
                northward_sea_water_velocity_standard_error:long_name = "standard error of the northward component of the near-surface current velocity" ;
                northward_sea_water_velocity_standard_error:units = "m s-1" ;
                northward_sea_water_velocity_standard_error:grid_mapping = "crs" ;
                northward_sea_water_velocity_standard_error:_FillValue = NaN ;
        int number_of_fitted_spectral_points(wavenumber_bin, latitude, longitude) ; // optional
                number_of_fitted_spectral_points:long_name = "number of points of the wavenumber-frequency spectrum used in the least-squares fit" ;
                number_of_fitted_spectral_points:units = "1" ;
                number_of_fitted_spectral_points:grid_mapping = "crs" ;
                number_of_fitted_spectral_points:_FillValue = -1 ;
        ubyte measurement_quality(wavenumber_bin, latitude, longitude) ; // recommended
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

### Minimal form

The smallest file of this product that complies with SOMaR, obtained by removing the marked items from the example (see [Reading the examples](index.md#reading-the-examples)):

```
// minimal form of the example above
netcdf or_2025-01-15-11_currents_profile {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :platform_is_mobile = "true" ;
                :product_type = "currents_profile" ;

group: time_20250115110031 {
  dimensions:
        wavenumber_bin = 13 ;
        nv = 2 ;
        latitude = 17 ;
        longitude = 17 ;
  variables:
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of current measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
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
                eastward_sea_water_velocity:_FillValue = NaN ;
        double northward_sea_water_velocity(wavenumber_bin, latitude, longitude) ;
                northward_sea_water_velocity:long_name = "northward component of the near-surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
                northward_sea_water_velocity:_FillValue = NaN ;
  } // group time_20250115110031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per measurement period ...
}
```
