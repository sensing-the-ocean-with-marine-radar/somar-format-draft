---
title: Relative roughness images (L2a)
layout: default
parent: "Annex: Examples"
nav_order: 5
---

# L2a: Relative roughness images

{: .informative }
> An example of the product type `relative_roughness`, of the data type [`gridded_pixels`](../data_types/gridded_pixels.md), which defines its structure and variables (see [Annex: Examples](index.md)).

Relative roughness images (product type `relative_roughness`) provide temporally averaged relative sea surface roughness, derived from Level 1b Cartesian backscatter images averaged over a short averaging period (typically tens of seconds) to reduce speckle noise.
Because the platform continues to move during this averaging period, and because the local grid origin and extent may change from one averaging period to the next, each averaging period is mapped onto its own time-bounded local grid; all grids of one file, typically covering one hour of a platform trajectory, are stored as sibling groups.
From a fixed platform, the grid does not change, and all averaging periods of a file share a single grid.
Within each grid, [`relative_roughness`](../data_types/product_variables.md#relative_roughness) gives the averaged, still uncalibrated radar backscatter amplitude, which the examples average instead of power to give less weight to sea spikes (the quantity averaged is stated by [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity)), and [`number_of_observations`](../data_types/product_variables.md#number_of_observations) records how many Level 1b images contributed to each grid cell.

## File contents

**Layout.** On a moving platform, the file holds one [time-bounded grid](../georeferencing/index.md#time-bounded-grids) per averaging period, each in a `time_<YYYYMMDDHHMMSS>` group; on a fixed platform, it holds one [single grid](../georeferencing/index.md#single-grid) in the root group, with the leading dimension [`time`](../data_types/gridded_pixels.md#time). Each grid is the [local grid](../georeferencing/index.md#local-grid) `(y, x)`.

| Item | Tier | Condition |
|---|---|---|
| **Global attributes** | | |
| [`Conventions`](../metadata_attributes/mandatory_global.md#Conventions), [`data_type`](../metadata_attributes/mandatory_global.md#data_type) `= "gridded_pixels"` | Required | |
| [`product_type`](../metadata_attributes/optional_global.md#product_type) `= "relative_roughness"` | Recommended | |
| [`platform_is_mobile`](../metadata_attributes/mandatory_global.md#platform_is_mobile) `= "true"` | Required | moving platform |
| [`platform_is_mobile`](../metadata_attributes/mandatory_global.md#platform_is_mobile) `= "false"` | Required | fixed platform |
| [`keywords`](../metadata_attributes/optional_global.md#keywords), [`summary`](../metadata_attributes/optional_global.md#summary), [`title`](../metadata_attributes/optional_global.md#title) | Highly recommended | |
| the other [recommended global attributes](../metadata_attributes/optional_global.md#recommended) | Recommended | |
| [`averaging_duration`](../metadata_attributes/processing_parameters.md#averaging_duration) | Recommended | |
| **Variables of each grid** | | |
| [`time`](../data_types/gridded_pixels.md#time) | Required | |
| [`time_iso_8601`](../metadata_attributes/variable_attributes.md#time_iso_8601) on `time` | Optional | time-bounded grid |
| [`time_bounds`](../data_types/gridded_pixels.md#time_bounds) | Optional | |
| [`x`](../data_types/gridded_pixels.md#x), [`y`](../data_types/gridded_pixels.md#y), [`crs`](../data_types/gridded_pixels.md#crs) | Required | |
| [`relative_roughness`](../data_types/product_variables.md#relative_roughness) | Required | |
| [`cell_methods`](../metadata_attributes/variable_attributes.md#cell_methods) `= "time: mean"`, [`averaged_quantity`](../metadata_attributes/variable_attributes.md#averaged_quantity), and [`coordinates`](../metadata_attributes/variable_attributes.md#coordinates) `= "time"` on `relative_roughness` | Required | |
| [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) `= "crs"` on the data variables | Required | |
| [`number_of_observations`](../data_types/product_variables.md#number_of_observations) | Optional | |
{: .contents-table }

## Example

A radar on a moving platform.

```
netcdf or_2025-01-15-11_relative_roughness {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :data_type = "gridded_pixels" ;
                :geospatial_lat_max = 14.99528 ; // recommended
                :geospatial_lat_min = 14.95348 ; // recommended
                :geospatial_lon_max = 145.94251 ; // recommended
                :geospatial_lon_min = 145.86816 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ; // highly recommended
                :platform_is_mobile = "true" ;
                :product_type = "relative_roughness" ; // recommended
                :summary = "Sea surface roughness from a marine X-band radar on board R/V Ocean Research: Cartesian backscatter images averaged over 30 s windows to reduce speckle noise, each window on its own local grid." ; // highly recommended
                :time_coverage_end = "2025-01-15T12:00:31.417000Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:31.417000Z" ; // recommended
                :title = "Marine X-band radar sea surface relative roughness images from R/V Ocean Research" ; // highly recommended
                :averaging_duration = 30. ; // recommended

group: time_20250115110031 {
  dimensions:
        y = 1000 ;
        x = 1000 ;
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
                relative_roughness:long_name = "temporally averaged radar backscatter amplitude in uncalibrated analog-to-digital converter units" ;
                relative_roughness:units = "1" ;
                relative_roughness:grid_mapping = "crs" ;
                relative_roughness:coordinates = "time" ;
                relative_roughness:cell_methods = "time: mean" ;
                relative_roughness:averaged_quantity = "amplitude" ;
                relative_roughness:ancillary_variables = "number_of_observations" ;
        int number_of_observations(y, x) ; // optional
                number_of_observations:standard_name = "number_of_observations" ;
                number_of_observations:long_name = "number of measurements from which the radar backscatter amplitude averages have been derived" ;
                number_of_observations:units = "1" ;
                number_of_observations:grid_mapping = "crs" ;
  } // group time_20250115110031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per averaging period ...
}
```

## Example for a fixed platform

A radar on a fixed platform: all averaging periods share a [single grid](../georeferencing/index.md#single-grid) in the root group, with the leading dimension [`time`](../data_types/gridded_pixels.md#time), and the [`crs`](../data_types/gridded_pixels.md#crs) is centered on the radar antenna.

```
netcdf ors_2023-08-31-17_relative_roughness {
dimensions:
        time = 120 ;
        y = 1000 ;
        x = 1000 ;
variables:
        char crs ;
                crs:grid_mapping_name = "azimuthal_equidistant" ;
                crs:longitude_of_projection_origin = 7.8853 ;
                crs:latitude_of_projection_origin = 54.1826 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double x(x) ;
                x:long_name = "eastward distance from radar antenna" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "northward distance from radar antenna" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        float relative_roughness(time, y, x) ;
                relative_roughness:long_name = "temporally averaged radar backscatter amplitude in uncalibrated analog-to-digital converter units" ;
                relative_roughness:units = "1" ;
                relative_roughness:grid_mapping = "crs" ;
                relative_roughness:coordinates = "time" ;
                relative_roughness:cell_methods = "time: mean" ;
                relative_roughness:averaged_quantity = "amplitude" ;
                relative_roughness:ancillary_variables = "number_of_observations" ;
        int number_of_observations(time, y, x) ; // optional
                number_of_observations:standard_name = "number_of_observations" ;
                number_of_observations:long_name = "number of measurements from which the radar backscatter amplitude averages have been derived" ;
                number_of_observations:units = "1" ;
                number_of_observations:grid_mapping = "crs" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :data_type = "gridded_pixels" ;
                :geospatial_lat_max = 54.2185 ; // recommended
                :geospatial_lat_min = 54.1467 ; // recommended
                :geospatial_lon_max = 7.9467 ; // recommended
                :geospatial_lon_min = 7.8239 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ; // highly recommended
                :platform_is_mobile = "false" ;
                :product_type = "relative_roughness" ; // recommended
                :summary = "Sea surface roughness from a marine X-band radar at Ocean Research Station: Cartesian backscatter images averaged over 30 s windows to reduce speckle noise, all windows on one local grid centered on the radar antenna." ; // highly recommended
                :time_coverage_end = "2023-08-31T18:00:00Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar sea surface relative roughness images from Ocean Research Station" ; // highly recommended
                :averaging_duration = 30. ; // recommended
}
```

## Example for a rotated grid

A radar on a fixed platform at a coastal site, with the images on a [rotated local grid](../georeferencing/index.md#rotated-local-grids): its axes follow the convention of Argus and CIRN, [`x`](../data_types/gridded_pixels.md#x) cross-shore, positive offshore, and [`y`](../data_types/gridded_pixels.md#y) along-shore, at a coast whose offshore normal points to 110°, so that the azimuth of the y axis is 20°. The [`crs`](../data_types/gridded_pixels.md#crs) gives `grid_mapping_name = "rotated_azimuthal_equidistant"`, [`azimuth_of_y_axis`](../metadata_attributes/variable_attributes.md#azimuth_of_y_axis), and [`crs_wkt`](../metadata_attributes/variable_attributes.md#crs_wkt).

```
netcdf ors_2023-08-31-17_relative_roughness {
dimensions:
        time = 120 ;
        y = 1000 ;
        x = 1000 ;
variables:
        char crs ;
                crs:grid_mapping_name = "rotated_azimuthal_equidistant" ;
                crs:azimuth_of_y_axis = 20. ;
                crs:longitude_of_projection_origin = 7.8853 ;
                crs:latitude_of_projection_origin = 54.1826 ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:reference_ellipsoid_name = "WGS 84" ;
                crs:prime_meridian_name = "Greenwich" ;
                crs:horizontal_datum_name = "World Geodetic System 1984" ;
                crs:geographic_crs_name = "WGS 84" ;
                crs:crs_wkt = "DERIVEDPROJCRS[\"SOMaR rotated local grid\",",
                        "BASEPROJCRS[\"SOMaR local grid\",",
                        "BASEGEOGCRS[\"WGS 84\",DATUM[\"World Geodetic System 1984\",ELLIPSOID[\"WGS 84\",6378137,298.257223563,LENGTHUNIT[\"metre\",1]]],PRIMEM[\"Greenwich\",0,ANGLEUNIT[\"degree\",0.0174532925199433]]],",
                        "CONVERSION[\"Azimuthal equidistant\",METHOD[\"Azimuthal Equidistant\",ID[\"EPSG\",1125]],",
                        "PARAMETER[\"Latitude of natural origin\",54.1826,ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8801]],",
                        "PARAMETER[\"Longitude of natural origin\",7.8853,ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8802]],",
                        "PARAMETER[\"False easting\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8806]],",
                        "PARAMETER[\"False northing\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8807]]]],",
                        "DERIVINGCONVERSION[\"Rotation of the axes\",METHOD[\"Affine parametric transformation\",ID[\"EPSG\",9624]],",
                        "PARAMETER[\"A0\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8623]],",
                        "PARAMETER[\"A1\",0.939692620785908,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8624]],",
                        "PARAMETER[\"A2\",-0.342020143325669,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8625]],",
                        "PARAMETER[\"B0\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8639]],",
                        "PARAMETER[\"B1\",0.342020143325669,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8640]],",
                        "PARAMETER[\"B2\",0.939692620785908,SCALEUNIT[\"coefficient\",1],ID[\"EPSG\",8641]]],",
                        "CS[Cartesian,2],AXIS[\"(x)\",unspecified,ORDER[1],LENGTHUNIT[\"metre\",1]],AXIS[\"(y)\",unspecified,ORDER[2],LENGTHUNIT[\"metre\",1]]]" ;
                crs:comment = "Argus/CIRN axes: x cross-shore, positive offshore; y along-shore" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double x(x) ;
                x:long_name = "cross-shore distance from radar antenna, positive offshore" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "along-shore distance from radar antenna" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        float relative_roughness(time, y, x) ;
                relative_roughness:long_name = "temporally averaged radar backscatter amplitude in uncalibrated analog-to-digital converter units" ;
                relative_roughness:units = "1" ;
                relative_roughness:grid_mapping = "crs" ;
                relative_roughness:coordinates = "time" ;
                relative_roughness:cell_methods = "time: mean" ;
                relative_roughness:averaged_quantity = "amplitude" ;
                relative_roughness:ancillary_variables = "number_of_observations" ;
        int number_of_observations(time, y, x) ; // optional
                number_of_observations:standard_name = "number_of_observations" ;
                number_of_observations:long_name = "number of measurements from which the radar backscatter amplitude averages have been derived" ;
                number_of_observations:units = "1" ;
                number_of_observations:grid_mapping = "crs" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :data_type = "gridded_pixels" ;
                :geospatial_lat_max = 54.2185 ; // recommended
                :geospatial_lat_min = 54.1467 ; // recommended
                :geospatial_lon_max = 7.9467 ; // recommended
                :geospatial_lon_min = 7.8239 ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :keywords = "EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR BACKSCATTER, EARTH SCIENCE > SPECTRAL/ENGINEERING > RADAR > RADAR IMAGERY" ; // highly recommended
                :platform_is_mobile = "false" ;
                :product_type = "relative_roughness" ; // recommended
                :summary = "Sea surface roughness from a marine X-band radar at Ocean Research Station: Cartesian backscatter images averaged over 30 s windows to reduce speckle noise, all windows on one local grid centered on the radar antenna." ; // highly recommended
                :time_coverage_end = "2023-08-31T18:00:00Z" ; // recommended
                :time_coverage_start = "2023-08-31T17:00:00Z" ; // recommended
                :title = "Marine X-band radar sea surface relative roughness images from Ocean Research Station" ; // highly recommended
                :averaging_duration = 30. ; // recommended
}
```

