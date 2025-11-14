def preprocess_dem(dem_path: str) -> tuple:
    """
    Pre-process digital elevation model (DEM), in line standard preprocessing steps
    outlined in pysheds documentation
    
    NOTE: First call to this function is slow (~10s) as it imports pysheds.
    Subsequent calls will be fast. This is normal due to pysheds' heavy dependencies
    (numba, scipy, etc).

    Parameters
    ----------
    dem_path: str
      Path to DEM raster file

    Returns
    -------
    grid: pysheds.sgrid.sGrid
      Grid view of digitial elevation model (DEM) raster

    acc: pysheds.sview.Raster
      A pysehds flow accumulation raster

    fdir: pysheds.sview.Raster
      A pysheds flow direction raster
    """
    # Lazy import to avoid slow module startup time (~10s saved on import)
    from pysheds.grid import Grid
    
    grid = Grid.from_raster(dem_path)
    dem = grid.read_raster(dem_path)
    pit_filled = grid.fill_pits(dem)
    flooded = grid.fill_depressions(pit_filled)
    inflated = grid.resolve_flats(flooded)
    fdir = grid.flowdir(inflated)
    acc = grid.accumulation(fdir)
    return (grid, fdir, acc)


def mosaic_to_new_raster(raster_paths: list, out_path: str):
    """
    Combine a set of rasters and write to a new file.

    Parameters
    ----------
    raster_paths: list
      List of str, each being a path to an existing raster file
    out_path: str
      Path to write new mosiac raster to
    """
    import rasterio
    import rasterio.merge

    tiles = [rasterio.open(r) for r in raster_paths]
    mosaic, transform = rasterio.merge.merge(tiles)

    # get and update metadata for mosaic raster, write to dis
    out_meta = tiles[0].meta.copy()
    out_meta.update(
        {"width": mosaic.shape[2], "height": mosaic.shape[1], "transform": transform}
    )
    with rasterio.open(out_path, "w", **out_meta) as dst:
        dst.write(mosaic)
