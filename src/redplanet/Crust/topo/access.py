import numpy as np
import xarray as xr

from redplanet.helper_functions import _verify_coords, _plon2slon
from redplanet.Crust.topo.load import _get_dataset


def get(
    lon        : float | list | np.ndarray,
    lat        : float | list | np.ndarray,
    interpolate: bool = False,
    as_xarray  : bool = False,
) -> float | np.ndarray | xr.Dataset:

    dat_dem = _get_dataset()

    ## input validation
    # lon = np.array(lon)   # skip conversion since `interp` doesn't work with singleton array indices, for some reason
    # lat = np.array(lat)
    _verify_coords(lon, lat)
    lon = _plon2slon(lon)

    ## get data
    if interpolate:
        data = dat_dem.interp(
            lon = lon,
            lat = lat,
            method = 'linear',
            assume_sorted = True
        )
    else:
        data = dat_dem.sel(
            lon = lon,
            lat = lat,
            method = 'nearest'
        )

    if not as_xarray:
        data = data.values
        ## convert singleton numpy array to scalar
        if data.shape == (): data = data.item()

    return data
