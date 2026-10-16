---
title: Optional global attributes
layout: default
parent: Metadata
nav_order: 2
---

# Optional global attributes

In addition to the [mandatory global attributes](mandatory_global.md), the following global attributes are recommended where applicable, since they aid data discovery and provenance tracking but are not required for a file to be a valid SOMaR product.

| Attribute | Values | Description |
|---|---|---|
| `creator_email`<br><small>[ACDD][acdd]</small> | String; email address | An email address for questions about the file's content. |
| `creator_name`<br><small>[ACDD][acdd]</small> | String; free text | The name of the person or group principally responsible for creating the file. |
| `date_created`<br><small>[ACDD][acdd]</small> | String; ISO 8601 date and time in UTC | The date on which this version of the data was created. It must agree with the creation time recorded in `history`; changes to metadata alone do not alter it. |
| `geospatial_lat_max`<br><small>[ACDD][acdd]</small> | Number; degrees north | The northernmost latitude covered by the file's data. |
| `geospatial_lat_min`<br><small>[ACDD][acdd]</small> | Number; degrees north | The southernmost latitude covered by the file's data. |
| `geospatial_lon_max`<br><small>[ACDD][acdd]</small> | Number; degrees east | The easternmost longitude covered by the file's data. |
| `geospatial_lon_min`<br><small>[ACDD][acdd]</small> | Number; degrees east | The westernmost longitude covered by the file's data. |
| `history`<br><small>[CF][cf-description]</small> | String; one entry per processing step, each starting with a UTC timestamp | A record of the file's provenance, at minimum its creation time. Later entries (e.g. reprocessing) are appended to this attribute rather than overwriting it. |
| `institution`<br><small>[CF][cf-description]</small> | String; free text | The institution responsible for producing the file. |
| `institution_id`<br><small>SOMaR</small> | String; URI | A persistent identifier for the institution named in `institution`, e.g. its [ROR](https://ror.org/) ID. |
| `instrument`<br><small>[ACDD][acdd]</small> | String; free text | The manufacturer, model, and/or type of the radar system used, including relevant technical detail such as whether the receiver is coherent. |
| `license`<br><small>[ACDD][acdd]</small> | String; URL or free text | The data usage license under which the file is released. |
| `platform`<br><small>[ACDD][acdd]</small> | String; free text | The name of the vessel or platform the radar was mounted on. |
| `platform_is_mobile`<br><small>[FM 301][fm301], Table 301-1</small> | String; `true` or `false` | Whether the platform moves. FM 301 allows only `false`; SOMaR also allows `true`. In polar products (Level 1a and Level 1b polar), `true` requires the position and heading of the platform for every sweep or every pulse (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)). Assumed `false` if missing. |
| `processing_level`<br><small>[ACDD][acdd]</small> | String; one of `L1a`, `L1b`, `L2a`, `L2b` | The SOMaR processing level of the file's content (see [SOMaR product types](../product_types/index.md)). ACDD allows free text here; SOMaR restricts it to these codes. |
| `processing_software`<br><small>SOMaR</small> | String; free text | The name and version of the software used to produce the file, to support reproducibility. |
| `source`<br><small>[CF][cf-description]</small> | String; free text | The method of production of the underlying data, e.g. the type of platform and sensor. |
| `summary`<br><small>[ACDD][acdd]</small> | String; free text | A paragraph describing the file's content, analogous to an abstract: the retrieval method, processing parameters, and any caveats. |
| `time_coverage_end`<br><small>[ACDD][acdd]</small> | String; ISO 8601 date and time in UTC, fractional seconds permitted | The time of the latest observation contributing to the data in the file. For products organized in time-bounded groups of fixed window length, this is the end of the last window. |
| `time_coverage_start`<br><small>[ACDD][acdd]</small> | String; ISO 8601 date and time in UTC, fractional seconds permitted | The time of the first observation contributing to the data in the file. |
| `title`<br><small>[CF][cf-description]</small> | String; free text | A short, human-readable description of the file's content. |
{: .attribute-table }

## Example

The global attributes of a [near-surface current map](../product_types/level2/current_maps.md) file, with the mandatory and optional attributes:

```
// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "currents" ;
                :creator_email = "famous.scientist@frori.org" ;
                :creator_name = "Dr. Famous Scientist" ;
                :date_created = "2025-01-15T12:05:00Z" ;
                :geospatial_lat_max = 15.03 ;
                :geospatial_lat_min = 14.9265 ;
                :geospatial_lon_max = 145.96815 ;
                :geospatial_lon_min = 145.8426 ;
                :history = "20250115T120500Z: File creation time" ;
                :institution = "Famous Radar Ocean Research Institute" ;
                :institution_id = "https://ror.org/01abcde23" ;
                :instrument = "Famous Radar Ocean Research Institute coherent-on-receive marine X-band radar" ;
                :license = "Creative Commons Attribution 4.0 International Public License (CC BY 4.0)" ;
                :platform = "R/V Ocean Research" ;
                :platform_is_mobile = "true" ;
                :processing_level = "L2a" ;
                :processing_software = "FRORI X-band radar processing software version 2.5.0 (Python 3.13.6)" ;
                :source = "Shipboard marine X-band radar" ;
                :summary = "The near-surface current vectors are obtained through least-squares fits ..." ;
                :time_coverage_end = "2025-01-15T12:00:00.775429Z" ;
                :time_coverage_start = "2025-01-15T11:00:31.417000Z" ;
                :title = "Marine X-band radar near-surface current measurements with quality control flag from R/V Ocean Research" ;
```

[cf-description]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents
[acdd]: https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
