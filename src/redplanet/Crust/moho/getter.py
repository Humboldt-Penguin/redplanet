import numpy as np
import xarray as xr

from redplanet.Crust.moho.loader import get_dataset



def get(
    lon                 : float | np.ndarray,
    lat                 : float | np.ndarray,
    crthick             : bool = False,
    as_xarray           : bool = False
) -> float | np.ndarray | xr.DataArray:

    if crthick:
        var = 'crthick'
    else:
        var = 'moho'

    dat_moho = get_dataset()

    return dat_moho.get_values(
        lon = lon,
        lat = lat,
        var = var,
        as_xarray = as_xarray,
    )
