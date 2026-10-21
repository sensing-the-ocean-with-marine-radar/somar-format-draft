---
title: Introduction
layout: default
nav_order: 2
---

# Introduction

Over the past decades, the Sensing the Ocean with Marine Radar (SOMaR) community has developed a set of techniques to extract oceanographic variables from marine radar data. However, the output data formats have not yet been standardized, and different formats are currently used across research groups. To make marine radar data findable, accessible, interoperable, and reusable (FAIR), and thereby facilitate their use and exchange well beyond the groups that produce them, SOMaR defines a common data format with standard products.

## Scope
This document is tailored for use within the SOMaR community and applies to ocean radar data collected by radars typically used for navigation. These are primarily systems operating in the X or S band and equipped with fan-beam antennas that rotate to scan the ocean surface or are held at a fixed direction (pointing mode).

## Why a new format?

The primary reason for developing a new format is that marine radar data are often collected from moving vessels, so that gridded products cover an area that moves with the vessel.
Each measurement period of the [near-surface current maps](../annex/current_maps.md), for example, yields a map over the radar footprint, and by the next period that footprint has moved on: a file holds a sequence of maps on different grids rather than one grid sampled repeatedly.
The same holds for the other Level 2 maps and for radar images mapped onto a local Cartesian grid whose origin moves with the vessel.
The CF conventions can describe each such grid but have no provision for a sequence of grids whose location changes; SOMaR therefore defines how such sequences are stored, using NetCDF-4 groups (see [Time-bounded local grids](../georeferencing/index.md#time-bounded-local-grids) and [Gridded products](../product_types/gridded.md#time-bounded-grids)).
Each grid can thus have its own origin, extent, and resolution, while every variable within it still carries standard CF metadata.

At the lowest level of processing, radar data in polar coordinates are already covered by an international standard, the WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes), which was developed for weather radars from the earlier [CfRadial format](https://github.com/NCAR/CfRadial/tree/master/docs).
SOMaR does not replicate this work: [Level 1a data](../product_types/polar.md#relation-to-fm-301-and-cfradial) follow FM 301 wherever possible, and CfRadial 2.1 for moving platforms, which FM 301 does not support.
Neither document covers the products that follow, i.e. image sequences on regular grids and the geophysical variables retrieved from them; these are defined by SOMaR.
For discovery metadata, such as the creator, license, and coverage of a file, SOMaR adopts the [Attribute Convention for Data Discovery (ACDD)](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3), which is designed to complement CF.
The versions of these standards that SOMaR refers to are listed under [References](../references/index.md#standards-and-conventions).

## Terms

- **Processing levels** order SOMaR products from the radar's own measurement (Level 1a and 1b) to geophysical variables (Level 2a and 2b); they are defined under [SOMaR product types](../product_types/index.md). **Level 0** data, the radar recording as delivered by the instrument in the manufacturer's format, are not defined by SOMaR; [Level 1a](../product_types/polar.md) is their conversion to NetCDF.
- A **ray** is one stored azimuth sample of a sweep, i.e. the echo along one beam direction as a function of range, following FM 301. At Level 1a, a ray normally holds a single transmitted pulse, unless the radar itself averages pulses (`n_samples` > 1); at Level 1b polar, it is one bin of the regular azimuth axis.
- A **sweep** is the sequence of rays of one antenna revolution, or of one dwell at a fixed direction for a radar in pointing mode. It is the unit in which Level 1a data are stored.
- An **image** is the Level 1b representation of one sweep. Images are not defined for sweeps recorded in pointing mode.
- An **analysis window** is the area, within the radar footprint, from which one Level 2 measurement is retrieved.
- A **measurement period** is the time span over which the images contributing to one Level 2 map or measurement are collected. Its length is given by `measurement_duration`.
- An **averaging window** is the time span over which Level 1b images are averaged into one relative roughness image or one mosaic pixel. Its nominal length is given by `averaging_duration`; for individual pixels it may be shorter.

## Document structure

The [Metadata](../metadata_attributes/index.md) chapter describes what all SOMaR products share: the NetCDF-4 data model, global and variable attributes, the processing parameters and quality flags of the Level 2 products, and the radar, georeference correction, and wave calibration parameters.
The [Georeferencing](../georeferencing/index.md) chapter defines the spatial framework that locates the products: polar coordinates, the application of georeference corrections, coordinate reference systems, time-bounded local grids, and analysis windows.
The [SOMaR product types](../product_types/index.md) chapter defines the products in three categories by their geometry, polar, gridded, and spatially averaged, from the Level 1 radar products to the Level 2 geophysical products, with their structures, and defines the variables that hold their data.
The [File naming](../file_naming/index.md) chapter specifies the naming pattern for SOMaR files on disk.
Finally, the informative [Annex: Example products](../annex/index.md) gives an example file of each product, and for Level 2 a description of the product and of its retrieval.
