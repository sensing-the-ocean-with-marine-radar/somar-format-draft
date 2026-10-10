---
title: Abstract
layout: home
description: SOMaR-data-formats-v0.5-draft
nav_order: 1
---

# Data Format Conventions for Sensing the Ocean with Marine Radar
SOMaR-data-formats-v0.5-draft

_The SOMaR community_

This document is the first draft of the Sensing the Ocean with Marine Radar (SOMaR) data format conventions. They define a common NetCDF structure and metadata for marine radar products at every processing level, from raw radar data and image sequences to maps of sea surface roughness, near-surface currents, bathymetry, and sea ice drift, and to surface wave spectra and parameters, so that these data are findable, accessible, interoperable, and reusable (FAIR).

Wherever possible, SOMaR follows existing standards: the [NetCDF Climate and Forecast (CF) Metadata Conventions](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html) throughout, the [Attribute Convention for Data Discovery (ACDD)](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3) for discovery metadata such as the creator, license, and coverage of a file, and, for radar data in polar coordinates, the WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes) together with the [CfRadial format](https://github.com/NCAR/CfRadial/tree/master/docs) for moving platforms. What SOMaR adds is a way to store gridded products from a moving vessel, whose grids change location from one measurement to the next.
