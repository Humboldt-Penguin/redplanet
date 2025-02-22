import numpy as np
import xarray as xr

from redplanet.Mag.sh.loader import get_dataset

from redplanet.helper_functions.docstrings.main import substitute_docstrings



@substitute_docstrings
def get(
    lon       : float | np.ndarray,
    lat       : float | np.ndarray,
    quantity  : str  = 'total',
    as_xarray : bool = False
) -> float | np.ndarray | xr.DataArray:
    """
    Get magnetic field values at the specified coordinates. Dataset must be loaded first, see `redplanet.Mag.sh.load(...)`.

    Parameters
    ----------
    {param.lon}
    {param.lat}
    quantity : str, optional
        Options are: ['radial', 'theta', 'phi', 'total', 'potential'], by default 'total'.
    {param.as_xarray}

    Returns
    -------
    {return.GriddedData}

        Units are nanotesla [nT].

    Raises
    ------
    ValueError
        If `quantity` is not one of ['radial', 'theta', 'phi', 'total', 'potential.
    """

    q = ['radial', 'theta', 'phi', 'total', 'potential']
    if quantity not in q:
        raise ValueError(f"Quantity {quantity} is not in list of supported quantities: {q}.")

    dat_mag = get_dataset()

    return dat_mag.get_values(
        lon = lon,
        lat = lat,
        var = quantity,
        as_xarray = as_xarray,
    )
