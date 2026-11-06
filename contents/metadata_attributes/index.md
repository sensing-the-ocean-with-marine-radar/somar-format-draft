---
title: Metadata
layout: default
nav_order: 3
---

# Metadata

Every SOMaR NetCDF file carries a common core of metadata, stored as global attributes, variable attributes, and variables, in addition to whatever data variables and attributes are specific to its own data type and product (defined under [SOMaR data types](../data_types/index.md), whose [product variables](../data_types/product_variables.md) hold the data). All SOMaR files must be written in the NetCDF-4 format (the HDF5-based enhanced data model, `NETCDF4`), which provides the hierarchical groups (such as sweep groups and time-bounded grids) and unsigned integer types (such as `ubyte`) that SOMaR uses; groups follow the scoping rules of CF 1.8 and later.
This chapter documents that shared metadata, one topic per page, from the global attributes to the groups of radar, georeference correction, and wave calibration parameters.
For conventions locating SOMaR's polar data and time-bounded local grids in space, see [Georeferencing](../georeferencing/index.md); for file naming on disk, see [File naming](../file_naming/index.md).

## Reading the tables

Attributes are tabulated with three columns: the attribute name, its permitted values, and a description.
Variables are tabulated with three columns: the variable name, its values, i.e. its type and dimension followed by its units or permitted values, and a description.
The rows are in alphabetical order, except in the tables of the coordinates and other structural variables on the pages of the [data types](../data_types/index.md#choosing-the-data-type), which follow the structure of the file.
In both cases, the convention that defines the attribute or variable is named in small print under it, for FM 301 and CfRadial together with the table or section; it is one of five:

- **CF**: the attribute is defined by the [NetCDF Climate and Forecast (CF) Metadata Conventions][cf], version 1.13, and is used as defined there.
- **ACDD**: the attribute is defined by the [Attribute Convention for Data Discovery (ACDD)][acdd], version 1.3, which complements CF with attributes describing who created a dataset, under which license, and what time span and area it covers.
- **FM 301**: the attribute or variable is defined by the WMO-CF Radial profile [FM 301][fm301] of the WMO Manual on Codes (WMO-No. 306, Volume I.2), the international standard for radar data in polar coordinates. SOMaR follows it for the [polar data types](../data_types/polar_raw.md#relation-to-fm-301-and-cfradial) and the [radar parameters](radar_parameters.md).
- **CfRadial**: the attribute or variable is defined by the [CfRadial format][cfradial], version 2.1 (draft of 2019), from which FM 301 was developed. SOMaR follows it for moving platforms and georeference corrections, which FM 301 does not include.
- **SOMaR**: the attribute is defined by none of these conventions and is introduced by this document.

[acdd]: https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
[cf]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html
[cfradial]: https://github.com/NCAR/CfRadial/tree/master/docs
[fm301]: https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes
