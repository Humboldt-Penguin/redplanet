import numpy as np
import xarray as xr

from redplanet.Mag.sh.load import get_dataset
from redplanet.helper_functions.coordinates import (
    _verify_coords,
    _slon2plon,
)



def get(
    lon                 : float | list | np.ndarray,
    lat                 : float | list | np.ndarray,
    quantity            : str  = 'total',
    as_xarray           : bool = False,
    return_exact_coords : bool = False,
) -> float | np.ndarray | list[np.ndarray, np.ndarray, np.ndarray] | xr.Dataset:

    ## input validation
    if as_xarray and return_exact_coords:
        raise ValueError("Can't return both xarray and exact coordinates. Choose one.")

    quantities = list(_dat_mag.data_vars)
    if quantity not in quantities:
        raise ValueError(f'Unknown quantity: \"{quantity}\".\nOptions are: \"{"\", \"".join(quantities)}\".')

    _verify_coords(lon, lat)
    lon = _slon2plon(lon)


    ## get data
    dat_mag = get_dataset()
    data = dat_mag[quantity].sel(
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
