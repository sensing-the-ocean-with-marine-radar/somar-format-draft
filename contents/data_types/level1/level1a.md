---
title: Level 1a data
layout: default
parent: Level 1 Products
#nav_order: 2
---

# Level 1a data products

A SOMaR NetCDF file at Level 1a originates directly from the data recorded by the radar system used (Level 0).
It can therefore still be considered "raw" radar data, but stored as NetCDF rather than in the often proprietary radar data containers used by different manufacturers.
This ensures interoperability even when different radar systems are used.
No changes to the data, other than this format conversion, are allowed.
In particular, Level 1a data should contain all pulses without any interpolation or pulse averaging.
The primary axis is time and should, if possible, be given as an absolute timestamp in UNIX time (seconds from 1970-01-01 00:00:00.000 UTC).
The secondary axes are the range bin number or slant range (or both) and azimuth angle (with respect to the radar's "0" angle which can be different from north).
The data itself are stored in the units of the radar's respective analog-to-digital converters.
Since the SOMaR format aims for full compliance with UDUNITS and CF, the `unit` variable must be `"1"` or `"dB"` to indicate linear or logarithmic dimensionless units.
It should therefore be clearly specified in the `comment` variable whether the unit refers to amplitude or power.

## 

## Minimal example:
```
{
dimensions:
        time = 39575 ;
        range = 435 ;
variables:
        double time(time) ;
                time:units = "seconds since 1970-01-01 00:00:00" ;
                time:standard_name = "time" ;
                time:long_name = "number of seconds (including fractional seconds) elapsed since 00:00:00 1-Jan-1970 UTC (Universal Coordinated Time), ignoring leap seconds" ;
        float azimuth(time) ;
                azimuth:units = "degrees" ;
                azimuth:standard_name = "sensor_azimuth_angle" ;
                azimuth:long_name = "radar antenna pointing direction" ;
                azimuth:comment = "clockwise positive, not North-oriented" ;
        float range(range) ;
                range:units = "meters" ;
                range:long_name = "slant_range" ;
        ushort polar_amp(time, range) ;
                polar_amp:scale_factor = 0.176738930567883 ;
                polar_amp:add_offset = 0. ;
                polar_amp:long_name = "radar_backscatter_amplitude" ;
                polar_amp:units = "1" ;
                polar_amp:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). I and Q are the in-phase and quadrature channels both measured in counts of the analog-to-digital-converter (ADC)." ;

// global attributes:
                :Conventions = "CF-1.10" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :title = "Bare minimum level 1a X-band radar data example" ;
                :source = "ground-based radar" ;
                :creation_date = "20230831T170026Z" ;
                :originator = "Dr. Famous Scientist" ;
                :contact = "famous.scientist@frori.org" ;
                :crs = "Polar local sensor coordinates" ;
}
```