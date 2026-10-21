---
title: "Level 2: Geophysical quantities"
layout: default
parent: SOMaR product types
nav_order: 2
has_children: true
---

# Level 2: Geophysical quantities

Level 2 products are geophysical quantities derived from sequences of Level 1b images, such as relative sea surface roughness, near-surface currents, bathymetry, sea ice drift, and surface waves.
This page describes their processing levels and their two categories; their [processing parameters](../../metadata_attributes/processing_parameters.md), with the names of the retrieval methods, and their [quality flags](../../metadata_attributes/quality_flags.md) are described under Metadata.

## Processing levels

Level 2 products are divided into two sublevels according to how they are obtained.
Level 2a products are the direct result of a retrieval applied to Level 1b image sequences: relative roughness images and mosaics, maps of near-surface currents, current profiles, bathymetry, and sea ice drift, and two-dimensional wavenumber spectra.
Level 2b products are computed from Level 2a products and therefore inherit their sampling, calibration, and quality control; currently all of them are surface wave products derived from the two-dimensional wavenumber spectra.
The level of each product is given in the product-type table of its category.

## Categories

Level 2 products fall into two categories, according to how a measurement is located in space:

- [Gridded products](gridded.md) (maps, images) give one value set for each cell of a grid that resolves the area covered: each analysis window, or each pixel of an image, keeps its own position.
- [Spatially averaged products](spatially_averaged.md) (spectra, bulk parameters) combine several analysis windows into one value set per measurement, located at their mean position.

The structure of a file depends on its category and on whether the platform moves, which a file from a moving platform states by setting [`platform_is_mobile`](../../metadata_attributes/optional_global.md) to `"true"`:

| | Moving platform | Fixed platform |
|---|---|---|
| **Gridded products** | one [time-bounded grid](gridded.md#time-bounded-grids) per measurement, each in its own `time_<YYYYMMDDHHMMSS>` group | a [single grid](gridded.md#fixed-platform) for the whole file, with the leading dimension `time` |
| **Spatially averaged products** | a [trajectory](spatially_averaged.md#moving-and-fixed-platforms): `longitude(time)` and `latitude(time)` | a [time series](spatially_averaged.md#moving-and-fixed-platforms): scalar `longitude` and `latitude` |

Each category page defines the structure that its products share and lists its products with the variables that each of them holds.
The variables themselves are defined under [Product variables](../../metadata_attributes/product_variables.md).
