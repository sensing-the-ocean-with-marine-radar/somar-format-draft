---
title: Introduction
layout: default
nav_order: 2
---

# Introduction

Over the past decades, the Sensing the Ocean with Marine Radar (SOMaR) community has developed a set of techniques to extract oceanographic variables from marine radar data. However, the output data formats have not yet been standardized, and different formats are currently used across research groups. To make marine radar data findable, accessible, interoperable, and reusable (FAIR), and thereby facilitate their use and exchange well beyond the groups that produce them, SOMaR defines a common data format with standard products.

## Scope
This document is tailored for use within the SOMaR community and applies to ocean radar data collected by radars typically used for navigation. These are primarily systems operating in the X or S band and equipped with rotating fan-beam antennas that scan the ocean surface.

## Why a new format?

The primary reason for developing a new format is that marine radar data are often collected from moving vessels, so that gridded products cover an area that moves with the vessel.
Each measurement period of the [near-surface current maps](../product_types/level2/current_maps.md), for example, yields a map over the radar footprint, and by the next period that footprint has moved on: a file holds a sequence of maps on different grids rather than one grid sampled repeatedly.
The same holds for the other Level 2 maps and for radar images mapped onto a local Cartesian grid whose origin moves with the vessel.
The CF conventions can describe each such grid but have no provision for a sequence of grids whose location changes; SOMaR therefore defines how such sequences are stored, using NetCDF-4 groups (see [Time-bounded local grids](../georeferencing/index.md#time-bounded-local-grids) and [Map products](../product_types/level2/index.md#map-products)).
Each grid can thus have its own origin, extent, and resolution, while every variable within it still carries standard CF metadata.

At the lowest level of processing, radar data in polar coordinates are already covered by an international standard, the WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes), which was developed for weather radars from the earlier [CfRadial format](https://github.com/NCAR/CfRadial/tree/master/docs).
SOMaR does not replicate this work: [Level 1a data](../product_types/level1/level1a.md#relation-to-fm-301-and-cfradial) follow FM 301 wherever possible, and CfRadial 2.1 for moving platforms, which FM 301 does not support.
Neither document covers the products that follow, i.e. image sequences on regular grids and the geophysical variables retrieved from them; these are defined by SOMaR.
For discovery metadata, such as the creator, license, and coverage of a file, SOMaR adopts the [Attribute Convention for Data Discovery (ACDD)](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3), which is designed to complement CF.
The versions of these standards that SOMaR refers to are listed under [References](../references/index.md#standards-and-conventions).

## Terms

- **Processing levels** order SOMaR products from the radar's own measurement (Level 1a and 1b) to geophysical variables (Level 2a and 2b); they are defined under [SOMaR product types](../product_types/index.md). **Level 0** data, the radar recording as delivered by the instrument in the manufacturer's format, are not defined by SOMaR; [Level 1a](../product_types/level1/level1a.md) is their conversion to NetCDF.
- A **sweep** is the sequence of pulses of one antenna revolution, or of one pass over the sector for a radar that scans a sector. It is the unit in which Level 1a data are stored.
- An **image** is the Level 1b representation of one sweep.
- An **analysis window** is the area, within the radar footprint, from which one Level 2 measurement is retrieved.
- A **measurement period** is the time span over which the images contributing to one Level 2 map or measurement are collected.
- An **averaging window** is the time span over which Level 1b images are averaged into one roughness image or one mosaic pixel.

## Document structure

The [Metadata](../metadata_attributes/index.md) chapter describes what all SOMaR products share: the NetCDF-4 data model, global and variable attributes, and the radar, georeference correction, and wave calibration parameters.
The [Georeferencing](../georeferencing/index.md) chapter defines the spatial framework that locates the products: polar coordinates, the application of georeference corrections, coordinate reference systems, time-bounded local grids, and analysis windows.
The [SOMaR product types](../product_types/index.md) chapter defines each product in turn, from Level 1 radar products to Level 2 geophysical products, with its variables, its grid, and a minimal example.
Finally, the [File naming](../file_naming/index.md) chapter specifies the naming pattern for SOMaR files on disk.
