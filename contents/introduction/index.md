---
title: Introduction
layout: default
nav_order: 2
---

# Introduction

Over the past decades, the Sensing the Ocean with Marine Radar (SOMaR) community has developed a set of techniques to extract hydrographic variables from marine radar data. However, the associated algorithms and output data formats have not yet been standardized, and different formats are currently used across research groups. To achieve better comparability, and thereby facilitate collaboration between groups, a common interoperable data format defining standard products used within the SOMaR community is needed.

## Scope
This document is tailored for use within the SOMaR community and applies to ocean radar data collected by radars typically used for navigation. These are primarily systems operating in the X or S band and equipped with beam antennas that scan the ocean surface.

## Why a New Format?
The primary reason for developing a new format is that marine radar data are often collected from moving vessels with rotating radar antennas scanning the ocean surface. High-level data products (gridded geophysical variables) are therefore often mapped onto a local Cartesian grid whose origin changes over time. Such a data type is not specified by the current CF conventions; therefore, an extension is required.
At a lower level of processing, the WMO-CF RADIAL format may also be applicable. However, this format has not yet been released and is relatively complex compared to the requirements of marine radar data. The SOMaR data formats therefore aim to be compatible with WMO-CF RADIAL and standard CF conventions wherever possible, while providing a more lightweight data standard for the specific needs of the SOMaR community.
SOMaR introduces the concept of time-bounded local grids, in which geophysical variables are mapped onto Cartesian grids defined in a radar-centric reference frame. These grids are valid only for a limited time window and may change in spatial extent, resolution, and orientation over time. Each grid is therefore stored together with its own georeferencing information in a dedicated NetCDF group. This approach preserves flexibility while maintaining CF compatibility at the variable level.

## Document Structure
In the following, we first describe mandatory and optional global metadata attributes, file-naming conventions, and georeferencing applicable to all SOMaR data products. We then introduce specific high-level products together with their respective additional attributes and grid-definition conventions.