---
title: Relative roughness images (L2a)
layout: default
parent: "Annex: Example products"
nav_order: 4
---

# L2a: Relative roughness images

{: .informative }
> This page is informative. The product type `relative_roughness` is one of the [gridded products](../product_types/gridded.md#product-types), whose page defines the structure and variables that a file of this product holds; the variables are defined under [Product variables](../metadata_attributes/product_variables.md).

Relative roughness images (`relative_roughness`) provide temporally averaged relative sea surface roughness, derived from Level 1b Cartesian backscatter images averaged over a short time window (typically tens of seconds) to reduce speckle noise.
Because the platform continues to move during this averaging window, and because the local grid origin and extent may change from one averaging window to the next, each averaging window is mapped onto its own time-bounded local grid; all grids of one file, typically covering one hour of a platform trajectory, are stored as sibling groups.
Within each group, `relative_roughness` gives the averaged, still uncalibrated radar backscatter power, and `number_of_observations` records how many Level 1b images contributed to each grid cell.

## Example

```
netcdf or_2025-01-15-11_relative_roughness {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :averaging_duration = 30. ; // recommended
                :geospatial_lat_max = 14.99528 ; // recommended
                :geospatial_lat_min = 14.95348 ; // recommended
                :geospatial_lon_max = 145.94251 ; // recommended
                :geospatial_lon_min = 145.86816 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ; // highly recommended
                :platform_is_mobile = "true" ; // required: the platform moves
                :product_type = "relative_roughness" ;
                :summary = "Sea surface roughness from a marine X-band radar on board R/V Ocean Research: Cartesian backscatter images averaged over 30 s windows to reduce speckle noise, each window on its own local grid." ; // highly recommended
                :time_coverage_end = "2025-01-15T11:59:59Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:00Z" ; // recommended
                :title = "Marine X-band radar sea surface relative roughness images from R/V Ocean Research" ; // highly recommended

group: time_20250115110031 {
  dimensions:
        y = 1988 ;
        x = 1898 ;
  variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 145.868167860183 ;
                crs:latitude_of_projection_origin = 14.9952749946079 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
                time:time_iso_8601 = "2025-01-15T11:00:31.417000Z" ; // optional
        double x(x) ;
                x:long_name = "eastward distance from radar position at measurement start time" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from radar position at measurement start time" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        float relative_roughness(y, x) ;
                relative_roughness:long_name = "temporally averaged radar backscatter power in uncalibrated analog-to-digital converter units" ;
                relative_roughness:units = "1" ;
                relative_roughness:grid_mapping = "crs" ;
                relative_roughness:coordinates = "time" ;
                relative_roughness:cell_methods = "time: mean" ;
                relative_roughness:ancillary_variables = "number_of_observations" ;
        int number_of_observations(y, x) ; // optional
                number_of_observations:standard_name = "number_of_observations" ;
                number_of_observations:long_name = "number of measurements from which the radar backscatter power averages have been derived" ;
                number_of_observations:units = "1" ;
                number_of_observations:grid_mapping = "crs" ;
  } // group time_20250115110031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per averaging window ...
}
```
