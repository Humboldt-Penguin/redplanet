import numpy as np
import xarray as xr

from redplanet.Crust.moho.loader import get_dataset

from redplanet.helper_functions.docstrings.main import substitute_docstrings



@substitute_docstrings
def get(
    lon       : float | np.ndarray,
    lat       : float | np.ndarray,
    crthick   : bool = False,
    as_xarray : bool = False
) -> float | np.ndarray | xr.DataArray:
    """
    Get Mohorovičić discontinuity depth (or derived crustal thickness) values at the specified coordinates. Dataset must be loaded first, see `redplanet.Crust.moho.load(...)`.

    Parameters
    ----------
    {param.lon}
    {param.lat}
    crthick : bool, optional
        If True, return crustal thickness values, which is just the difference between the moho and a spherical harmonic model of topography evaluated to the same degree (same method as {@Wieczorek2022_icta.n}). Default is False.
    {param.as_xarray}

    Returns
    -------
    {return.GriddedData}

        Units are meters [m].
    """

    dat_moho = get_dataset()

    return dat_moho.get_values(
        lon = lon,
        lat = lat,
        var = 'crthick' if crthick else 'moho',
        as_xarray = as_xarray,
    )
