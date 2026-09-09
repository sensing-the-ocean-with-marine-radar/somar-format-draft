---
title: Introduction
layout: default
nav-order: 2
---

# Introduction

Over the past decades, the Sensing the Ocean with Marine Radar (SOMaR) community has developed a set of techniques to extract hydrographic variables from marine radar data. So far, the algorithms and their output data formats are not standardized and different formats are used among groups. In order to achieve better comparability - thus easier collaboration between groups - a common interoperable data format defining standard products used within the SOMaR community is needed.   

## Scope
This document is tailored for use within the SOMaR community, thus for ocean radar data that are collected with radars that are typically used for navigation. Those are mostly systems working at X- or S-band that are equipped with beam antennas scanning the ocean surface. 

## Why a new format? 
The major fact that leads to the necessity of a new format is the fact that marine radar data is often collected from moving vessels with a rotating radar antenna scanning the ocean surface. High level data products (gridded geophysical variables) are therefore often mapped to a Cartesian local grid, with its origin changing in time. Such a data type is not specified by the current CF conventions hence an extension is required. On a lower level of processing, the WMO-CF RADIAL format may also be applicable. However, this format is not released yet and is quite “heavy” compared to what is needed for marine radar data. The SOMaR data formats are therefore aiming to be compatible with the CF RADIAL and standard CF-conventions as far as possible, yet providing a more lightweight data standard for the specific needs of the SOMaR community.  

SOMaR introduces the concept of time-bounded local grids, where geophysical variables are mapped onto Cartesian grids defined in a radar-centric reference frame. These grids are valid only for a limited time window and may change their spatial extent, resolution, and orientation over time. Each grid is therefore stored together with its own georeferencing information in a dedicated NetCDF group. This approach preserves flexibility while maintaining CF compatibility at the variable level.

## Document structure 
In the following, we first describe mandatory and optional global metadata attributes, file naming conventions, and georeferencing pertaining to all SOMaR data products. We then introduce specific high level products with their respective additional attributes or grid definition conventions. 
