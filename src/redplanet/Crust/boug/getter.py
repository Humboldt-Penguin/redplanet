import numpy as np
import xarray as xr

from redplanet.Crust.boug.loader import get_dataset



def get(
    lon                 : float | np.ndarray,
    lat                 : float | np.ndarray,
    return_exact_coords : bool = False,
    as_xarray           : bool = False
) -> float | np.ndarray | dict[str, np.ndarray] | xr.Dataset:

    dat_boug = get_dataset()

    return dat_boug.get_values(
        lon = lon,
        lat = lat,
        var = 'boug',
        return_exact_coords = return_exact_coords,
        as_xarray = as_xarray,
    )
