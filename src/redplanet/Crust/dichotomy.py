from pathlib import Path

import numpy as np
import xarray as xr

from redplanet.DatasetManager.master import _get_fpath_dataset
from redplanet.helper_functions import _verify_coords, _slon2plon



def is_above_dichotomy(
    lon       : float | list | np.ndarray,
    lat       : float | list | np.ndarray,
    as_xarray : bool = False,
) -> bool | np.ndarray | xr.DataArray:
    """
    Denote:
        - len(lons) = x
        - len(lats) = y

    Returns shape(y, x) boolean array.
    """
    ## input validation
    _verify_coords(lon, lat)
    lon = _slon2plon(lon)

    lon = np.atleast_1d(lon)
    lat = np.atleast_1d(lat)

    ## load dataset
    dat_dichotomy_coords = get_dichotomy_coords()

    ## for each input longitude, find nearest dichotomy coordinates
    i_lons = np.searchsorted(dat_dichotomy_coords[:,0], lon, side='right') - 1
    llons, llats = dat_dichotomy_coords[i_lons].T
    rlons, rlats = dat_dichotomy_coords[i_lons+1].T

    ## linear interpolate between two nearest dichotomy coordinates to find threshold latitude
    tlats = llats + (rlats - llats) * ( (lon - llons) / (rlons - llons) )

    ## compare shape(y,1) with shape(x), which broadcasts to shape(y,x) with element-wise comparison
    result = lat[:, None] >= tlats

    ## convert singleton arrays to scalars (i.e. both inputs were scalars)
    if result.size == 1:
        return result.item()

    elif as_xarray:
        result = xr.DataArray(
            result,
            dims   = ("lat", "lon"),
            coords = {"lat": lat, "lon": lon},
        )
        # result = result.sortby('lat').sortby('lon')
    return result



def get_dichotomy_coords() -> np.ndarray:
    fpath = _get_fpath_dataset('dichotomy_coords')
    dat_dichotomy_coords = np.loadtxt(fpath)
    return dat_dichotomy_coords
