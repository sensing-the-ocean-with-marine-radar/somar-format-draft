---
title: Trajectory data
layout: default
parent: Level 2 data
#nav_order: 1
---

# Trajectory data

Trajectory products give one value or spectrum per analysis window along the platform's path, indexed by `time` with accompanying `longitude` and `latitude` and a `measurement_quality` flag, rather than as spatial fields.
Currently this covers surface wave products, retrieved from a dispersion-relation-based wavenumber-frequency analysis of local circular radar image analysis windows: [two-dimensional wavenumber spectra](wave_wavenumber_spectra.md), [one-dimensional frequency spectra](wave_frequency_spectra.md) derived from them, and [peak and mean wave parameters](wave_parameters.md).
