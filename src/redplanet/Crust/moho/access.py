import numpy as np
import pandas as pd
import xarray as xr

from redplanet.helper_functions import _verify_coords, _slon2plon
from redplanet.DatasetManager.master import _get_fpath_dataset
from redplanet.Crust.moho.load import _get_dataset, _model_info



def get_registry() -> pd.DataFrame:
    registry = pd.read_csv(
        _get_fpath_dataset('moho_registry'),
        usecols = ['model_name'],
    )
    registry = registry['model_name'].str.split('-', expand=True)
    registry.columns = ['interior_model', 'insight_thickness', 'rho_south', 'rho_north']
    registry.iloc[:,1:] = registry.iloc[:,1:].astype(int)
    return registry



def get_model_info() -> dict[ str, str|int ] | None:
    if _model_info is not None:
        return _model_info.copy()
    return None



def get(
    lon        : float | list | np.ndarray,
    lat        : float | list | np.ndarray,
    interpolate: bool = False,
    as_xarray  : bool = False,
) -> float | np.ndarray | xr.Dataset:

    dat_moho = _get_dataset()

    ## input validation
    # lon = np.array(lon)   # skip conversion since `interp` doesn't work with singleton array indices, for some reason
    # lat = np.array(lat)
    _verify_coords(lon, lat)
    lon = _slon2plon(lon)

    ## get data
    if interpolate:
        data = dat_moho.interp(
            lon = lon,
            lat = lat,
            method = 'linear',
            assume_sorted = True
        )
    else:
        data = dat_moho.sel(
            lon = lon,
            lat = lat,
            method = 'nearest'
        )

    if not as_xarray:
        data = data.values
        ## convert singleton numpy array to scalar
        if data.shape == (): data = data.item()

    return data
