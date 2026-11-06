---
title: "Annex: Examples"
layout: default
nav_order: 9
has_children: true
---

# Annex: Examples

{: .informative }
> This annex is informative.

This annex gives a table of the file contents and a complete example file of each Level 1 data type and each Level 2 product, as the header of a NetCDF file in CDL, and for the Level 2 products a description of the product and of its retrieval.
The examples illustrate the definitions of the [SOMaR data types](../data_types/index.md) and of the Level 2 products but do not add to them; where an example and a definition differ, the definition applies.
Each page names, at its top, the data type and, for Level 2, the product type that it illustrates; the page of the data type defines the structure and variables of the file, and the variables themselves are defined under [Product variables](../data_types/product_variables.md).

## File contents

Each page begins with its file contents: the layout of the file, i.e. the forms its structure takes, followed by a table of its global attributes, variables, and groups, and the variable attributes that have a tier of their own, each with its tier and linked to its definition; the condition of a row, where one is given, states when its tier applies.
Where the tier of an item depends on the platform, the grid, or another item, the table gives the condition under which it applies: one of the forms of the layout, "moving platform", "fixed platform", "time-bounded grid", "local grid", "geographic grid", "rotated grid", or "north-oriented grid" (see [Rotated local grids](../georeferencing/index.md#rotated-local-grids)); the presence of another item, such as "with `crs`", or its value, such as "`sweep_mode = "pointing"`" or "`cartesian_resampling` other than `nearest_neighbor`". The table so also covers the forms of a file that the example does not show, such as a file from a fixed platform.
The table summarizes the definitions of the data type and product and, like the example, does not add to them.

## Reading the examples

The examples are illustrative: their platforms, stations, and institution are fictional, and they are not based on existing NetCDF files or real data.
They come from three platforms, each with its own [`station_id`](../metadata_attributes/optional_global.md#station_id) as the prefix of its file names: the moving R/V Ocean Research (`or`), the fixed Ocean Research Station on a North Sea coast (`ors`, 54.18° N, 7.89° E), and the fixed Arctic Ocean Research Station (`aors`, 78.98° N, 11.45° E).
Each example is a typical file: it carries the recommended items of its data type and product and the optional items that its retrieval method yields; of the recommended global attributes it shows only a few, all of which appear in the [example of the global attributes](../metadata_attributes/optional_global.md#example).
Every item that a file may omit is marked by a trailing comment with its tier, `// highly recommended`, `// recommended`, or `// optional`, as given by the [global attributes](../metadata_attributes/optional_global.md), the [processing parameters](../metadata_attributes/processing_parameters.md), and the tables of the page of its data type and, for a Level 2 product, its row in the product table there; unmarked items are required.
The markers apply to global attributes, variables, and groups, and to the variable attributes that have a tier of their own; the other variable attributes, such as [`units`](../metadata_attributes/variable_attributes.md#units) and [`long_name`](../metadata_attributes/variable_attributes.md#long_name), follow CF and the description of their variable.
An item that the tables recommend or make optional but that a minimal file must keep is marked `// required:` with the reason, such as one of the [bulk wave parameters](../data_types/averaged_windows.md#products), of which at least one is required, or an [`analysis_window_motion`](../metadata_attributes/processing_parameters.md#analysis_window_motion) other than its default.

Removing the marked items, together with the references to them in [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) and [`ancillary_variables`](../metadata_attributes/variable_attributes.md#ancillary_variables), leaves the minimal form of an example: the smallest file of its data type that complies with SOMaR, which omits the recommended [`product_type`](../metadata_attributes/optional_global.md#product_type) too.
It is written out for one example, the [near-surface current map](current_maps.md#minimal-form); the file contents table of each page gives the tiers from which the minimal forms of the other examples follow.
