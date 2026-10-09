---
title: Metadata attributes
layout: default
nav_order: 3
---

# Metadata attributes

Every SOMaR NetCDF file carries a common core of global and variable-level metadata attributes, in addition to whatever data variables and attributes are specific to its own product (documented alongside each product under [SOMaR data types](../data_types/index.md)).
This chapter documents that shared metadata: the [mandatory global attributes](mandatory_global.md) that every SOMaR file must carry, [optional global attributes](optional_global.md) that are recommended where applicable, the [variable attributes](variable_attributes.md) attached to individual variables, the [radar and calibration parameters](radar_parameters.md) that describe how raw instrument counts relate to physical quantities, the [file naming](file_naming.md) convention used to identify a file's platform, time, and product without opening it, and the [georeferencing](georeferencing.md) conventions used to locate SOMaR's time-bounded local grids and trajectory points in space.

Attributes are tabulated with five columns: the attribute name, the convention that defines it, its permitted values, a description, and an example.
The "Defined by" column takes one of three values:

- **CF**: the attribute is defined by the [NetCDF Climate and Forecast (CF) Metadata Conventions](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html), version 1.13, and is used as defined there.
- **ACDD**: the attribute is defined by the [Attribute Convention for Data Discovery (ACDD)](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3), version 1.3, which complements CF with attributes describing who created a dataset, under which license, and what time span and area it covers.
- **SOMaR**: the attribute is defined by neither convention and is introduced by this document.
