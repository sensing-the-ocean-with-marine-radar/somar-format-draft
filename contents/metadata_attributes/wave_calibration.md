---
title: Wave calibration parameters
layout: default
parent: Metadata
nav_order: 6
---

# Wave calibration parameters

Two steps of the wave retrieval rely on empirical parameters, which differ between processors. They are recorded in a group named `wave_calibration` in the root group of every surface wave product ([wavenumber spectra](../product_types/level2/wave_wavenumber_spectra.md), [frequency-direction spectra](../product_types/level2/wave_frequency_direction_spectra.md), [frequency spectra](../product_types/level2/wave_frequency_spectra.md), and [wave parameters](../product_types/level2/wave_parameters.md)), so that the calibration can be reproduced from the file.

- The **modulation transfer function** M(k) converts the radar image spectrum into the uncalibrated wave energy density spectrum, which is the image spectrum divided by the squared magnitude of M(k). For the form `"power_law"`, that squared magnitude is proportional to k^β, where k is the wavenumber and β is given by `mtf_exponent`; a positive β thus reduces the energy at high wavenumbers.
- The **significant wave height calibration** converts the signal-to-noise ratio, i.e. the ratio of the `wave_signal` to the `background_noise` reported with the [wave parameters](../product_types/level2/wave_parameters.md), into the significant wave height: Hs = `hs_intercept` + `hs_slope` × P, where the predictor P named by `hs_predictor` is typically the square root of the signal-to-noise ratio.

| Variable | Values | Description |
|---|---|---|
| `hs_intercept`<br><small>SOMaR</small> | double; `m` | Intercept of the significant wave height calibration. |
| `hs_slope`<br><small>SOMaR</small> | double; `m` | Slope of the significant wave height calibration. |
| `hs_predictor`<br><small>SOMaR</small> | string; `"sqrt_signal_to_noise_ratio"`, `"signal_to_noise_ratio"`, or `"other"` | The quantity to which the slope and intercept are applied. |
| `mtf_form`<br><small>SOMaR</small> | string; `"power_law"`, `"none"`, or `"other"` | The form of the modulation transfer function. |
| `mtf_exponent`<br><small>SOMaR</small> | double; `1` | For `"power_law"`: the exponent β. Omitted otherwise. |
{: .variable-table }

A processor that uses a different predictor or a different form of the modulation transfer function sets the variable to `"other"` and describes its method in a `comment` attribute of that variable; a `references` attribute gives the underlying scientific literature.

The group carries the following attributes.

| Attribute | Values | Description |
|---|---|---|
| `calibration_date`<br><small>SOMaR</small> | String; ISO 8601 date | The date of the calibration. |
| `calibration_reference`<br><small>SOMaR</small> | String; free text | The reference wave data against which the calibration was derived. |
{: .attribute-table }

## Example

```
group: wave_calibration {
  variables:
        double hs_intercept ;
                hs_intercept:units = "m" ;
                hs_intercept:long_name = "intercept of the significant wave height calibration" ;
        double hs_slope ;
                hs_slope:units = "m" ;
                hs_slope:long_name = "slope of the significant wave height calibration" ;
        string hs_predictor ;
                hs_predictor:long_name = "quantity to which the significant wave height calibration is applied" ;
        string mtf_form ;
                mtf_form:long_name = "form of the modulation transfer function" ;
                mtf_form:references = "Nieto Borge, J. C., G. Rodriguez Rodriguez, K. Hessner, and P. Izquierdo Gonzalez (2004), Inversion of marine radar images for surface wave analysis, J. Atmos. Oceanic Technol., 21(8), 1291-1300, doi:10.1175/1520-0426(2004)021<1291:IOMRIF>2.0.CO;2" ;
        double mtf_exponent ;
                mtf_exponent:units = "1" ;
                mtf_exponent:long_name = "exponent of the power-law modulation transfer function" ;

  // group attributes:
                :calibration_reference = "MFWAM global wave data" ;
                :calibration_date = "2025-01-06" ;
  data:
        hs_intercept = 0.1 ;
        hs_slope = 1.5 ;
        hs_predictor = "sqrt_signal_to_noise_ratio" ;
        mtf_form = "power_law" ;
        mtf_exponent = 1.2 ;
  } // group wave_calibration
```
