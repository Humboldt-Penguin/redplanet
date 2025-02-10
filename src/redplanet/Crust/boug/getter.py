import numpy as np
import xarray as xr

from redplanet.Crust.boug.loader import get_dataset



def get(
    lon                 : float | np.ndarray,
    lat                 : float | np.ndarray,
    as_xarray           : bool = False
) -> float | np.ndarray | xr.DataArray:

    dat_boug = get_dataset()

    return dat_boug.get_values(
        lon = lon,
        lat = lat,
        var = 'boug',
        as_xarray = as_xarray,
    )
