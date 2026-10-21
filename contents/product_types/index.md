---
title: SOMaR product types
layout: default
nav_order: 5
has_children: true
---

# SOMaR product types

SOMaR products are organized by processing level, from radar data as recorded by the instrument to derived geophysical variables.
Every SOMaR NetCDF file carries a mandatory global attribute, `product_type`, which uniquely identifies the product's structure and schema.

| Level | Product | `product_type` |
|:---:|---|---|
| **L1a** | [Radar "raw" data](level1/level1a.md) | `radar_polar_raw` |
| **L1b** | [Polar image sequences](level1/level1b_polar.md) | `radar_polar_regularized` |
| **L1b** | [Cartesian image sequences](level1/level1b_cartesian.md) | `radar_cartesian` |
| **L2a** | [Roughness images](level2/roughness_images.md) | `sea_surface_roughness` |
| **L2a** | [Roughness image mosaics](level2/roughness_mosaics.md) | `sea_surface_roughness_mosaic` |
| **L2a** | [Near-surface current maps](level2/current_maps.md) | `currents` |
| **L2a** | [Near-surface current profile maps](level2/current_profile_maps.md) | `currents_profile` |
| **L2a** | [Bathymetric maps](level2/depth_maps.md) | `bathymetry` |
| **L2a** | [Sea ice drift maps](level2/sea_ice_drift.md) | `sea_ice_drift` |
| **L2a** | [Surface wave two-dimensional wavenumber spectra](level2/wave_wavenumber_spectra.md) | `wave_wavenumber_spectra` |
| **L2b** | [Surface wave frequency-direction spectra](level2/wave_frequency_direction_spectra.md) | `wave_frequency_direction_spectra` |
| **L2b** | [Surface wave one-dimensional frequency spectra](level2/wave_frequency_spectra.md) | `wave_frequency_spectra` |
| **L2b** | [Peak and mean wave parameters](level2/wave_parameters.md) | `wave_parameters` |
{: .product-table }

[Level 1](level1/index.md) products retain the radar's own measurement (backscatter amplitude or power in uncalibrated units), either ray by ray in the sensor's polar geometry ([Level 1a](level1/level1a.md)) or as individual images with a regular azimuth axis ([Level 1b polar](level1/level1b_polar.md)) or on a local Cartesian grid ([Level 1b Cartesian](level1/level1b_cartesian.md)).
[Level 2](level2/index.md) products are geophysical variables, either retrieved directly from image sequences (Level 2a) or derived from those retrievals (Level 2b).
Each page below documents the product-specific dimensions, variables, and attributes, with an example, in addition to the [shared metadata](../metadata_attributes/index.md).
The tables state for each variable and attribute whether it is required, recommended, or optional:

- **Required** items are those without which a reader would misread the values or misplace them in time or space: the coordinates, the data variables that define the product, and the parameters that change what a value means.
- **Recommended** items document how the data were obtained and how good they are, such as the processing parameters, the quality flag, and retrieval diagnostics. A file should carry them where its producer can supply them.
- **Optional** items are further diagnostics and details that a producer may add.

Only the required items are part of [compliance](../metadata_attributes/mandatory_global.md#compliance).
Sectors of the field of view that are shadowed or blanked are recorded in the `radar_parameters` group (see [Obstructed sectors](../metadata_attributes/radar_parameters.md#obstructed-sectors)).

{: .open_issue }
> Radar product types that are not yet defined:
> * Wave spectrum partitioning results (wave parameters for wind sea and swell systems),
> * Wind speed and direction retrieved from radar backscatter,
> * Products for coastal applications, such as the mapping of intertidal areas.

## Examples

The example on each product page is a typical file: it carries the recommended items, and the optional items that its retrieval method yields.
Every item that a file may omit is marked by a trailing comment with its tier, `// highly recommended`, `// recommended`, or `// optional`, as given by the [global attributes](../metadata_attributes/optional_global.md) and the tables of the product page; unmarked items are required.
The markers apply to global attributes, variables, and groups, and to the variable attributes that have a tier of their own; the other variable attributes, such as `units` and `long_name`, follow CF and the description of their variable.
An item that the tables recommend but that a minimal file must keep is marked `// required:` with the reason, such as one of the [bulk wave parameters](level2/wave_parameters.md#variables), of which at least one is required.

Removing the marked items, together with the references to them in `grid_mapping` and `ancillary_variables`, leaves the minimal form of an example: the smallest file of its product that complies with SOMaR.
For the [near-surface current map](level2/current_maps.md#example), it is:

```
// minimal form of the near-surface current map example
netcdf or_2025-01-15-11_currents {

// global attributes:
                :Conventions = "CF-1.13, ACDD-1.3, SOMaR-0.5-draft" ;
                :platform_is_mobile = "true" ; // required: the platform moves
                :product_type = "currents" ;

group: time_20250115110031 {
  dimensions:
        latitude = 17 ;
        longitude = 17 ;
  variables:
        double time ;
                time:calendar = "standard" ;
                time:long_name = "start time of current measurement" ;
                time:standard_name = "time" ;
                time:units = "seconds since 1970-01-01T00:00:00Z" ;
        double longitude(longitude) ;
                longitude:long_name = "center longitude of current measurement" ;
                longitude:standard_name = "longitude" ;
                longitude:units = "degrees_east" ;
        double latitude(latitude) ;
                latitude:long_name = "center latitude of current measurement" ;
                latitude:standard_name = "latitude" ;
                latitude:units = "degrees_north" ;
        double eastward_sea_water_velocity(latitude, longitude) ;
                eastward_sea_water_velocity:long_name = "eastward component of the near-surface current velocity" ;
                eastward_sea_water_velocity:standard_name = "eastward_sea_water_velocity" ;
                eastward_sea_water_velocity:units = "m s-1" ;
                eastward_sea_water_velocity:_FillValue = NaN ;
        double northward_sea_water_velocity(latitude, longitude) ;
                northward_sea_water_velocity:long_name = "northward component of the near-surface current velocity" ;
                northward_sea_water_velocity:standard_name = "northward_sea_water_velocity" ;
                northward_sea_water_velocity:units = "m s-1" ;
                northward_sea_water_velocity:_FillValue = NaN ;
  } // group time_20250115110031

// ... additional time_<YYYYMMDDHHMMSS> groups follow the same layout, one per measurement period ...
}
```
