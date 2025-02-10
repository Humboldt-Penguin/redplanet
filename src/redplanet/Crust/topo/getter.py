import numpy as np
import xarray as xr

from redplanet.Crust.topo.loader import get_dataset



def get(
    lon                 : float | np.ndarray,
    lat                 : float | np.ndarray,
    as_xarray           : bool = False
) -> float | np.ndarray | xr.DataArray:

    dat_topo = get_dataset()

    return dat_topo.get_values(
        lon = lon,
        lat = lat,
        var = 'topo',
        as_xarray = as_xarray,
    )
