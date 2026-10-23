---
title: "Annex: Example products"
layout: default
nav_order: 8
has_children: true
---

# Annex: Example products

{: .informative }
> This annex is informative.

This annex gives a table of the file contents and a complete example file of each product type, as the header of a NetCDF file in CDL, and for the Level 2 products a description of the product and of its retrieval.
The examples illustrate the definitions of the [SOMaR product types](../product_types/index.md) but do not add to them; where an example and a definition differ, the definition applies.

## File contents

The page of each product begins with its file contents: the layout of the file, i.e. the forms its structure takes, followed by a table of its global attributes, variables, and groups, and the variable attributes that have a tier of their own, each with its tier and linked to its definition.
Where the tier of an item depends on the platform, the grid, or another item, the table gives the condition under which it applies: one of the forms of the layout, "moving platform", "fixed platform", "time-bounded grid", "local grid", "geographic grid", "rotated grid", or "north-oriented grid" (see [Rotated local grids](../georeferencing/index.md#rotated-local-grids)); the presence of another item, such as "with `crs`", or its value, such as "`sweep_mode = "pointing"`" or "`cartesian_resampling` other than `nearest_neighbor`". The table so also covers the forms of a file that the example does not show, such as a file from a fixed platform.
The table summarizes the definitions of the product and, like the example, does not add to them.

## Reading the examples

The examples are illustrative: their platforms, stations, and institution are fictional, and they are not based on existing NetCDF files or real data.
Each example of a product is a typical file: it carries the recommended items of its product and the optional items that its retrieval method yields; of the recommended global attributes it shows only a few, all of which appear in the [example of the global attributes](../metadata_attributes/optional_global.md#example).
Every item that a file may omit is marked by a trailing comment with its tier, `// highly recommended`, `// recommended`, or `// optional`, as given by the [global attributes](../metadata_attributes/optional_global.md), the [processing parameters](../metadata_attributes/processing_parameters.md), and the tables of the product's category page and its row in the product-type table there; unmarked items are required.
The markers apply to global attributes, variables, and groups, and to the variable attributes that have a tier of their own; the other variable attributes, such as [`units`](../metadata_attributes/variable_attributes.md#units) and [`long_name`](../metadata_attributes/variable_attributes.md#long_name), follow CF and the description of their variable.
An item that the tables recommend but that a minimal file must keep is marked `// required:` with the reason, such as one of the [bulk wave parameters](../product_types/spatially_averaged.md#product-types), of which at least one is required.

Removing the marked items, together with the references to them in [`grid_mapping`](../metadata_attributes/variable_attributes.md#grid_mapping) and [`ancillary_variables`](../metadata_attributes/variable_attributes.md#ancillary_variables), leaves the minimal form of an example: the smallest file of its product that complies with SOMaR.
It is given under each example, as for the [near-surface current map](current_maps.md#minimal-form).
