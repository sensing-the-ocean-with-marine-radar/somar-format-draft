---
title: Metadata
layout: default
nav_order: 3
---

# Metadata

Every SOMaR NetCDF file carries a common core of metadata, stored as global attributes, variable attributes, and variables, in addition to whatever data variables and attributes are specific to its own product (documented alongside each product under [SOMaR data types](../data_types/index.md)).
This chapter documents that shared metadata: the [mandatory global attributes](mandatory_global.md) that every SOMaR file must carry, [optional global attributes](optional_global.md) that are recommended where applicable, the [variable attributes](variable_attributes.md) attached to individual variables, the [radar and calibration parameters](radar_parameters.md) that describe how raw instrument counts relate to physical quantities, the [file naming](file_naming.md) convention used to identify a file's platform, time, and product without opening it, and the [georeferencing](georeferencing.md) conventions used to locate SOMaR's time-bounded local grids and trajectory points in space.

## Variables and attributes

NetCDF stores information in two ways.
A variable is a named array of values with a type, dimensions, and attributes of its own.
An attribute is a label attached either to a variable or, as a global attribute, to the file as a whole.

```
variables:
        float prt(time) ;                  // a variable
                prt:units = "seconds" ;    // an attribute of that variable

// global attributes:
                :title = "..." ;           // an attribute of the file
```

As a rule of thumb, a quantity that can change from pulse to pulse or from sweep to sweep, or that is a number with units, is stored as a variable; a description of a variable or of the file is stored as an attribute.

## Reading the tables

Attributes are tabulated with three columns: the attribute name, its permitted values, and a description.
Variables are tabulated with three columns: the variable name, its values, i.e. its type and dimension followed by its units or permitted values, and a description.
In both cases, the convention that defines the attribute or variable is named in small print under it, for FM 301 and CfRadial together with the table or section; it is one of five:

- **CF**: the attribute is defined by the [NetCDF Climate and Forecast (CF) Metadata Conventions](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html), version 1.13, and is used as defined there.
- **ACDD**: the attribute is defined by the [Attribute Convention for Data Discovery (ACDD)](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3), version 1.3, which complements CF with attributes describing who created a dataset, under which license, and what time span and area it covers.
- **FM 301**: the attribute or variable is defined by the WMO-CF Radial profile [FM 301](https://library.wmo.int/records/item/35625-manual-on-codes-volume-i-2-international-codes) of the WMO Manual on Codes (WMO-No. 306, Volume I.2), the international standard for radar data in polar coordinates. SOMaR follows it for [Level 1a data](../data_types/level1/level1a.md) and for the [radar parameters](radar_parameters.md), leaving out what a marine radar does not need.
- **CfRadial**: the attribute or variable is defined by the [CfRadial format](https://github.com/NCAR/CfRadial/tree/master/docs), version 2.1 (draft of 2019), from which FM 301 was developed. SOMaR follows it only for the parameters of moving platforms and the georeference corrections, which FM 301 does not include.
- **SOMaR**: the attribute is defined by none of these conventions and is introduced by this document.
