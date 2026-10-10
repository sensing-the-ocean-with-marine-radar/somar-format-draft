---
title: Introduction
layout: default
nav_order: 2
---

# Introduction

Over the past decades, the Sensing the Ocean with Marine Radar (SOMaR) community has developed a set of techniques to extract hydrographic variables from marine radar data. However, the output data formats have not yet been standardized, and different formats are currently used across research groups. To make marine radar data findable, accessible, interoperable, and reusable (FAIR), and thereby facilitate their use and exchange well beyond the groups that produce them, SOMaR defines a common data format with standard products.

## Scope
This document is tailored for use within the SOMaR community and applies to ocean radar data collected by radars typically used for navigation. These are primarily systems operating in the X or S band and equipped with beam antennas that scan the ocean surface.

## Why a New Format?
The primary reason for developing a new format is that marine radar data are often collected from moving vessels with rotating radar antennas scanning the ocean surface. High-level products (gridded geophysical variables) are therefore often mapped onto a local Cartesian grid whose origin changes over time. Such a data type is not specified by the current CF conventions; therefore, an extension is required.
At the lowest level of processing, radar data in polar coordinates are already covered by an international standard, the WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes) of the WMO Manual on Codes, which was developed for weather radars from the earlier [CfRadial format](https://github.com/NCAR/CfRadial/tree/master/docs). SOMaR does not replicate this work. For [Level 1a data](../data_types/level1/level1a.md) and the [radar parameters](../metadata_attributes/radar_parameters.md), it follows FM 301 wherever possible, including the organization of a file in sweeps, but leaves out what is of no use for a marine radar, such as the elevation angle of a radar that scans horizontally only. FM 301 does not support moving platforms; for the position and heading of a ship and for corrections to the recorded azimuth and range, SOMaR follows the CfRadial 2.1 draft, which provides them. Everything else is defined by SOMaR: neither document covers the products that follow, i.e. image sequences on regular polar or Cartesian grids and the geophysical variables retrieved from them. For discovery metadata, such as the creator, license, and temporal and spatial coverage of a file, SOMaR adopts the attribute names of the [Attribute Convention for Data Discovery (ACDD)](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3), which is designed to complement CF.
SOMaR introduces the concept of time-bounded local grids, in which geophysical variables are mapped onto Cartesian grids defined in a radar-centric reference frame. These grids are flat, with coordinates in meters east and north (true north) of the radar position. They are valid only for a limited time window and may change in origin, spatial extent, and resolution over time. Each grid is therefore stored together with its own georeferencing information in a dedicated NetCDF group. This approach preserves flexibility while maintaining CF compatibility at the variable level.

## Document Structure
In the following, we first describe mandatory and optional global metadata attributes, file-naming conventions, and georeferencing applicable to all SOMaR products. We then introduce specific high-level products together with their respective additional attributes and grid-definition conventions.