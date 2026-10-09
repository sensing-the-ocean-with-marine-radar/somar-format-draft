---
title: Polar/Cartesian image sequences (L1b)
layout: default
parent: Level 1 data
nav_order: 2
---

# L1b: Radar image sequences

## Polar image sequences (pol3d)

Here we refer to Level 1b data in polar form: radar image sequences, kept in polar (range, azimuth) coordinates but mapped to a regularized range and azimuth axis, such that every individual image in the sequence shares the same range and azimuth grid.

A SOMaR NetCDF file with Level 1b polar images mostly originates from Level 1a (or Level 0) data.
Each time step represents one complete antenna revolution to form the individual image.
The data variable has the dimensions `(time, azimuth, range)`, and reflects uncalibrated amplitude (or power) data.  


One image corresponds to one sweep of the [Level 1a](level1a.md) data.
The `range` and `azimuth` variables carry the same attributes as at Level 1a, which are taken from the WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes).
As at Level 1a, the azimuth is given relative to the radar's zero direction and is not necessarily north-oriented; it is related to true north through the platform `heading` and the `azimuth_correction` (see [Georeferencing](../../metadata_attributes/georeferencing.md#polar-sensor-coordinates)).
The image cube with the dimensions `(time, azimuth, range)` has no equivalent in FM 301, which keeps the individual rays of each sweep, and is specific to SOMaR.

The spacing of the regular azimuth axis is recorded in the `rays_angle_resolution` attribute of `azimuth`, in degrees. The name is that of the FM 301 variable `rays_angle_resolution`, which gives the angular spacing of rays that are indexed to a regular grid.

The resampling method is recorded in the `azimuth_regularization` attribute of the data variable, which must be one of:

| Value | Description |
|---|---|
| `"nearest_neighbor"` | Each azimuth bin takes the pulse closest in azimuth. |
| `"linear_interpolation"` | Each azimuth bin is linearly interpolated between the two adjacent pulses. |
| `"average"` | Each azimuth bin is the mean of all pulses falling within it. |

The `comment` attribute should describe the method in words.
`time` gives the start time of each revolution. 

<!---and `pulse_time` gives the acquisition time represented by each azimuth bin, i.e. the time of the selected pulse, the correspondingly interpolated time, or the mean time of the averaged pulses.-->

## Minimal example (NEEDS TO BE ADAPTED!!!)
```
{
dimensions:
        time = 41 ;
        azimuth = 1440 ;
        range = 435 ;
variables:
        double time(time) ;
                time:units = "seconds since 1970-01-01 00:00:00" ;
                time:standard_name = "time" ;
                time:long_name = "start time of radar measurement" ;
        float azimuth(azimuth) ;
                azimuth:units = "degrees" ;
                azimuth:long_name = "radar antenna pointing direction on regular grid" ;
                azimuth:rays_angle_resolution = 0.25f ;
                azimuth:comment = "clockwise positive, relative to the radar heading marker, not North-oriented" ;
        float range(range) ;
                range:units = "metres" ;
                range:long_name = "range_to_measurement_volume" ;
                range:spacing_is_constant = "true" ;
                range:meters_to_center_of_first_gate = 3.75f ;
                range:meters_between_gates = 7.5f ;
        double pulse_time(time, azimuth) ;
                pulse_time:units = "seconds since 1970-01-01 00:00:00" ;
                pulse_time:long_name = "radar pulse time" ;
                pulse_time:comment = "acquisition time represented by each azimuth bin" ;
        float polar_amp(time, azimuth, range) ;
                polar_amp:long_name = "radar_backscatter_amplitude" ;
                polar_amp:units = "1" ;
                polar_amp:azimuth_regularization = "nearest_neighbor" ;
                polar_amp:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). Pulses recorded at irregular azimuths were regularized onto the azimuth grid by nearest-neighbor selection." ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :title = "Bare minimum level 1b polar X-band radar data example" ;
                :source = "ground-based radar" ;
                :history = "20230831T170026Z: File creation time" ;
                :creator_name = "Dr. Famous Scientist" ;
                :creator_email = "famous.scientist@frori.org" ;
                :processing_level = "L1b" ;
}
```

## Cartesian image sequences (cart3d)

Here we refer to Level 1b data in Cartesian form: individual radar images, one per antenna revolution, mapped from polar coordinates onto a local Cartesian grid centered on the platform.

A SOMaR NetCDF file at Level 1b contains individual radar images that have been mapped from the sensor's native polar (range, azimuth) geometry onto a Cartesian grid, while otherwise remaining as close as possible to the underlying Level 1a raw data.
Unlike Level 1a, where the primary axis is time and pulses are stored individually, Level 1b images represent one complete antenna revolution per time step, reprojected onto a regular Cartesian `x`/`y` grid.
The grid is defined in a local, radar-centric coordinate system whose origin is given by the platform's `longitude`/`latitude` at the start of each scan; this is an instance of the time-bounded local grid concept introduced in the [Introduction](../../introduction/index.md), since the grid origin moves with the platform from one image to the next.
Grid cells that fall outside the calibrated field of view, for example those obstructed by platform superstructure, are blanked.
Because each image pixel is acquired at a slightly different time as the antenna rotates, the acquisition time of a given pixel can, if needed, be approximated from the `pulse_azimuth` and `pulse_time` variables, which record the azimuth and acquisition time of each individual radar pulse contributing to the image.
As at Level 1a, values are stored in uncalibrated analog-to-digital converter units and are therefore dimensionless (`units = "1"`); no radiometric calibration or temporal averaging is applied at this level.

## Minimal example
```
netcdf or_2025-01-15-11-00_single_scan_sea_surface_roughness {
dimensions:
        time = 41 ;
        y = 1980 ;
        x = 1980 ;
        pulse_azimuth = 1440 ;
variables:
        char trajectory ;
                trajectory:cf_role = "trajectory_id" ;
                trajectory:long_name = "radar backscatter intensity measurements along R/V Ocean Research trajectory" ;
        char crs ;
                crs:grid_mapping_name = "latitude_longitude" ;
                crs:longitude_of_prime_meridian = 0. ;
                crs:semi_major_axis = 6378137. ;
                crs:inverse_flattening = 298.257223563 ;
                crs:authority_string = "EPSG:4326" ;
        double time(time) ;
                time:calendar = "standard" ;
                time:long_name = "start time of radar measurement" ;
                time:standard_name = "time" ;
                time:units = "days since 2025-01-01T00:00:00Z" ;
        double longitude(time) ;
                longitude:long_name = "longitude" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
                longitude:grid_mapping = "crs" ;
        double latitude(time) ;
                latitude:long_name = "latitude" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
                latitude:grid_mapping = "crs" ;
        double x(x) ;
                x:long_name = "distance from radar along grid x-axis at measurement start time for each image" ;
                x:standard_name = "projection_x_coordinate" ;
                x:units = "m" ;
        double y(y) ;
                y:long_name = "distance from radar along grid y-axis at measurement start time for each image" ;
                y:standard_name = "projection_y_coordinate" ;
                y:units = "m" ;
        float radar_backscatter_intensity(time, y, x) ;
                radar_backscatter_intensity:long_name = "radar backscatter intensity in uncalibrated analog-to-digital converter units" ;
                radar_backscatter_intensity:units = "1" ;
                radar_backscatter_intensity:grid_mapping = "crs" ;
        double pulse_azimuth(pulse_azimuth) ;
                pulse_azimuth:long_name = "radar pulse azimuth (clockwise with respect to north)" ;
                pulse_azimuth:units = "degrees" ;
        double pulse_time(time, pulse_azimuth) ;
                pulse_time:calendar = "standard" ;
                pulse_time:long_name = "radar pulse time" ;
                pulse_time:units = "days since 2025-01-01T00:00:00Z" ;

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :title = "Marine X-band radar backscatter intensity images from R/V Ocean Research" ;
                :source = "Shipboard marine X-band radar" ;
                :creator_name = "Dr. Famous Scientist" ;
                :creator_email = "famous.scientist@frori.org" ;
                :summary = "The marine X-band radar backscatter intensity images are corrected for ship motion. Segments of the radar field of view that are obstructed by platform superstructures are blanked. The origin of the coordinate system is given by (longitude, latitude), which corresponds to the radar location at the measurement start time for each image. The approximate time of measurement for each image pixel can be inferred from the pulse_time variable." ;
                :featureType = "trajectory" ;
                :history = "20250115T120500Z: File creation time" ;
                :processing_level = "L1b" ;
}
```