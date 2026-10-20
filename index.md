---
title: Abstract
layout: home
description: SOMaR data format conventions (draft)
nav_order: 1
---

# Data Format Conventions for Sensing the Ocean with Marine Radar

_The SOMaR community_

This document is the first draft of the Sensing the Ocean with Marine Radar (SOMaR) data format conventions. They define a common NetCDF structure and metadata for marine radar products at every processing level, from raw radar data and image sequences to maps of sea surface roughness, near-surface currents, bathymetry, and sea ice drift, and to surface wave spectra and parameters, so that these data are findable, accessible, interoperable, and reusable (FAIR).

Wherever possible, SOMaR follows existing standards: the [NetCDF Climate and Forecast (CF) Metadata Conventions](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html) throughout, the [Attribute Convention for Data Discovery (ACDD)](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3) for discovery metadata such as the creator, license, and coverage of a file, and, for radar data in polar coordinates, the WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes) together with the [CfRadial format](https://github.com/NCAR/CfRadial/tree/master/docs) for moving platforms. What SOMaR adds is a way to store gridded products from a moving vessel, whose grids change location from one measurement to the next. The versions of these standards are listed under [References](contents/references/index.md#standards-and-conventions).

To keep the bar for adoption low, SOMaR has no separate lightweight version: it requires only the global attributes that tell a reader how to interpret a file, `Conventions` and `product_type`, and highly recommends those that describe the file for discovery and citation (see [Mandatory global attributes](contents/metadata_attributes/mandatory_global.md#compliance)).

{: .open_issue }
> Review which of the variables and attributes that the product pages mark as required a reader needs to interpret the data, and make the others optional or highly recommended, so that a minimal SOMaR file stays easy to write.

## Status

This is version {{ site.somar_version }} of the SOMaR data format conventions, a {{ site.somar_status }} that is subject to change.
Topics that are not yet decided are marked as open issues.
Changes are tracked in the [repository history](https://github.com/sensing-the-ocean-with-marine-radar/somar-format-draft/commits/main), and comments and proposals are welcome as [issues](https://github.com/sensing-the-ocean-with-marine-radar/somar-format-draft/issues) or pull requests.

### Versioning

A SOMaR version is identified as `SOMaR-<major>.<minor>`, the string that files declare in their `Conventions` attribute (see [Mandatory global attributes](contents/metadata_attributes/mandatory_global.md)).
Before version 1.0, anything may change from one draft to the next.
From 1.0 on, a minor version (1.1, 1.2) only adds or clarifies, so that a file valid under one minor version remains valid under the next; changes that can invalidate existing files require a new major version (2.0), and features to be removed are first marked as deprecated in a minor version.
Corrections that change no file, such as clarified wording, do not change the version.
The working copy published here carries the suffix `-draft` (e.g. `SOMaR-{{ site.somar_version }}-draft`); files written according to a draft declare that string, and released versions drop the suffix.
Each draft or release that files may refer to is tagged and published as a [release](https://github.com/sensing-the-ocean-with-marine-radar/somar-format-draft/releases) of the repository, with notes on the changes that affect files.
