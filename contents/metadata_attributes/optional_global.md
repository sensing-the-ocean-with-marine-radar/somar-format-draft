---
title: Recommended global attributes
layout: default
parent: Metadata
nav_order: 2
---

# Recommended global attributes

In addition to the [mandatory global attributes](mandatory_global.md), SOMaR recommends the following global attributes.
They are not required for a file to be a valid SOMaR product, but they aid data discovery, citation, and provenance tracking.
The convention an attribute is taken from is named in small print under the attribute (see [Metadata](index.md)).

## Highly recommended

Every SOMaR file should carry the following global attributes, regardless of processing level or product, unless its producer cannot supply them (see [Compliance](mandatory_global.md#compliance)).
They give the file a title and describe its content, which data catalogs and users rely on to find it.
They are the attributes that ACDD highly recommends, apart from `Conventions`, which SOMaR makes mandatory (see [Mandatory global attributes](mandatory_global.md)).

| Attribute | Values | Description |
|---|---|---|
| `keywords`<br><small>[ACDD][acdd]</small> | String; comma-separated list | Keywords describing the file's content, either free text or, preferably, from a controlled vocabulary such as the [GCMD Science Keywords](https://www.earthdata.nasa.gov/data/tools/gcmd-keyword-viewer). |
| `summary`<br><small>[ACDD][acdd]</small> | String; free text | A paragraph describing the file's content, analogous to an abstract: the retrieval method, processing parameters, and any caveats. |
| `title`<br><small>[CF][cf-description]</small> | String; free text | A short, human-readable description of the file's content. |
{: .attribute-table }

## Recommended

The following global attributes are recommended where they apply to the file.
The time coverage and the spatial bounds follow from the file's content, so that the software writing a file can set them.

| Attribute | Values | Description |
|---|---|---|
| `comment`<br><small>[CF][cf-description]</small> | String; free text | Further information about the file, such as the placement of the analysis windows and any window shape or retrieval method named by the processor (see [Processing parameters](processing_parameters.md)). |
| `creator_email`<br><small>[ACDD][acdd]</small> | String; email address | An email address for questions about the file's content. |
| `creator_name`<br><small>[ACDD][acdd]</small> | String; free text | The name of the person or group principally responsible for creating the file. |
| `date_created`<br><small>[ACDD][acdd]</small> | String; ISO 8601 date and time in UTC | The date on which this version of the data was created. It must agree with the creation time recorded in `history`; changes to metadata alone do not alter it. |
| `featureType`<br><small>[CF][cf-dsg]</small> | String; `trajectory` or `timeSeries` | For [spatially averaged products](../product_types/spatially_averaged.md#moving-and-fixed-platforms): the CF discrete sampling geometry that the file follows, `trajectory` from a moving platform and `timeSeries` from a fixed one. Not used by other products, which are not discrete sampling geometries. |
| `geospatial_lat_max`<br><small>[ACDD][acdd]</small> | Number; degrees north | The northernmost latitude of the positions stored in the file (see [Spatial bounds](#spatial-bounds)). |
| `geospatial_lat_min`<br><small>[ACDD][acdd]</small> | Number; degrees north | The southernmost latitude of the positions stored in the file (see [Spatial bounds](#spatial-bounds)). |
| `geospatial_lon_max`<br><small>[ACDD][acdd]</small> | Number; degrees east, between -180 and 180 | The easternmost longitude of the positions stored in the file (see [Spatial bounds](#spatial-bounds)). |
| `geospatial_lon_min`<br><small>[ACDD][acdd]</small> | Number; degrees east, between -180 and 180 | The westernmost longitude of the positions stored in the file (see [Spatial bounds](#spatial-bounds)). |
| `history`<br><small>[CF][cf-description]</small> | String; one entry per processing step, each starting with a UTC timestamp | A record of the file's provenance, at minimum its creation time. Later entries (e.g. reprocessing) are appended to this attribute rather than overwriting it. |
| `institution`<br><small>[CF][cf-description]</small> | String; free text | The institution responsible for producing the file. |
| `institution_id`<br><small>SOMaR</small> | String; URI | A persistent identifier for the institution named in `institution`, e.g. its [ROR](https://ror.org/) ID. |
| `instrument`<br><small>[ACDD][acdd]</small> | String; free text | The manufacturer, model, and/or type of the radar system used, including relevant technical detail such as whether the receiver is coherent. |
| `keywords_vocabulary`<br><small>[ACDD][acdd]</small> | String; free text | The controlled vocabulary from which the `keywords` are taken, e.g. `GCMD Science Keywords`. |
| `license`<br><small>[ACDD][acdd]</small> | String; URL or free text | The data usage license under which the file is released. |
| `platform`<br><small>[ACDD][acdd]</small> | String; free text | The name of the vessel or platform the radar was mounted on. |
| `platform_is_mobile`<br><small>[FM 301][fm301], Table 301-1</small> | String; `true` or `false` | Required for a moving platform. Whether the platform moves. FM 301 allows only `false`; SOMaR also allows `true`. Assumed `false`, a fixed platform, if missing, so that a file from a moving platform must set it to `true`. Polar products (Level 1a and Level 1b polar) should then record the position and heading of the platform for every sweep or every ray (see [Georeferencing](../georeferencing/index.md#polar-sensor-coordinates)), and Level 2 products take the structure of a moving platform (see [Gridded products](../product_types/gridded.md) and [Spatially averaged products](../product_types/spatially_averaged.md#moving-and-fixed-platforms)). |
| `processing_level`<br><small>[ACDD][acdd]</small> | String; one of `L1a`, `L1b`, `L2a`, `L2b` | The SOMaR processing level of the file's content (see [SOMaR product types](../product_types/index.md)). ACDD allows free text here; SOMaR restricts it to these codes. |
| `processing_software`<br><small>SOMaR</small> | String; free text | The name and version of the software used to produce the file, to support reproducibility. |
| `project`<br><small>[ACDD][acdd]</small> | String; free text | The scientific project(s) under which the data were collected, comma-separated. |
| `references`<br><small>[CF][cf-description]</small> | String; free text | Published or web-based references that describe the data or the methods by which they were retrieved. |
| `source`<br><small>[CF][cf-description]</small> | String; free text | The method of production of the underlying data, e.g. the type of platform and sensor. |
| `standard_name_vocabulary`<br><small>[ACDD][acdd]</small> | String; e.g. `CF Standard Name Table v95` | The version of the CF standard name table from which the `standard_name` attributes are taken. The table is versioned separately from the CF conventions, so the CF version in `Conventions` does not identify it; if the attribute is missing, the table is the one SOMaR refers to (see [References](../references/index.md#cf-standard-names)). |
| `station_id`<br><small>SOMaR</small> | String; short, lowercase identifier | The identifier of the platform used as the prefix of the [file name](../file_naming/index.md), e.g. `or`. |
| `time_coverage_end`<br><small>[ACDD][acdd]</small> | String; ISO 8601 date and time in UTC, fractional seconds permitted | The time of the latest observation contributing to the data in the file. For products that store one group or measurement per averaging window or measurement period, each identified by its start time, this is the end of the last averaging window or measurement period. |
| `time_coverage_start`<br><small>[ACDD][acdd]</small> | String; ISO 8601 date and time in UTC, fractional seconds permitted | The time of the first observation contributing to the data in the file. |
{: .attribute-table }

### Spatial bounds

The `geospatial_lat_min`, `geospatial_lat_max`, `geospatial_lon_min`, and `geospatial_lon_max` attributes give the extremes of the positions stored in the file, so that they follow from its content alone.
These positions are the values of all variables named `latitude` and `longitude`, in any group and excluding fill values, and, in groups without such variables, the projection origin of the `crs` variable (`latitude_of_projection_origin`, `longitude_of_projection_origin`).
Depending on the product, they are the positions of the radar antenna (Level 1 products, relative roughness images, and relative roughness image mosaics), the centers of the analysis windows (map products), or their mean positions (wave products), in each case as stored, i.e. uncorrected in polar products (see [Georeferencing](../georeferencing/index.md#applying-georeference-corrections)).
Other positions, such as `radar_latitude` and `radar_longitude`, do not count.

The bounds therefore enclose the positions of the data rather than the area observed, which extends beyond them by up to the maximum range of the radar or half the analysis window size; for a fixed platform, the minimum and maximum may coincide.
ACDD describes these attributes as the bounds of the data; SOMaR narrows this to a definition that every writer can apply in the same way and that can be checked against the file.
If the positions span the antimeridian, `geospatial_lon_min` is the westernmost and `geospatial_lon_max` the easternmost longitude, so that `geospatial_lon_min` is greater than `geospatial_lon_max`, as ACDD allows.

## Example

The global attributes of a [near-surface current map](../annex/current_maps.md) file, with the mandatory, highly recommended, and recommended attributes:

```
// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :product_type = "currents" ;
                :creator_email = "famous.scientist@frori.org" ; // recommended
                :creator_name = "Dr. Famous Scientist" ; // recommended
                :date_created = "2025-01-15T12:05:00Z" ; // recommended
                :geospatial_lat_max = 15.03 ; // recommended
                :geospatial_lat_min = 14.9265 ; // recommended
                :geospatial_lon_max = 145.96815 ; // recommended
                :geospatial_lon_min = 145.8426 ; // recommended
                :history = "20250115T120500Z: File creation time" ; // recommended
                :institution = "Famous Radar Ocean Research Institute" ; // recommended
                :institution_id = "https://ror.org/01abcde23" ; // recommended
                :instrument = "Famous Radar Ocean Research Institute coherent-on-receive marine X-band radar" ; // recommended
                :keywords = "EARTH SCIENCE > OCEANS > OCEAN CIRCULATION > OCEAN CURRENTS" ; // highly recommended
                :keywords_vocabulary = "GCMD Science Keywords" ; // recommended
                :license = "Creative Commons Attribution 4.0 International Public License (CC BY 4.0)" ; // recommended
                :platform = "R/V Ocean Research" ; // recommended
                :platform_is_mobile = "true" ;
                :processing_level = "L2a" ; // recommended
                :processing_software = "FRORI X-band radar processing software version 2.5.0 (Python 3.13.6)" ; // recommended
                :project = "FRORI Coastal Currents Experiment" ; // recommended
                :source = "Shipboard marine X-band radar" ; // recommended
                :standard_name_vocabulary = "CF Standard Name Table v95" ; // recommended
                :station_id = "or" ; // recommended
                :summary = "The near-surface current vectors are obtained through least-squares fits ..." ; // highly recommended
                :time_coverage_end = "2025-01-15T12:00:00.775429Z" ; // recommended
                :time_coverage_start = "2025-01-15T11:00:31.417000Z" ; // recommended
                :title = "Marine X-band radar near-surface current measurements with quality control flag from R/V Ocean Research" ; // highly recommended
```

[cf-description]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents
[acdd]: https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
[cf-dsg]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#discrete-sampling-geometries
