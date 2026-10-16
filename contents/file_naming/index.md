---
title: File naming recommendations
layout: default
nav_order: 6
---

# File naming recommendations

SOMaR files should be named so that a file's platform, time coverage, and product can be identified without opening it, following the pattern:

```
<station_id>_<YYYY-MM-DD>-<HH>[-<MM>]_<product_name>.nc
```

- `station_id` is a short, lowercase identifier for the originating platform, e.g. `or` for the fictional R/V Ocean Research used throughout this document's examples. It is chosen by the data provider and needs to be unique only among the provider's platforms; files from different providers are told apart by the [`platform` and `institution` attributes](../metadata_attributes/optional_global.md). The identifier may also be recorded in the `station_id` global attribute.
- `<YYYY-MM-DD>-<HH>` is the UTC date and hour at which the file's data coverage begins. Most SOMaR products are aggregated into one file per hour; sub-hourly products additionally append a two-digit `-<MM>` minute field.
- `product_name` is a short, snake_case name identifying the product, matching the canonical `product_type` attribute defined for the product (e.g. `radar_polar_raw`, `radar_polar_regularized`, `radar_cartesian`, `sea_surface_roughness`, `sea_surface_roughness_mosaic`, `currents`, `currents_profile`, `wave_wavenumber_spectra`, `wave_frequency_direction_spectra`, `wave_frequency_spectra`, `wave_parameters`, `bathymetry`, `sea_ice_drift`; see [SOMaR product types](../product_types/index.md)).

| Example filename | Product |
|---|---|
| `or_2025-01-15-11-00_radar_polar_raw.nc` | [Radar "raw" data](../product_types/level1/level1a.md) (sub-hourly) |
| `or_2025-01-15-11-00_radar_polar_regularized.nc` | [Polar images](../product_types/level1/level1b_polar.md) (sub-hourly) |
| `or_2025-01-15-11-00_radar_cartesian.nc` | [Cartesian images](../product_types/level1/level1b_cartesian.md) (sub-hourly) |
| `or_2025-01-15-11_sea_surface_roughness.nc` | [Roughness images](../product_types/level2/roughness_images.md) |
| `or_2025-01-15-11_sea_surface_roughness_mosaic.nc` | [Roughness image mosaics](../product_types/level2/roughness_mosaics.md) |
| `or_2025-01-15-11_currents.nc` | [Near-surface current maps](../product_types/level2/current_maps.md) |
| `or_2025-01-15-11_currents_profile.nc` | [Near-surface current profile maps](../product_types/level2/current_maps.md) |
| `or_2025-01-15-11_wave_wavenumber_spectra.nc` | [Surface wave two-dimensional wavenumber spectra](../product_types/level2/wave_wavenumber_spectra.md) |
| `or_2025-01-15-11_wave_frequency_direction_spectra.nc` | [Surface wave frequency-direction spectra](../product_types/level2/wave_frequency_direction_spectra.md) |
| `or_2025-01-15-11_wave_frequency_spectra.nc` | [Surface wave one-dimensional frequency spectra](../product_types/level2/wave_frequency_spectra.md) |
| `or_2025-01-15-11_wave_parameters.nc` | [Peak and mean wave parameters](../product_types/level2/wave_parameters.md) |
| `or_2025-01-15-12_bathymetry.nc` | [Bathymetric maps](../product_types/level2/depth_maps.md) |
| `or_2025-08-23-12_sea_ice_drift.nc` | [Sea ice drift maps](../product_types/level2/sea_ice_drift.md) |
