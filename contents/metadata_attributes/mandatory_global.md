---
title: Mandatory global attributes
layout: default
parent: Metadata attributes
nav_order: 1
---

# Mandatory global attributes

Every SOMaR NetCDF file must carry the following global attributes, regardless of processing level or product:

| Attribute | Example | Description |
|---|---|---|
| `Conventions` | `"CF-1.13 SOMaR-0.3-draft"` | The CF convention version the file complies with, together with the SOMaR format version, space separated. |
| `title` | `"Marine X-band radar near-surface current measurements with quality control flag from R/V Ocean Research"` | A short, human-readable description of the file's content, specific enough to distinguish it from other SOMaR products. |
| `institution` | `"Famous Radar Ocean Research Institute"` | The institution responsible for producing the file. |
| `source` | `"Shipboard marine X-band radar"` | The method of production of the underlying data, e.g. the type of platform and sensor. |
| `contact` | `"famous.scientist@frori.org"` | An email address for questions about the file's content. |
| `originator` | `"Dr. Famous Scientist"` | The name of the person or group responsible for creating the file. |
| `history` | `"20230831T170026Z: File creation time"` | A record of the file's provenance, at minimum its creation time; audit trail entries (e.g. later reprocessing) should be appended to this attribute rather than overwriting it, following standard CF practice. |
| `featureType` | `"trajectory"` | The CF discrete sampling geometry of the file. All SOMaR Level 1b and Level 2 products currently use `"trajectory"`, since every product is defined along the platform's track through time; see [Georeferencing](georeferencing.md) for the accompanying `trajectory` variable convention this requires. |

Level 1a files, which precede the trajectory/georeferencing conventions used from Level 1b onward (see [Level 1a data](../data_types/level1/level1a.md)), are not required to carry `featureType`.
