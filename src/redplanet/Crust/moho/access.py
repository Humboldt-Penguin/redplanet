import copy

import numpy as np
import pandas as pd
import xarray as xr

from redplanet.Crust.moho.load import get_dataset, _model_info
from redplanet.DatasetManager.master import _get_fpath_dataset
from redplanet.helper_functions.coordinates import (
    _verify_coords,
    _slon2plon,
)



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
        return copy.deepcopy(_model_info)
    return None



def get(
    lon                 : float | list | np.ndarray,
    lat                 : float | list | np.ndarray,
    interpolate         : bool = False,
    as_xarray           : bool = False,
    return_exact_coords : bool = False,
) -> float | np.ndarray | list[np.ndarray, np.ndarray, np.ndarray] | xr.Dataset:

    ## input validation
    if as_xarray and return_exact_coords:
        raise ValueError("Can't return both xarray and exact coordinates. Choose one.")

    _verify_coords(lon, lat)
    lon = _slon2plon(lon)
    # lon = np.array(lon)   # skip conversion since `interp` doesn't work with singleton array indices, for some reason -- TODO: is the solution to use `np.atleast_1d`??? idk when i made this change unfortunately, dig through git history
    # lat = np.array(lat)


    ## get data
    dat_moho = get_dataset()
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


    ## Case 1: return type `xarray.Dataset`
    if as_xarray:
        return data

    ## Case 2: return type `list[np.ndarray, np.ndarray, np.ndarray]` (data with coords)
    if return_exact_coords:
        return data.values, data.lon.values, data.lat.values

    ## Case 3: return type `float` or `np.ndarray` (just data)
    data = data.values
    ## convert singleton numpy array to scalar
    if data.shape == (): data = data.item()
    return data
