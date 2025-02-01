import numpy as np
import xarray as xr

from redplanet.GRS.loader import get_dataset



def get(
    element             : str,
    lon                 : float | np.ndarray,
    lat                 : float | np.ndarray,
    quantity            : str  = 'concentration',
    normalize           : bool = False,
    # return_exact_coords : bool = False,  ## TODO: need to account for this when normalizing -- when implemented, comment out lines in `test_GRS.py`
    as_xarray           : bool = False
) -> float | np.ndarray | dict[str, np.ndarray] | xr.Dataset:

    ## input validation
    e = ['al','ca','cl','fe','h2o','k','si','s','th']
    v = ['cl','h2o','s']
    q = ['concentration','sigma']

    if element not in e:
        raise ValueError(f"Element {element} is not in list of supported elements: {e}.")

    if quantity not in q:
        raise ValueError(f"Quantity {quantity} is not in list of supported quantities: {q}.")

    if normalize and (element in v):
        raise ValueError(f"Can't normalize a volatile element ('{element}') to a volatile-free (cl, h2o, s) basis.")


    ## get data & normalize
    dat_grs = get_dataset()

    dat = dat_grs.get_values(
        lon = lon,
        lat = lat,
        var = f'{element}_{quantity}',
        return_exact_coords = False,
        as_xarray = as_xarray,
    )

    if normalize:
        volatiles = dat_grs.get_values(
            lon = lon,
            lat = lat,
            var = f'cl+h2o+s_{quantity}',
            return_exact_coords = False,
            as_xarray = as_xarray,
        )
        dat = dat / (1 - volatiles)

    return dat
