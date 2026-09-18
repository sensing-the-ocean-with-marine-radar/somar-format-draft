---
title: Optional global attributes
layout: default
parent: Metadata attributes
nav_order: 2
---

# Optional global attributes

In addition to the [mandatory global attributes](mandatory_global.md), the following global attributes are recommended where applicable, since they aid data discovery and provenance tracking but are not required for a file to be a valid SOMaR product:

| Attribute | Example | Description |
|---|---|---|
| `comment` | `"The near-surface current vectors are obtained through least-squares fits that minimize the distance between the wave signal found in marine X-band radar backscatter intensity wavenumber frequency spectra and the linear ocean wave dispersion shell. ..."` | Free-text description of the retrieval method, processing parameters, and any caveats specific to the file's content; in practice, most SOMaR products carry a fairly detailed `comment`. |
| `platform` | `"R/V Ocean Research"` | The name of the vessel or platform the radar was mounted on. |
| `processing_software` | `"CSTARS X-band radar processing software version 2.5.0 written in Python 3.13.6"` | The name and version of the software (and its runtime) used to produce the file, to support reproducibility. |
| `institution_id` | `"https://ror.org/02dgjyy92"` | A persistent identifier for the institution, e.g. its [ROR](https://ror.org/) ID. |
| `licence` | `"Creative Commons Attribution 4.0 International Public License (CC BY 4.0)"` | The data usage licence under which the file is released. |
| `time_coverage_start` / `time_coverage_end` | `"2025-01-15T11:10:01.357666Z"` / `"2025-01-15T12:00:00.775429Z"` | The time of the first and the latest observation contributing to the data in the file, in ISO 8601 format in UTC. Fractional seconds (up to microsecond precision) are permitted and should be given where the source data provide them, so that `time_coverage_start` equals the start time of the first observation exactly. For products organized in time-bounded groups of fixed window length, `time_coverage_end` is the end of the last window, i.e. approximately the start time plus the number of groups times the window length (five 600 s groups starting at 11:10:01 end at approximately 12:00:01). |
| `geospatial_lat_min` / `geospatial_lat_max` | `14.9265` / `15.03` | The minimum and maximum latitude covered by the file's data, in degrees north. |
| `geospatial_lon_min` / `geospatial_lon_max` | `145.8426` / `145.96815` | The minimum and maximum longitude covered by the file's data, in degrees east. |

Individual products may additionally define their own product-specific optional global attributes, documented on the relevant product's own page rather than here — for example `sea_surface_wave_significant_height_calibration_status` on [Surface wave spectra and parameters](../data_types/level2/trajectory/surface_waves.md), or `wavenumber_bin_size` on the [near-surface current profile maps](../data_types/level2/gridded/current_maps.md).

