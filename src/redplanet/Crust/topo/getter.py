import numpy as np
import xarray as xr

from redplanet.Crust.topo.loader import get_dataset

from redplanet.helper_functions.docstrings.main import substitute_docstrings



@substitute_docstrings
def get(
    lon       : float | np.ndarray,
    lat       : float | np.ndarray,
    as_xarray : bool = False
) -> float | np.ndarray | xr.DataArray:
    """
    Get topography values at the specified coordinates. Dataset must be loaded first, see `redplanet.Crust.topo.load(...)`.

    Parameters
    ----------
    {param.lon}
    {param.lat}
    {param.as_xarray}

    Returns
    -------
    {return.GriddedData}

        Units are meters [m].
    """

    dat_topo = get_dataset()

    return dat_topo.get_values(
        lon = lon,
        lat = lat,
        var = 'topo',
        as_xarray = as_xarray,
    )
