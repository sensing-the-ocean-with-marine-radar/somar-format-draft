---
title: "Annex: Example products"
layout: default
nav_order: 8
has_children: true
---

# Annex: Example products

{: .informative }
> This annex is informative.

This annex gives a complete example file of each Level 2 product type, as the header of a NetCDF file in CDL, together with a description of the product and of its retrieval.
The examples illustrate the definitions of the [SOMaR product types](../product_types/index.md) but do not add to them; where an example and a definition differ, the definition applies.

## Reading the examples

The example of each product is a typical file: it carries the recommended items, and the optional items that its retrieval method yields.
Every item that a file may omit is marked by a trailing comment with its tier, `// highly recommended`, `// recommended`, or `// optional`, as given by the [global attributes](../metadata_attributes/optional_global.md), the [processing parameters](../product_types/level2/index.md#processing-parameters), and the tables of the product: for a Level 1 product those of its page, for a Level 2 product those of its category page and its row in the product-type table there; unmarked items are required.
The markers apply to global attributes, variables, and groups, and to the variable attributes that have a tier of their own; the other variable attributes, such as `units` and `long_name`, follow CF and the description of their variable.
An item that the tables recommend but that a minimal file must keep is marked `// required:` with the reason, such as one of the [bulk wave parameters](../product_types/level2/spatially_averaged.md#product-types), of which at least one is required, or `platform_is_mobile` in a file from a moving platform.

Removing the marked items, together with the references to them in `grid_mapping` and `ancillary_variables`, leaves the minimal form of an example: the smallest file of its product that complies with SOMaR.
For the [near-surface current map](current_maps.md#example), it is:

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
