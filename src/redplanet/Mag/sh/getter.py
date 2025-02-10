import numpy as np
import xarray as xr

from redplanet.Mag.sh.loader import get_dataset



def get(
    lon                 : float | np.ndarray,
    lat                 : float | np.ndarray,
    quantity            : str  = 'total',
    as_xarray           : bool = False
) -> float | np.ndarray | xr.DataArray:
    """
    Quantity options are: ['radial', 'theta', 'phi', 'total', 'potential'].
    """

    dat_mag = get_dataset()

    return dat_mag.get_values(
        lon = lon,
        lat = lat,
        var = quantity,
        as_xarray = as_xarray,
    )
