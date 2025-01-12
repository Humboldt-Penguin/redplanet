import numpy as np
import xarray as xr

from redplanet.Crust.moho.loader import get_dataset



def get(
    lon                 : float | np.ndarray,
    lat                 : float | np.ndarray,
    crthick             : bool = False,
    return_exact_coords : bool = False,
    as_xarray           : bool = False
) -> float | np.ndarray | dict[str, np.ndarray] | xr.Dataset:

    if crthick:
        var = 'crthick'
    else:
        var = 'moho'

    dat_moho = get_dataset()

    return dat_moho.get_values(
        lon = lon,
        lat = lat,
        var = var,
        return_exact_coords = return_exact_coords,
        as_xarray = as_xarray,
    )
