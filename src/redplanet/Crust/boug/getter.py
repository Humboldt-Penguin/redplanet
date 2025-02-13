import numpy as np
import xarray as xr

from redplanet.Crust.boug.loader import get_dataset

from redplanet.helper_functions.docstrings import substitute_docstrings



@substitute_docstrings
def get(
    lon                 : float | np.ndarray,
    lat                 : float | np.ndarray,
    as_xarray           : bool = False
) -> float | np.ndarray | xr.DataArray:
    """
    Get Bouguer anomaly values at the specified coordinates. Dataset must be loaded first, see `redplanet.Crust.boug.load(...)`.

    Parameters
    ----------
    {param_lon}
    {param_lat}
    {param_as_xarray}

    Returns
    -------
    {return_GriddedData}

        Units are milligals [mGal].
    """

    dat_boug = get_dataset()

    return dat_boug.get_values(
        lon = lon,
        lat = lat,
        var = 'boug',
        as_xarray = as_xarray,
    )
