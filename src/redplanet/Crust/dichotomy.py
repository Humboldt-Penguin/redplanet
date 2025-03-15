import numpy as np
import xarray as xr

from redplanet.DatasetManager.main import _get_fpath_dataset
from redplanet.helper_functions.coordinates import (
    _verify_coords,
    _slon2plon,
)
from redplanet.helper_functions.docstrings.main import substitute_docstrings



@substitute_docstrings
def is_above(
    lon       : float | np.ndarray,
    lat       : float | np.ndarray,
    as_xarray : bool = False,
) -> bool | np.ndarray | xr.DataArray:
    """
    Determine if the given point(s) are above the dichotomy boundary.

    See `help(redplanet.Crust.dichotomy.get_coords)` for the source of the dichotomy boundary coordinates data.

    Parameters
    ----------
    {param.lon}
    {param.lat}
    {param.as_xarray}

    Returns
    -------
    bool | np.ndarray | xr.DataArray
        Boolean array indicating whether the input coordinates are above the dichotomy boundary. If both inputs are 1D numpy arrays then it returns a 2D numpy array with shape `(len(lat), len(lon))`.
    """

    ## input validation
    _verify_coords(lon, lat)
    lon = _slon2plon(lon)

    lon = np.atleast_1d(lon)
    lat = np.atleast_1d(lat)

    ## load dataset
    dat_dichotomy_coords = get_coords()

    ## for each input longitude, find nearest dichotomy coordinates
    i_lons = np.searchsorted(dat_dichotomy_coords[:,0], lon, side='right') - 1
    llons, llats = dat_dichotomy_coords[i_lons].T
    rlons, rlats = dat_dichotomy_coords[i_lons+1].T

    ## linear interpolate between two nearest dichotomy coordinates to find threshold latitude
    tlats = llats + (rlats - llats) * ( (lon - llons) / (rlons - llons) )

    ## compare shape(y,1) with shape(x), which broadcasts to shape(y,x) with element-wise comparison
    result = lat[:, None] >= tlats

    ## remove singleton arrays/dimensions (i.e. one or both inputs were scalars)
    result = np.squeeze(result)
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



@substitute_docstrings
def get_coords() -> np.ndarray:
    """
    Get a list of dichotomy boundary coordinates.

    The origin of the dataset is not fully clear. We use the file "dichotomy_coordinates-JAH-0-360.txt" (0.046 MiB) downloaded from {@Wieczorek2022_icta.n}. They attribute the data to *"Andrews-Hanna et al. (2008)"* which is ambiguous (to me atleast, I could be missing something obvious) — my best guess is {@dichotomy_paper.n}.

    Returns
    -------
    np.ndarray
        A numpy array of shape `(n, 2)` where `n` is the number of coordinates, and the two columns are longitude (0->360) and latitude respectively.
    """
    fpath = _get_fpath_dataset('dichotomy_coords')
    dat_dichotomy_coords = np.loadtxt(fpath)
    return dat_dichotomy_coords
