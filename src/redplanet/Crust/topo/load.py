import xarray as xr

from redplanet.DatasetManager.master import _get_fpath_dataset


_dat_dem: xr.Dataset | None = None


def _get_dataset() -> xr.Dataset:
    if _dat_dem is None:
        raise ValueError('DEM dataset not loaded. Use `load` method to load the dataset.')
    return _dat_dem


def load(model: str = None) -> None:

    match model:
        case '200m':
            _load_200m_dem()
        case '463m':
            _load_463m_dem()
        case _:
            raise ValueError(f"Unknown model: '{model}'. Options are: '200m', '463m'.")


def _load_200m_dem() -> None:
    global _dat_dem
    if _dat_dem is not None and '200m' in _dat_dem.name:
        return

    fpath_dataset = _get_fpath_dataset('DEM_200m')

    _dat_dem = xr.open_zarr(fpath_dataset)
    _dat_dem = (
        _dat_dem
        ['Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2']
        .rio.write_crs(
            _dat_dem.spatial_ref.crs_wkt
        )
    )

def _load_463m_dem() -> None:
    global _dat_dem
    if _dat_dem is not None and '463m' in _dat_dem.name:
        return

    fpath_dataset = _get_fpath_dataset('DEM_463m')

    _dat_dem = xr.open_zarr(fpath_dataset)
    _dat_dem = (
        _dat_dem
        ['Mars_MGS_MOLA_DEM_mosaic_global_463m']
        .rio.write_crs(
            _dat_dem.spatial_ref.crs_wkt
        )
    )
