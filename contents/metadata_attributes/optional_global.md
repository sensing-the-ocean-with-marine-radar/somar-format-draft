---
title: Optional global attributes
layout: default
parent: Metadata attributes
nav_order: 2
---

# Optional global attributes

In addition to the [mandatory global attributes](mandatory_global.md), the following global attributes are recommended where applicable, since they aid data discovery and provenance tracking but are not required for a file to be a valid SOMaR product.

| Attribute | Defined by | Values | Description | Example |
|---|---|---|---|---|
| `summary` | [ACDD][acdd] | String; free text | A paragraph describing the file's content, analogous to an abstract: the retrieval method, processing parameters, and any caveats. In practice, most SOMaR products carry a fairly detailed `summary`. | `"The near-surface current vectors are obtained through least-squares fits that minimize the distance between the wave signal ... and the linear ocean wave dispersion shell. ..."` |
| `platform` | [ACDD][acdd] | String; free text | The name of the vessel or platform the radar was mounted on. | `"R/V Ocean Research"` |
| `instrument` | [ACDD][acdd] | String; free text | The manufacturer, model, and/or type of the radar system used (see [Radar parameters](radar_parameters.md)). | `"Helmholtz-Zentrum Hereon coherent-on-receive marine X-band radar"` |
| `processing_software` | SOMaR | String; free text | The name and version of the software (and its runtime) used to produce the file, to support reproducibility. | `"CSTARS X-band radar processing software version 2.5.0 written in Python 3.13.6"` |
| `institution_id` | SOMaR | String; URI | A persistent identifier for the institution named in `institution`, e.g. its [ROR](https://ror.org/) ID. | `"https://ror.org/02dgjyy92"` |
| `license` | [ACDD][acdd] | String; URL or free text | The data usage license under which the file is released. | `"Creative Commons Attribution 4.0 International Public License (CC BY 4.0)"` |
| `date_created` | [ACDD][acdd] | String; ISO 8601 date and time in UTC | The date on which this version of the data was created. It must agree with the creation time recorded in `history`; changes to metadata alone do not alter it. | `"2025-01-15T12:05:00Z"` |
| `time_coverage_start` | [ACDD][acdd] | String; ISO 8601 date and time in UTC, fractional seconds permitted | The time of the first observation contributing to the data in the file. Fractional seconds (up to microsecond precision) should be given where the source data provide them, so that the value equals the start time of the first observation exactly. | `"2025-01-15T11:10:01.357666Z"` |
| `time_coverage_end` | [ACDD][acdd] | String; ISO 8601 date and time in UTC, fractional seconds permitted | The time of the latest observation contributing to the data in the file. For products organized in time-bounded groups of fixed window length, this is the end of the last window, i.e. approximately the start time plus the number of groups times the window length (five 600 s groups starting at 11:10:01 end at approximately 12:00:01). | `"2025-01-15T12:00:00.775429Z"` |
| `geospatial_lat_min` | [ACDD][acdd] | Number; degrees north | The southernmost latitude covered by the file's data. | `14.9265` |
| `geospatial_lat_max` | [ACDD][acdd] | Number; degrees north | The northernmost latitude covered by the file's data. | `15.03` |
| `geospatial_lon_min` | [ACDD][acdd] | Number; degrees east | The westernmost longitude covered by the file's data. | `145.8426` |
| `geospatial_lon_max` | [ACDD][acdd] | Number; degrees east | The easternmost longitude covered by the file's data. | `145.96815` |

Individual products may additionally define their own product-specific optional global attributes, documented on the relevant product's own page rather than here — for example `sea_surface_wave_significant_height_calibration_status` on the [surface wave products](../data_types/level2/index.md), or `wavenumber_bin_size` on the [near-surface current profile maps](../data_types/level2/current_maps.md).

[acdd]: https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
