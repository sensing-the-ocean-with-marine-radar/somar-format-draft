---
title: Storage recommendations
layout: default
nav_order: 7
---

# Storage recommendations

SOMaR files are written in the NetCDF-4 format (see [Metadata](../metadata_attributes/index.md)), whose variables can be compressed and stored in chunks.
The following recommendations keep files small and quick to read with any NetCDF library; like the [file naming](../file_naming/index.md), they are not part of [compliance](../metadata_attributes/mandatory_global.md#compliance).

## Compression

Data variables should be compressed losslessly, with the deflate filter of NetCDF-4 at level 4 and the shuffle filter:

- **Deflate** is the zlib compression of zip and gzip. Each chunk of a variable is compressed when it is written and decompressed when it is read, so that the values read are identical to those written. Levels above 4 make files only slightly smaller but writing much slower.
- **Shuffle** reorders the bytes within each chunk before deflate, first the most significant byte of every value, then the next, and so on. Since neighboring values, such as the backscatter of adjacent range gates, mostly share their high bytes, the reordered chunk compresses better. It is reversible and costs little time.

Both filters are part of every NetCDF-4 library, so that a file compressed with them can be read without further software.
Other filters, such as Zstandard or Blosc, need plugins that a reader may not have installed, and lossy methods, including the quantization of CF (section 8.4), change the values; neither should be used.

Backscatter may be stored as floating-point values or as integers, packed with [`scale_factor`](../metadata_attributes/variable_attributes.md#scale_factor) and [`add_offset`](../metadata_attributes/variable_attributes.md#add_offset) where the values are scaled.
Integers keep the values exactly only where they are at the resolution of the analog-to-digital converter, as in [`polar_raw`](../data_types/polar_raw.md) and in images resampled by `nearest_neighbor`: there, the smallest type that holds that resolution, such as `ubyte` for 8 bits or `ushort` for up to 16 bits, makes the file smallest, as in the [example](../annex/level1a.md#example).
Averaged or interpolated values, such as pulse-averaged data or images resampled by interpolation, fall between the integer steps and should be stored as `float`, since rounding them would be lossy.

In netCDF4-python, the filters are set with `zlib=True, complevel=4, shuffle=True` when a variable is created, in xarray with the encoding `{"zlib": True, "complevel": 4, "shuffle": True}`, and in the C library with `nc_def_var_deflate(ncid, varid, 1, 1, 4)`; an existing file is compressed with `nccopy -d 4 -s in.nc out.nc`.

## Chunking

A chunk is the block of a variable that is compressed and read as a whole.
Its shape should follow the way the data are usually read, so that a reader decompresses no more than it needs, and its size should be at least about 100 KiB; one image per chunk is preferred even where the image is larger than a few MiB, since images are usually read whole:

- **Sweeps** (`polar_raw`, `polar_pulse_averaged`): blocks of consecutive whole rays, with all range gates, such as a quarter of a revolution.
- **Image cubes** (`polar_image_cube`, `cartesian_image_cube`): one image per chunk, `(1, azimuth, range)` or `(1, y, x)`.
- **Gridded data** (`gridded_pixels`, `gridded_windows`): one grid per chunk, i.e. the whole grid of a time-bounded group, or `(1, latitude, longitude)` or `(1, y, x)` on the single grid of a fixed platform.
- **Windows** (`discrete_windows`, `averaged_windows`): the whole `time` dimension for bulk values, and one spectrum per chunk, such as `(1, northward_wave_wavenumber, eastward_wave_wavenumber)`, for spectra.

The CDL that `ncdump -s` prints shows the storage of each variable in special attributes, which `ncgen` also accepts; for a sweep of 4500 rays and 1000 range gates, chunked in quarters of the revolution of about 2 MiB each:

```
// excerpt: storage of the data variable of a sweep
        ushort backscatter_amplitude(time, range) ;
                backscatter_amplitude:_Storage = "chunked" ;
                backscatter_amplitude:_ChunkSizes = 1125, 1000 ;
                backscatter_amplitude:_DeflateLevel = 4 ;
                backscatter_amplitude:_Shuffle = "true" ;
```

A chunk larger than the chunk cache of the reading library is decompressed again on every access.
The default cache of HDF5 is 1 MiB per variable; a reader that reads large chunks repeatedly, such as one pixel through all images of a cube, should enlarge it, with `set_var_chunk_cache` in netCDF4-python, `rdcc_nbytes` in h5py, or `nc_set_var_chunk_cache` in the C library.
