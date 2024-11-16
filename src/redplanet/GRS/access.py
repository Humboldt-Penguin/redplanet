import numpy as np
import xarray as xr

from redplanet.helper_functions import _verify_coords, _plon2slon
from redplanet.GRS.load import _get_dataset



def get(
    element : str,
    lon     : float | np.ndarray,  ## TODO: test array inputs!!!
    lat     : float | np.ndarray,
    quantity           : str  = 'concentration',
    normalize          : bool = False,
    as_xarray          : bool = False,
    return_exact_coords: bool = False,
) -> float | np.ndarray | list[np.ndarray, np.ndarray, np.ndarray] | xr.Dataset:


    ## input validation
    if as_xarray and return_exact_coords:
        raise ValueError("Can't return both xarray and exact coordinates. Choose one.")

    if element not in ['al','ca','cl','fe','h2o','k','si','s','th']:
        raise ValueError(f"Element {element} is not in list of supported elements: ['al','ca','cl','fe','h2o','k','si','s','th'].")

    if normalize and (element in ['cl','h2o','s']):
        raise ValueError(f"Can't normalize a volatile element ('{element}') to a volatile-free (cl, h2o, s) basis.")

    _verify_coords(lon, lat)
    lon = _plon2slon(lon)
    lon = np.atleast_1d(lon)
    lat = np.atleast_1d(lat)


    ## get data
    dat_grs = _get_dataset()
    data = (
        dat_grs
            .sel(element=element)
            .sel(lon=lon, lat=lat, method='nearest')
            [quantity]
    )

    if normalize:
        volatiles = (
            dat_grs
                .sel(element=['cl','h2o','s'])
                .sel(lon=lon, lat=lat, method='nearest')
                [quantity]
                .sum(dim='element')
        )
        data = data / (1 - volatiles)


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
