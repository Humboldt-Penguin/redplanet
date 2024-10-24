import numpy as np
import xarray as xr

from redplanet.helper_functions import _verify_coords, _plon2slon
from redplanet.GRS.load import _get_dataset



def get(
    element  : str,
    lon      : float,
    lat      : float,
    quantity : str  = 'concentration',
    normalize: bool = False,
    as_xarray: bool = False,
) -> float | np.ndarray | xr.Dataset:

    dat_grs = _get_dataset()

    ## input validation
    if element not in ['al','ca','cl','fe','h2o','k','si','s','th']:
        raise ValueError(f"Element {element} is not in list of supported elements: ['al','ca','cl','fe','h2o','k','si','s','th'].")

    lon = np.array(lon)
    lat = np.array(lat)
    _verify_coords(lon, lat)
    lon = _plon2slon(lon)


    ## get data
    data = (
        dat_grs
            .sel(element=element)
            .sel(lon=lon, lat=lat, method='nearest')
            [quantity]
    )

    if normalize:
        if element in ['cl','h2o','s']:
            raise ValueError(f"Can't normalize a volatile element ('{element}') to a volatile-free (cl, h2o, s) basis.")
        volatiles = (
            dat_grs
                .sel(element=['cl','h2o','s'])
                .sel(lon=lon, lat=lat, method='nearest')
                [quantity]
                .sum(dim='element')
        )
        data = data / (1 - volatiles)

    if not as_xarray:
        data = data.values
        ## convert singleton numpy array to scalar
        if data.shape == (): data = data.item()

    return data
