---
title: Abstract
layout: home
description: SOMaR-data-formats-v0.5-draft
nav_order: 1
---

# Data Format Conventions for Sensing the Ocean with Marine Radar
SOMaR-data-formats-v0.5-draft

_The SOMaR community_

This document presents the first draft of the Sensing the Ocean with Marine Radars (SOMaR) standard data formats, developed to facilitate the use, sharing, and post-processing of marine radar ocean sensing products across multiple processing levels. It defines a common data structure and metadata conventions for a range of product types, including maps, trajectories, and profiles.

Wherever possible, SOMaR data formats adhere to the [NetCDF Climate and Forecast (CF) Metadata Conventions](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html). Discovery metadata, such as the creator, license, and temporal and spatial coverage of a file, follow the [Attribute Convention for Data Discovery (ACDD)](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3). Required SOMaR-specific extensions are documented in detail. The formats are designed to be lightweight, self-describing, and flexible enough to support a wide range of scientific and operational use cases.