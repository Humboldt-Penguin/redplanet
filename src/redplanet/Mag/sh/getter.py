import numpy as np
import xarray as xr

from redplanet.Mag.sh.loader import get_dataset



def get(
    lon                 : float | np.ndarray,
    lat                 : float | np.ndarray,
    quantity            : str  = 'total',
    return_exact_coords : bool = False,
    as_xarray           : bool = False
) -> float | np.ndarray | dict[str, np.ndarray] | xr.Dataset:
    """
    Quantity options are: ['radial', 'theta', 'phi', 'total', 'potential'].
    """

    dat_mag = get_dataset()

    return dat_mag.get_values(
        lon = lon,
        lat = lat,
        var = quantity,
        return_exact_coords = return_exact_coords,
        as_xarray = as_xarray,
    )
