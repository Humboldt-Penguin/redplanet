import numpy as np
import xarray as xr
import pyshtools as pysh

from redplanet.Crust.moho.load import (
    get_dataset,
    _get_shape,
)
from redplanet.helper_functions.coordinates import (
    _verify_coords,
    _slon2plon,
)





def get(
    lon                 : float | list | np.ndarray,
    lat                 : float | list | np.ndarray,
    as_crthick          : bool = False,
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
    dat_moho, _ = get_dataset()

    if as_crthick:
        dat_shape = _get_shape()
        dat_full = dat_shape - dat_moho
    else:
        dat_full = dat_moho


    if interpolate:
        data = dat_full.interp(
            lon = lon,
            lat = lat,
            method = 'linear',
            assume_sorted = True
        )
    else:
        data = dat_full.sel(
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
