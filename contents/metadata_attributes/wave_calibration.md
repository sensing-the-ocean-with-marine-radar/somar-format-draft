---
title: Wave calibration parameters
layout: default
parent: Metadata
nav_order: 6
---

# Wave calibration parameters

Two steps of the wave retrieval rely on empirical parameters, which differ between processors. They are recorded in a group named `wave_calibration` in the root group of every surface wave product ([wavenumber spectra](../product_types/level2/wave_wavenumber_spectra.md), [frequency-direction spectra](../product_types/level2/wave_frequency_direction_spectra.md), [frequency spectra](../product_types/level2/wave_frequency_spectra.md), and [wave parameters](../product_types/level2/wave_parameters.md)), so that the calibration can be reproduced from the file.

- The **modulation transfer function** $M(k)$ converts the radar image spectrum into the uncalibrated wave energy density spectrum, which is the image spectrum divided by $\lvert M(k) \rvert^2$. For the form `"power_law"`, $\lvert M(k) \rvert^2 \propto k^{\beta}$, where $k$ is the wavenumber and $\beta$ is given by `mtf_exponent`; a positive $\beta$ thus reduces the energy at high wavenumbers relative to that at low wavenumbers (Nieto Borge et al. [2004](../references/index.md#nieto-borge-2004)).
- The **significant wave height calibration** converts the signal-to-noise ratio, i.e. the ratio of the `wave_signal` to the `background_noise` reported with the [wavenumber spectra](../product_types/level2/wave_wavenumber_spectra.md) and the [wave parameters](../product_types/level2/wave_parameters.md), into the significant wave height: $H_s = a + b\,P$, where $a$ is `hs_intercept`, $b$ is `hs_slope`, and the predictor $P$ is given by `hs_predictor` as an expression in `wave_signal` and `background_noise`, typically the square root of the signal-to-noise ratio, `sqrt(wave_signal / background_noise)` (Nieto-Borge et al. [2008](../references/index.md#nieto-borge-2008)).

| Variable | Values | Description |
|---|---|---|
| `hs_intercept`<br><small>SOMaR</small> | double; `m` | Intercept of the significant wave height calibration. |
| `hs_slope`<br><small>SOMaR</small> | double; `m` | Slope of the significant wave height calibration. |
| `hs_predictor`<br><small>SOMaR</small> | string; an expression in `wave_signal` and `background_noise` (see below), e.g. `"sqrt(wave_signal / background_noise)"` | The predictor $P$ to which the slope and intercept are applied. |
| `mtf_form`<br><small>SOMaR</small> | string; `"power_law"`, `"none"`, or a name chosen by the processor (see below) | The form of the modulation transfer function. |
| `mtf_exponent`<br><small>SOMaR</small> | double; `1` | For `"power_law"`: the exponent $\beta$. Omitted otherwise. |
{: .variable-table }

The expression in `hs_predictor` may contain the variable names `wave_signal` and `background_noise`, numbers, the operators `+`, `-`, `*`, and `/`, parentheses, and the functions `sqrt` and `log10`; a predictor that is the wave signal alone, for example, is written `"wave_signal"`.
In the wavenumber spectra and the wave parameters, which store `wave_signal` and `background_noise`, $P$ can thus be computed from the file; in the frequency-direction and frequency spectra, which do not, the expression documents the calibration of the wavenumber spectra they are derived from.

A form of the modulation transfer function other than `"power_law"` or `"none"` is named by the processor with a short lowercase name with underscores, e.g. `"power_law_with_cutoff"`, so that files using the same form can be recognized.
The `mtf_form` variable then carries a `comment` attribute describing the form, and its parameters are stored as further variables in the group whose names begin with `mtf_`.

For either variable, a `references` attribute gives the underlying scientific literature.

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
                hs_predictor:references = "Nieto-Borge, J. C., K. Hessner, P. Jarabo-Amores, and D. de la Mata-Moya (2008), Signal-to-noise ratio analysis to estimate ocean wave heights from X-band marine radar image time series, IET Radar Sonar Navig., 2(1), 35-41, doi:10.1049/iet-rsn:20070027" ;
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
        hs_predictor = "sqrt(wave_signal / background_noise)" ;
        mtf_form = "power_law" ;
        mtf_exponent = 1.2 ;
  } // group wave_calibration
```
