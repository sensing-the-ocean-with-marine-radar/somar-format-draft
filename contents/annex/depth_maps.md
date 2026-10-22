---
title: Bathymetric maps (L2a)
layout: default
parent: "Annex: Example products"
nav_order: 9
---

# L2a: Bathymetric maps

{: .informative }
> This page is informative. The product type `bathymetry` is one of the [gridded products](../product_types/gridded.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md).

Bathymetric maps (`bathymetry`) provide sea floor depth (`sea_floor_depth_below_sea_surface`) at a set of analysis locations along the platform trajectory, together with an optional standard error and a `measurement_quality` bit flag.
As for the [near-surface current maps](current_maps.md), each depth is retrieved from the wave signal in the wavenumber-frequency spectrum of a local analysis window, here exploiting the depth-induced deviation from the deep-water dispersion relation; the method is named by [`retrieval_method`](../metadata_attributes/processing_parameters.md#retrieval-methods), e.g. a least-squares fit of the wave signal to the dispersion relation that solves for water depth rather than current velocity (`dispersion_relation_least_squares_fit`; Bell [1999](../references/index.md#bell-1999)).
Because this deviation only becomes detectable once the water depth is a small enough fraction of the dominant ocean wavelength, marine radar bathymetry retrievals are limited to waters shallower than approximately 30% of the underlying ocean wavelength; `mean_wavenumber` reports the actual mean wavenumber of the wave signal used for a given measurement.

The depths are not tide-corrected (see [Product variables](../product_types/product_variables.md)); users who need depths relative to a fixed vertical datum, such as mean sea level, must apply the correction themselves.

## Example

```
netcdf or_2025-01-15-12_bathymetry {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 14.9785 ; // recommended
                :geospatial_lat_min = 14.887 ; // recommended
                :geospatial_lon_max = 146.042 ; // recommended
                :geospatial_lon_min = 145.9175 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > BATHYMETRY/SEAFLOOR TOPOGRAPHY > WATER DEPTH" ; // highly recommended
                :platform_is_mobile = "true" ;
                :product_type = "bathymetry" ;
                :summary = "Water depths from a marine X-band radar on board R/V Ocean Research, retrieved by least-squares fits of the dispersion relation to the wave signal in the wavenumber-frequency spectra of 240 s image sequences." ; // highly recommended
                :time_coverage_end = "2025-01-15T12:59:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T12:00:00Z" ; // recommended
                :title = "Marine X-band radar bathymetric maps from R/V Ocean Research" ; // highly recommended
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 1245. ; // recommended
                :analysis_window_spacing = 500. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_images = 160 ; // recommended
                :retrieval_method = "dispersion_relation_least_squares_fit" ; // recommended

group: time_20250115120031 {
  dimensions:
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
                time:long_name = "start time of bathymetry measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T12:00:31.417000Z" ; // optional
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
        double mean_wavenumber(latitude, longitude) ; // recommended
                mean_wavenumber:long_name = "mean wavenumber of the wave signal used by the bathymetry measurement" ;
                mean_wavenumber:units = "m-1" ;
                mean_wavenumber:grid_mapping = "crs" ;
                mean_wavenumber:_FillValue = NaN ;
        double sea_floor_depth_below_sea_surface_standard_error(latitude, longitude) ; // optional
                sea_floor_depth_below_sea_surface_standard_error:long_name = "standard error of the bathymetry measurement" ;
                sea_floor_depth_below_sea_surface_standard_error:units = "m" ;
                sea_floor_depth_below_sea_surface_standard_error:grid_mapping = "crs" ;
                sea_floor_depth_below_sea_surface_standard_error:_FillValue = NaN ;
        int number_of_wave_coordinates(latitude, longitude) ; // optional
                number_of_wave_coordinates:long_name = "number of wave coordinates used by the bathymetry measurement" ;
                number_of_wave_coordinates:units = "1" ;
                number_of_wave_coordinates:grid_mapping = "crs" ;
                number_of_wave_coordinates:_FillValue = -1 ;
        ubyte measurement_quality(latitude, longitude) ; // recommended
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
