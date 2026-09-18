---
title: Regularized polar images
layout: default
parent: Level 1 data
nav_order: 2
---

# Regularized polar images

Here we refer to Level 1b data in polar form: individual radar images, one per antenna revolution, kept in polar (range, azimuth) coordinates with a regularized azimuth axis.
Values remain uncalibrated and are not averaged in time or range; only the azimuth axis changes relative to [Level 1a](level1a.md).

A SOMaR NetCDF file with Level 1b polar images is structured like a Level 1a file, with the same range axis, azimuth definition, and uncalibrated units, except that the irregularly spaced pulse azimuths are resampled onto a regular `azimuth` grid.
Each time step then represents one complete antenna revolution, and the data variable has the dimensions `(time, azimuth, range)`.
The azimuth is given relative to the radar's "0" angle, as in Level 1a, and is not necessarily north-oriented.
Because the values are no longer individual pulses, they can generally not be stored as integers with a `scale_factor`; `float` is recommended unless the method is `"nearest_neighbor"`.

The resampling method is recorded in the `azimuth_regularization` attribute of the data variable, which must be one of:

| Value | Description |
|---|---|
| `"nearest_neighbor"` | Each azimuth bin takes the pulse closest in azimuth. |
| `"linear_interpolation"` | Each azimuth bin is linearly interpolated between the two adjacent pulses. |
| `"average"` | Each azimuth bin is the mean of all pulses falling within it. |

The `comment` attribute should describe the method in words.
`time` gives the start time of each revolution, and `pulse_time` gives the acquisition time represented by each azimuth bin, i.e. the time of the selected pulse, the correspondingly interpolated time, or the mean time of the averaged pulses.

## Minimal example
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
                azimuth:standard_name = "sensor_azimuth_angle" ;
                azimuth:long_name = "radar antenna pointing direction on regular grid" ;
                azimuth:comment = "clockwise positive, not North-oriented" ;
        float range(range) ;
                range:units = "meters" ;
                range:long_name = "slant_range" ;
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
                :Conventions = "CF-1.13 SOMaR-0.5-draft" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :title = "Bare minimum level 1b polar X-band radar data example" ;
                :source = "ground-based radar" ;
                :history = "20230831T170026Z: File creation time" ;
                :originator = "Dr. Famous Scientist" ;
                :contact = "famous.scientist@frori.org" ;
                :crs = "Polar local sensor coordinates" ;
}
```
