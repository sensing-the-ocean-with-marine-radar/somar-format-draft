---
title: File naming recommendations
layout: default
parent: Metadata attributes
nav_order: 5
---

# File naming recommendations

SOMaR files should be named so that a file's platform, time coverage, and product can be identified without opening it, following the pattern:

```
<station_id>_<YYYY-MM-DD>-<HH>[-<MM>]_<product_name>[_average].nc
```

- `station_id` is a short, lowercase, unique identifier for the originating platform, e.g. `or` for the fictional R/V Ocean Research used throughout this document's examples.
- `<YYYY-MM-DD>-<HH>` is the UTC date and hour at which the file's data coverage begins. Most SOMaR products are aggregated into one file per hour; sub-hourly products additionally append a two-digit `-<MM>` minute field.
- `product_name` is a short, snake_case name identifying the product, matching the naming used for the product throughout this document (e.g. `sea_surface_roughness`, `sea_surface_roughness_mosaic`, `currents`, `currents_profile`, `bathymetry`, `sea_ice_drift`).
- Level 2 products that are temporal averages of an underlying per-analysis-window product carry an `_average` suffix (e.g. `wave_parameters_average.nc`) to distinguish them from their un-averaged counterparts.

| Example filename | Product |
|---|---|
| `or_2025-01-15-11-00_single_scan_sea_surface_roughness.nc` | [Cartesian images](../data_types/level1/level1b.md) (sub-hourly, one antenna revolution) |
| `or_2025-01-15-11_sea_surface_roughness.nc` | [Roughness images](../data_types/level2/gridded/roughness_images.md) |
| `or_2025-01-15-11_sea_surface_roughness_mosaic.nc` | [Roughness image mosaics](../data_types/level2/gridded/roughness_mosaics.md) |
| `or_2025-01-15-11_currents.nc` | [Near-surface current maps](../data_types/level2/gridded/current_maps.md) |
| `or_2025-01-15-11_currents_profile.nc` | [Near-surface current profile maps](../data_types/level2/gridded/current_maps.md) |
| `or_2025-01-15-11_wavenumber_spectra_average.nc` | [Surface wave energy density spectra](../data_types/level2/trajectory/surface_waves.md) (2D wavenumber spectrum) |
| `or_2025-01-15-11_wave_spectrograms_average.nc` | [Surface wave energy density spectra](../data_types/level2/trajectory/surface_waves.md) (1D frequency spectrogram) |
| `or_2025-01-15-11_wave_parameters_average.nc` | [Peak and mean wave parameters](../data_types/level2/trajectory/surface_waves.md) |
| `or_2025-01-15-12_bathymetry.nc` | [Bathymetric maps](../data_types/level2/gridded/depth_maps.md) |
| `or_2025-08-23-12_sea_ice_drift.nc` | [Sea ice drift maps](../data_types/level2/gridded/sea_ice_drift.md) |
