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
| `history`<br><small>[CF][cf-description]</small> | String; one entry per processing step, each starting with a UTC timestamp | A record of the file's provenance, at minimum its creation time. Later entries (e.g. reprocessing) are appended to this attribute rather than overwriting it. |
| `institution_id`<br><small>SOMaR</small> | String; URI | A persistent identifier for the institution named in `institution`, e.g. its [ROR](https://ror.org/) ID. |
| `instrument`<br><small>[ACDD][acdd]</small> | String; free text | The manufacturer, model, and/or type of the radar system used, including relevant technical detail such as whether the receiver is coherent. |
| `keywords`<br><small>[ACDD][acdd]</small> | String; comma-separated list | Keywords describing the file's content, preferably from a controlled vocabulary such as the [GCMD Science Keywords](https://www.earthdata.nasa.gov/data/tools/gcmd-keyword-viewer). |
| `keywords_vocabulary`<br><small>[ACDD][acdd]</small> | String; free text | The controlled vocabulary from which the `keywords` are taken, e.g. `GCMD Science Keywords`. |
| `license`<br><small>[ACDD][acdd]</small> | String; URL or free text | The data usage license under which the file is released. |
| `platform`<br><small>[ACDD][acdd]</small> | String; free text | The name of the vessel or platform the radar was mounted on. |
| `platform_is_mobile`<br><small>[FM 301][fm301], Table 301-1</small> | String; `true` or `false` | Whether the platform moves. FM 301 allows only `false`; SOMaR also allows `true`. In polar products (Level 1a and Level 1b polar), `true` requires the position and heading of the platform for every sweep or every ray (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)). Assumed `false` if missing. |
| `processing_level`<br><small>[ACDD][acdd]</small> | String; one of `L1a`, `L1b`, `L2a`, `L2b` | The SOMaR processing level of the file's content (see [SOMaR product types](../product_types/index.md)). ACDD allows free text here; SOMaR restricts it to these codes. |
| `processing_software`<br><small>SOMaR</small> | String; free text | The name and version of the software used to produce the file, to support reproducibility. |
| `project`<br><small>[ACDD][acdd]</small> | String; free text | The scientific project(s) under which the data were collected, comma-separated. |
| `source`<br><small>[CF][cf-description]</small> | String; free text | The method of production of the underlying data, e.g. the type of platform and sensor. |
| `standard_name_vocabulary`<br><small>[ACDD][acdd]</small> | String; e.g. `CF Standard Name Table v95` | The version of the CF standard name table from which the `standard_name` attributes are taken. The table is versioned separately from the CF conventions, so the CF version in `Conventions` does not identify it; if the attribute is missing, the table is the one SOMaR refers to (see [References](../references/index.md#cf-standard-names)). |
| `station_id`<br><small>SOMaR</small> | String; short, lowercase identifier | The identifier of the platform used as the prefix of the [file name](../file_naming/index.md), e.g. `or`. |
| `summary`<br><small>[ACDD][acdd]</small> | String; free text | A paragraph describing the file's content, analogous to an abstract: the retrieval method, processing parameters, and any caveats. |
{: .attribute-table }

## Processing parameters

The processing parameters needed to interpret the [roughness images](roughness_images.md), the [roughness image mosaics](roughness_mosaics.md), the [map products](#map-products), and the [wave products](#wave-products) are recorded in the following global attributes, in addition to the [shared global attributes](../../metadata_attributes/index.md).

| Attribute | Values | Description |
|---|---|---|
| `analysis_window_size`<br><small>SOMaR</small> | Number; `m` | Required for map and wave products. The diameter of the circular analysis windows. |
| `analysis_window_spacing`<br><small>SOMaR</small> | Number; `m` | Required for map products. The distance between the centers of neighboring analysis windows, i.e. the grid spacing of the map. |
| `averaging_duration`<br><small>SOMaR</small> | Number; `s` | Required for [roughness images](roughness_images.md), [roughness image mosaics](roughness_mosaics.md), and [sea ice drift maps](sea_ice_drift.md). The nominal duration over which Level 1b images are averaged: into one roughness image or mosaic pixel, or into each of the two correlated images of a drift vector. The window of an individual grid cell may be shorter, but never longer. |
| `measurement_duration`<br><small>SOMaR</small> | Number; `s` | Required for [roughness image mosaics](roughness_mosaics.md), map products, and wave products. The duration of the radar image sequence used for each mosaic, map, or wave measurement. |
| `number_of_analysis_windows`<br><small>SOMaR</small> | Integer | Required for wave products. The number of analysis windows averaged into each measurement. |
| `number_of_images`<br><small>SOMaR</small> | Integer | Required for map and wave products. The number of radar images used for each map or wave measurement. Omitted for [sea ice drift maps](sea_ice_drift.md), which are described by `time_lag` and `averaging_duration` instead. |
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
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > OCEAN CURRENTS" ;
                :keywords_vocabulary = "GCMD Science Keywords" ;
                :license = "Creative Commons Attribution 4.0 International Public License (CC BY 4.0)" ;
                :platform = "R/V Ocean Research" ;
                :platform_is_mobile = "true" ;
                :processing_level = "L2a" ;
                :processing_software = "FRORI X-band radar processing software version 2.5.0 (Python 3.13.6)" ;
                :project = "FRORI Coastal Currents Experiment" ;
                :source = "Shipboard marine X-band radar" ;
                :standard_name_vocabulary = "CF Standard Name Table v95" ;
                :station_id = "or" ;
                :summary = "The near-surface current vectors are obtained through least-squares fits ..." ;
                :time_coverage_end = "2025-01-15T12:00:00.775429Z" ;
                :time_coverage_start = "2025-01-15T11:00:31.417000Z" ;
                :title = "Marine X-band radar near-surface current measurements with quality control flag from R/V Ocean Research" ;
```

[cf-description]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents
[acdd]: https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
