---
title: Sea ice drift maps
layout: default
parent: Gridded data
nav_order: 5
---

# Sea ice drift maps

Sea ice drift maps provide the horizontal sea ice drift vector at a set of analysis locations along the platform trajectory, together with a `measurement_quality` bit flag.
Each drift vector is retrieved by cross correlating a pair of temporally averaged radar backscatter intensity images, computed within a local circular analysis window, that are separated by a short time lag; the offset between the two images at the correlation peak yields the drift vector.
Because the correlation is evaluated both forward and backward in time, two independent drift vector estimates are reported for each analysis window: `eastward_sea_ice_velocity`/`northward_sea_ice_velocity` from the forward correlation, with its corresponding `correlation_coefficient`, and `eastward_sea_ice_velocity_alternative`/`northward_sea_ice_velocity_alternative` from the backward correlation, with `correlation_coefficient_alternative`.
This cross-correlation method is blind to the actual presence or absence of sea ice in the analysis window; a high correlation coefficient together with good agreement between the forward and backward drift vectors is therefore used as an indicator that sea ice, rather than open water or noise, was tracked.
As for the near-surface current and bathymetric maps, analysis locations are stored as points indexed by a flat `measurement` dimension rather than as coordinates on a regular `x`/`y` grid, since the underlying analysis windows are placed on an overlapping, approximately regular grid that follows the platform trajectory.

## Minimal example
```
netcdf or_2025-08-23-12_sea_ice_drift {
dimensions:
        measurement = 23406 ;
variables:
        char trajectory ;
                trajectory:cf_role = "trajectory_id" ;
                trajectory:long_name = "Sea ice drift measurements along R/V Ocean Research trajectory" ;
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:authority_string = "EPSG:4326" ;
        double time(measurement) ;
                time:calendar = "standard" ;
                time:long_name = "start time of current measurement" ;
                time:standard_name = "time" ;
                time:units = "days since 2025-01-01T00:00:00Z" ;
        double longitude(measurement) ;
                longitude:long_name = "center longitude of current measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
                longitude:grid_mapping = "crs" ;
        double latitude(measurement) ;
                latitude:long_name = "center latitude of current measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
                latitude:grid_mapping = "crs" ;
        double eastward_sea_ice_velocity(measurement) ;
                eastward_sea_ice_velocity:long_name = "eastward component of the sea ice velocity from forward cross correlation" ;
                eastward_sea_ice_velocity:standard_name = "eastward_sea_ice_velocity" ;
                eastward_sea_ice_velocity:units = "m s-1" ;
        double northward_sea_ice_velocity(measurement) ;
                northward_sea_ice_velocity:long_name = "northward component of the sea ice velocity from forward cross correlation" ;
                northward_sea_ice_velocity:standard_name = "northward_sea_ice_velocity" ;
                northward_sea_ice_velocity:units = "m s-1" ;
        double correlation_coefficient(measurement) ;
                correlation_coefficient:long_name = "maximum Pearson coefficient from forward cross correlation" ;
                correlation_coefficient:units = "1" ;
        double eastward_sea_ice_velocity_alternative(measurement) ;
                eastward_sea_ice_velocity_alternative:long_name = "eastward component of the sea ice velocity from backward cross correlation" ;
                eastward_sea_ice_velocity_alternative:units = "m s-1" ;
        double northward_sea_ice_velocity_alternative(measurement) ;
                northward_sea_ice_velocity_alternative:long_name = "northward component of the sea ice velocity from backward cross correlation" ;
                northward_sea_ice_velocity_alternative:units = "m s-1" ;
        double correlation_coefficient_alternative(measurement) ;
                correlation_coefficient_alternative:long_name = "maximum Pearson coefficient from backward cross correlation" ;
                correlation_coefficient_alternative:units = "1" ;
        ubyte measurement_quality(measurement) ;
                measurement_quality:long_name = "measurement quality (0: good, 1-7: bad)" ;
                measurement_quality:flag_meanings = "good_quality forward_and_backward_cross_correlation_results_too_different sea_ice_speed_to_high correlation_coefficient_too_low" ;
                measurement_quality:flag_values = 0UB, 1UB, 2UB, 4UB ;
                measurement_quality:standard_name = "quality_flag" ;

// global attributes:
                :title = "Marine X-band radar sea ice drift measurements with quality control flag from R/V Ocean Research" ;
                :comment = "The sea ice drift vectors are obtained through cross correlation of pairs of 30.0 s averaged radar backscatter intensity images separated by 90.0 s. The images are partitioned into analysis windows where all pixels outside of the circles that are inscribed in the analysis windows are set to zero. The locations of the Pearson correlation coefficient peaks from two-dimensional sliding window correlations forward and backward in time yield two sea ice drift vectors per analysis window. This method is blind to the presence or absence of sea ice within the analysis window. A good indicator for the presence of sea ice are high correlation coefficients (>0.75) and a good agreement between the two sea ice drift vectors (magnitude of vector difference <0.1 m s-1). The resulting sea ice drift maps have a fixed latitude spacing and a longitude spacing that is updated within 1-degree latitude bands to ensure an approximately constant grid resolution. Analysis windows with a spatiotemporal data coverage of <90.0% are disregarded. Segments of the radar field of view that are obstructed by platform superstructures are also disregarded." ;
                :contact = "famous.scientist@frori.org" ;
                :Conventions = "CF-1.13 SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :featureType = "trajectory" ;
}
```