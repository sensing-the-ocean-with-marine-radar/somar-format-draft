---
title: Near-surface current maps (L2a)
layout: default
parent: "Annex: Example products"
nav_order: 6
---

# L2a: Near-surface current maps

{: .informative }
> This page is informative. The product type `currents` is one of the [gridded products](../product_types/gridded.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../product_types/product_variables.md).

Near-surface current maps (`currents`) provide the horizontal near-surface current vector (`eastward_sea_water_velocity`, `northward_sea_water_velocity`) at a set of analysis locations along the platform trajectory, together with optional diagnostics of the retrieval and a `measurement_quality` bit flag.
Each current vector is retrieved from the current-induced Doppler shift of the surface wave field, i.e. from the deviation of the wave signal in a wavenumber-frequency spectrum, computed from a radar image sequence within a local analysis window, from the linear ocean wave dispersion relation of still water.
The method is named by [`retrieval_method`](../metadata_attributes/processing_parameters.md#retrieval-methods): for example, a least-squares fit that minimizes the distance between the wave signal and the dispersion relation (`dispersion_relation_least_squares_fit`; Young et al. [1985](../references/index.md#young-1985); Senet et al. [2001](../references/index.md#senet-2001)), or the maximization of the normalized scalar product between the spectrum and a filter following the dispersion relation (`normalized_scalar_product`; Serafino et al. [2010](../references/index.md#serafino-2010)).
The diagnostics of the retrieval depend on the method: a least-squares fit yields standard errors and `number_of_wave_coordinates`, while other methods may report a `signal_to_noise_ratio`.
Because the resulting current is a depth-weighted average, with the surface current carrying the greatest weight (Stewart and Joy [1974](../references/index.md#stewart-joy-1974)), the effective sensing depth depends on the wavenumber range of the wave signal used in the retrieval and can be approximated as 4–8% of the underlying ocean wavelength; `mean_wavenumber` reports the actual mean wavenumber of the wave signal used for a given measurement.
The example shows a map on the geographic grid; the variables that differ on the local grid are shown under [Local grid](../product_types/gridded.md#local-grid).

## Example

```
netcdf or_2025-01-15-11_currents {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :geospatial_lat_max = 15.03 ; // recommended
                :geospatial_lat_min = 14.9265 ; // recommended
                :geospatial_lon_max = 145.96815 ; // recommended
                :geospatial_lon_min = 145.8426 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > OCEAN CURRENTS > SURFACE CURRENTS" ; // highly recommended
                :platform_is_mobile = "true" ; // required: the platform moves
                :product_type = "currents" ;
                :summary = "Near-surface current vectors from a marine X-band radar on board R/V Ocean Research, retrieved by least-squares fits of the dispersion relation to the wave signal in the wavenumber-frequency spectra of 240 s image sequences." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:59:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar near-surface current maps from R/V Ocean Research" ; // highly recommended
                :analysis_window_shape = "circle" ; // recommended
                :analysis_window_size = 1245. ; // recommended
                :analysis_window_spacing = 500. ; // recommended
                :measurement_duration = 240. ; // recommended
                :number_of_images = 160 ; // recommended
                :retrieval_method = "dispersion_relation_least_squares_fit" ; // recommended

group: time_20250115110031 {
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
                time:long_name = "start time of current measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T11:00:31.417000Z" ; // optional
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
        double mean_wavenumber(latitude, longitude) ; // recommended
                mean_wavenumber:long_name = "mean wavenumber of the wave signal used by the current measurement" ;
                mean_wavenumber:units = "m-1" ;
                mean_wavenumber:grid_mapping = "crs" ;
                mean_wavenumber:_FillValue = NaN ;
        double eastward_sea_water_velocity_standard_error(latitude, longitude) ; // optional
                eastward_sea_water_velocity_standard_error:long_name = "standard error of the eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity_standard_error:units = "m s-1" ;
                eastward_sea_water_velocity_standard_error:grid_mapping = "crs" ;
                eastward_sea_water_velocity_standard_error:_FillValue = NaN ;
        double northward_sea_water_velocity_standard_error(latitude, longitude) ; // optional
                northward_sea_water_velocity_standard_error:long_name = "standard error of the northward component of the near-surface current velocity" ;
                northward_sea_water_velocity_standard_error:units = "m s-1" ;
                northward_sea_water_velocity_standard_error:grid_mapping = "crs" ;
                northward_sea_water_velocity_standard_error:_FillValue = NaN ;
        int number_of_wave_coordinates(latitude, longitude) ; // optional
                number_of_wave_coordinates:long_name = "number of wave coordinates used by the current measurement" ;
                number_of_wave_coordinates:units = "1" ;
                number_of_wave_coordinates:grid_mapping = "crs" ;
                number_of_wave_coordinates:_FillValue = -1 ;
        ubyte measurement_quality(latitude, longitude) ; // recommended
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
