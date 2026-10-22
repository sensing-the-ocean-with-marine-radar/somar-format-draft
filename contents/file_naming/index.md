---
title: File naming recommendations
layout: default
nav_order: 6
---

# File naming recommendations

SOMaR files should be named so that a file's platform, time coverage, and product can be identified without opening it, following the pattern:

```
<station_id>_<YYYY-MM-DD>-<HH>[-<MM>]_<product_type>.nc
```

- `station_id` is a short identifier of lowercase letters and digits (`[a-z0-9]+`) for the originating platform, e.g. `or` for the fictional R/V Ocean Research used throughout this document's examples. It is chosen by the data provider and needs to be unique only among the provider's platforms; files from different providers are told apart by the [`platform`](../metadata_attributes/optional_global.md#platform) and [`institution`](../metadata_attributes/optional_global.md#institution) attributes. The identifier may also be recorded in the `station_id` global attribute.
- `<YYYY-MM-DD>-<HH>` is the UTC date and hour at which the file's data coverage begins. Most SOMaR products are aggregated into one file per hour; sub-hourly products additionally append a two-digit `-<MM>` minute field.
- `product_type` is the value of the file's [`product_type`](../metadata_attributes/mandatory_global.md#product_type) attribute, which identifies the product (see [SOMaR product types](../product_types/index.md)).

| Example filename | Product |
|---|---|
| `or_2025-01-15-11-00_radar_polar_raw.nc` | [Radar "raw" data](../annex/level1a.md) (sub-hourly) |
| `or_2025-01-15-11-00_radar_polar_regularized.nc` | [Polar image sequences](../annex/level1b_polar.md) (sub-hourly) |
| `or_2025-01-15-11-00_radar_polar_averaged.nc` | [Pulse-averaged pointing data](../annex/level1b_pointing.md) (sub-hourly) |
| `or_2025-01-15-11-00_radar_cartesian.nc` | [Cartesian image sequences](../annex/level1b_cartesian.md) (sub-hourly) |
| `or_2025-01-15-11_relative_roughness.nc` | [Relative roughness images](../annex/relative_roughness_images.md) |
| `or_2025-01-15-11_relative_roughness_mosaic.nc` | [Relative roughness image mosaics](../annex/relative_roughness_mosaics.md) |
| `or_2025-01-15-11_currents.nc` | [Near-surface current maps](../annex/current_maps.md) |
| `or_2025-01-15-11_currents_profile.nc` | [Near-surface current profile maps](../annex/current_profile_maps.md) |
| `or_2025-01-15-12_bathymetry.nc` | [Bathymetric maps](../annex/depth_maps.md) |
| `or_2025-08-23-12_sea_ice_drift.nc` | [Sea ice drift maps](../annex/sea_ice_drift.md) |
| `or_2025-01-15-11_wave_wavenumber_spectra.nc` | [Surface wave two-dimensional wavenumber spectra](../annex/wave_wavenumber_spectra.md) |
| `or_2025-01-15-11_wave_frequency_direction_spectra.nc` | [Surface wave frequency-direction spectra](../annex/wave_frequency_direction_spectra.md) |
| `or_2025-01-15-11_wave_frequency_spectra.nc` | [Surface wave one-dimensional frequency spectra](../annex/wave_frequency_spectra.md) |
| `or_2025-01-15-11_wave_parameters.nc` | [Peak and mean wave parameters](../annex/wave_parameters.md) |
