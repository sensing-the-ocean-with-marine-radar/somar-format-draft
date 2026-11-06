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

The primary reason for developing a new format is that marine radar data are often collected from moving vessels, so that gridded data cover an area that moves with the vessel.
Each measurement period of the [near-surface current maps](../annex/current_maps.md), for example, yields a map over the radar footprint, and by the next period that footprint has moved on: a file holds a sequence of maps on different grids rather than one grid sampled repeatedly.
The same holds for the other Level 2 maps and for radar images mapped onto a local Cartesian grid whose origin moves with the vessel.
The CF conventions can describe each such grid but have no provision for a sequence of grids whose location changes; SOMaR therefore defines how such sequences are stored, using NetCDF-4 groups (see [Time-bounded grids](../georeferencing/index.md#time-bounded-grids), with a [figure](../georeferencing/index.md#figure-time-bounded-grids)).
Each grid can thus have its own origin, extent, and resolution, while every variable within it still carries standard CF metadata.

At the lowest level of processing, radar data in polar coordinates are already covered by an international standard, the WMO-CF Radial profile [FM 301][fm301], which was developed for weather radars from the earlier [CfRadial format][cfradial].
SOMaR does not replicate this work: its [polar data types](../data_types/polar_raw.md#relation-to-fm-301-and-cfradial) follow FM 301 wherever possible, and CfRadial 2.1 for moving platforms, which FM 301 does not support.
Neither document covers the data that follow, i.e. image sequences on regular grids and the geophysical products retrieved from them; these are defined by SOMaR.
For discovery metadata, such as the creator, license, and coverage of a file, SOMaR adopts the [Attribute Convention for Data Discovery (ACDD)][acdd], which is designed to complement CF.
The versions of these standards that SOMaR refers to are listed under [References](../references/index.md#standards-and-conventions).

## Terms

- **Processing levels** order SOMaR data from the radar's own measurement (Level 1a and 1b) to geophysical variables (Level 2a and 2b); they are defined under [SOMaR data types](../data_types/index.md#processing-levels). **Level 0** data, the radar recording as delivered by the instrument in the manufacturer's format, are not defined by SOMaR; [Level 1a](../data_types/polar_raw.md) is their conversion to NetCDF.
- A **ray** is one stored azimuth sample of a sweep, i.e. the echo along one beam direction as a function of range, following FM 301. At Level 1a, a ray normally holds a single transmitted pulse, unless the radar itself averages pulses (`n_samples` > 1); in Level 1b polar images, it is one bin of the regular azimuth axis, and in Level 1b pulse-averaged data the mean of `n_samples` consecutive pulses.
- A **sweep** is the sequence of rays of one antenna revolution, or of one dwell at a fixed direction for a radar in pointing mode. It is the unit in which Level 1a data and Level 1b pulse-averaged data are stored.
- An **image** is the Level 1b representation of one sweep. Images are not defined for sweeps recorded in pointing mode, which Level 1b may average over pulses instead.
- An **analysis window** is the area, within the radar footprint, from which one Level 2 measurement is retrieved.
- A **measurement period** is the time span over which the images contributing to one Level 2 map or measurement are collected. Its length is given by [`measurement_duration`](../metadata_attributes/processing_parameters.md#measurement_duration).
- An **averaging period** is the time span over which Level 1b images are averaged into one relative roughness image, one mosaic pixel, or one of the two images of a sea ice drift retrieval. Its nominal length is given by [`averaging_duration`](../metadata_attributes/processing_parameters.md#averaging_duration); for individual pixels it may be shorter.

## Document structure

The [Metadata](../metadata_attributes/index.md) chapter describes what all SOMaR files share: the NetCDF-4 data model, global and variable attributes, the processing parameters and quality flags of the Level 2 products, and the radar, georeference correction, and wave calibration parameters.
The [Georeferencing](../georeferencing/index.md) chapter defines the spatial framework that locates the data: polar coordinates, the application of georeference corrections, coordinate reference systems, including the time-bounded and rotated local grids, and the grids of the gridded data types.
The [SOMaR data types](../data_types/index.md) chapter defines the data types, i.e. the structures of SOMaR files, on a page each, from the Level 1 radar data in polar or Cartesian form to the Level 2 data in pixels or in gridded, discrete, or averaged analysis windows, together with the Level 2 products of each data type and the variables that hold their data.
The [File naming](../file_naming/index.md) chapter specifies the naming pattern for SOMaR files on disk, and the [Storage recommendations](../storage/index.md) chapter their compression and chunking.
Finally, the informative [Annex: Examples](../annex/index.md) gives an example file of each Level 1 data type and each Level 2 product, and for Level 2 a description of the product and of its retrieval.

The chapters Metadata, Georeferencing, and SOMaR data types are normative; File naming and Storage recommendations give recommendations that are not part of [compliance](../metadata_attributes/mandatory_global.md#compliance).
The Annex and the CDL examples throughout the document are informative; where an example and a definition differ, the definition applies.

[acdd]: https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
