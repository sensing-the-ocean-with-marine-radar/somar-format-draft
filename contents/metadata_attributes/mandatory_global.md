---
title: Mandatory global attributes
layout: default
parent: Metadata attributes
nav_order: 1
---

# Mandatory global attributes

Every SOMaR NetCDF file must carry the following global attributes, regardless of processing level or product.
The convention an attribute is taken from is named in small print under the attribute (see [Metadata attributes](index.md)); where an attribute has a fixed set of permitted values, all of them are listed and those currently used by SOMaR are set in bold.

| Attribute | Values | Description |
|---|---|---|
| `Conventions`<br><small>[CF][cf-conventions]</small> | String; comma-separated list of the form `CF-<version>, ACDD-<version>, SOMaR-<version>` | The versions of the CF conventions, of ACDD, and of the SOMaR format that the file complies with. |
| `title`<br><small>[CF][cf-description]</small> | String; free text | A short, human-readable description of the file's content, specific enough to distinguish it from other SOMaR products. |
| `institution`<br><small>[CF][cf-description]</small> | String; free text | The institution responsible for producing the file. |
| `source`<br><small>[CF][cf-description]</small> | String; free text | The method of production of the underlying data, e.g. the type of platform and sensor. |
| `history`<br><small>[CF][cf-description]</small> | String; one entry per processing step, each starting with a UTC timestamp | A record of the file's provenance, at minimum its creation time. Later entries (e.g. reprocessing) are appended to this attribute rather than overwriting it. |
| `creator_name`<br><small>[ACDD][acdd]</small> | String; free text | The name of the person or group principally responsible for creating the file. |
| `creator_email`<br><small>[ACDD][acdd]</small> | String; email address | An email address for questions about the file's content. |
| `processing_level`<br><small>[ACDD][acdd]</small> | String; one of `L1a`, `L1b`, `L2a`, `L2b` | The SOMaR processing level of the file's content (see [SOMaR data types](../data_types/index.md)). ACDD allows free text here; SOMaR restricts it to these codes. |
| `featureType`<br><small>[CF][cf-featuretype]</small> | String; one of `point`, `timeSeries`, **`trajectory`**, `profile`, `timeSeriesProfile`, `trajectoryProfile` | The CF discrete sampling geometry of the file. All SOMaR Level 1b and Level 2 products currently use `trajectory`, since every product is defined along the platform's track through time; see [Georeferencing](georeferencing.md) for the accompanying `trajectory` variable. Not required at Level 1a, which precedes the trajectory and georeferencing conventions used from Level 1b onward. |
{: .attribute-table }

The WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes), which SOMaR follows for [Level 1a data](../data_types/level1/level1a.md), defines mandatory global attributes of its own. Apart from `platform_is_mobile` (see [Optional global attributes](optional_global.md)), Level 1a files do not use them: they are not FM 301 files, so `Conventions` does not list the WMO-CF extensions, the attributes of the `wmo__` namespace are omitted, and the radar is named with the ACDD attribute `instrument` rather than FM 301's `instrument_name`.

SOMaR adopts ACDD attribute names wherever it defines an attribute that ACDD also defines, but it does not require the complete set of attributes recommended by ACDD.

[cf-conventions]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#identification-of-conventions
[cf-description]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#description-of-file-contents
[cf-featuretype]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#featureType
[acdd]: https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
