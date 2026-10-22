---
title: Quality flags
layout: default
parent: Metadata
nav_order: 5
---

# Quality flags

The Level 2 maps and spatially averaged products should carry a `measurement_quality` variable of type `ubyte`, a bit flag in the sense of [CF][cf-flags]: 0 means that the measurement passed all checks, and each bit that is set marks a check that it failed.
Relative roughness images and mosaics, which result from no retrieval that could fail, carry no quality flag, nor do the Level 1 products.
A product without quality control omits the variable rather than storing 0, so that a missing `measurement_quality` means that no checks were applied.
The checks depend on the retrieval method and the processor, and are therefore defined by each file through the [`flag_masks`](variable_attributes.md#flag_masks) and [`flag_meanings`](variable_attributes.md#flag_meanings) attributes.
The following flag meanings are recommended for the checks they describe, so that the same check carries the same name in the files of different processors; the thresholds are set by the processor.

- `bathymetry_fit_boundaries_reached`: the water depth of a fit lies at a boundary of the range searched.
- `correlation_coefficient_too_low`: the peak correlation coefficient of a cross-correlation lies below a threshold.
- `current_fit_boundaries_reached`: the current of a fit lies at a boundary of the range searched.
- `difference_from_all_spatial_neighbors_exceeds_threshold`: the value differs from that of each of its spatial neighbors by more than a threshold.
- `difference_from_all_temporal_neighbors_exceeds_threshold`: the value differs from that of each of its temporal neighbors, i.e. the measurements at the same position in adjacent measurement periods, by more than a threshold.
- `forward_and_backward_cross_correlation_results_too_different`: the drift vectors of the forward and backward retrievals differ by more than a threshold.
- `invalid_peak`: the spectral peak from which the peak wave parameters are taken fails a validity check.
- `measurement_failed`: the retrieval yielded no value.
- `measurement_outside_area_of_validity`: the measurement lies where the retrieval is not valid, such as in water too deep for a bathymetry retrieval.
- `number_of_spatial_neighbors_below_threshold`: fewer spatial neighbors than a threshold hold a valid value.
- `number_of_temporal_neighbors_below_threshold`: fewer temporal neighbors than a threshold hold a valid value.
- `rain_contamination`: rain affects the radar images from which the measurement is retrieved.
- `sea_ice_speed_too_high`: the speed of the sea ice drift exceeds a threshold.
- `standard_error_above_threshold`: the standard error of the retrieval exceeds a threshold.
- `wave_steepness_above_threshold`: the wave steepness exceeds a threshold.

[cf-flags]: https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.html#flags
