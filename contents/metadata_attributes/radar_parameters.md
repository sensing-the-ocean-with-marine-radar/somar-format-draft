---
title: Radar parameters
layout: default
parent: Metadata attributes
nav_order: 4
---

# Radar Parameters/Calibration Group

SOMaR files currently describe the radar instrument itself through two global attributes, `instrument` (see [Optional global attributes](optional_global.md)) and `source` (see [Mandatory global attributes](mandatory_global.md)):

| Attribute | Defined by | Values | Description | Example |
|---|---|---|---|---|
| `instrument` | [ACDD](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3) | String; free text | The manufacturer, model, and/or type of the radar system used, including relevant technical detail such as whether the receiver is coherent. | `"Helmholtz-Zentrum Hereon coherent-on-receive marine X-band radar"` |
| `source` | [CF](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents) | String; free text | The general method of production, e.g. platform and sensor type. | `"Shipboard marine X-band radar"` |
{: .attribute-table }

Beyond these two descriptive attributes, the main radar-specific calibration information currently defined by SOMaR concerns the conversion of a data variable from raw analog-to-digital converter (ADC) counts to a physically meaningful, still-uncalibrated quantity. As introduced in [Level 1a data](../data_types/level1/level1a.md), such variables use the standard CF/UDUNITS `scale_factor` and `add_offset` attributes together with `units = "1"` or `units = "dB"`, and must state in a `comment` attribute whether the stored quantity is an amplitude or a power:

```
ushort polar_amp(time, range) ;
        polar_amp:scale_factor = 0.176738930567883 ;
        polar_amp:add_offset = 0. ;
        polar_amp:long_name = "radar_backscatter_amplitude" ;
        polar_amp:units = "1" ;
        polar_amp:comment = "the square root of (I^2 + Q^2) given in uncalibrated analog-to-digital units (ADU). I and Q are the in-phase and quadrature channels both measured in counts of the analog-to-digital-converter (ADC)." ;
```

Data variables in [Level 1b polar images](../data_types/level1/level1b.md#polar-image-sequences-pol3d), whose irregular pulse azimuths have been resampled onto a regular azimuth grid, additionally carry a variable attribute recording how this was done:

| Attribute | Defined by | Values | Description | Example |
|---|---|---|---|---|
| `azimuth_regularization` | SOMaR | String; one of `nearest_neighbor`, `linear_interpolation`, `average` | The method used to resample pulses recorded at irregular azimuths onto the regular `azimuth` axis: selection of the closest pulse, linear interpolation between the two adjacent pulses, or the mean of all pulses falling within each azimuth bin. Should be accompanied by a `comment` describing the method in words. | `"nearest_neighbor"` |
{: .attribute-table }

Several Level 2 products go further, deriving physically calibrated quantities (e.g. significant wave height, current velocity, water depth) from the radar signal using retrieval-specific calibration parameters — for example, the `summary` attributes of the wave and current products reference an "empirical modulation transfer function" and "radar specific calibration parameters" used internally during processing. These parameters are not yet exposed as their own NetCDF attributes or a dedicated calibration group in current SOMaR output; formalizing how such retrieval-calibration parameters should be recorded (for example, in a dedicated `radar_parameters`/calibration NetCDF group, as this section's heading anticipates) is an open item for a future revision of the format rather than an established convention today.
