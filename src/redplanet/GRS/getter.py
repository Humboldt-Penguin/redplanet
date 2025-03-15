import numpy as np
import xarray as xr

from redplanet.GRS.loader import get_dataset

from redplanet.helper_functions.docstrings.main import substitute_docstrings



@substitute_docstrings
def get(
    element   : str,
    lon       : float | np.ndarray,
    lat       : float | np.ndarray,
    quantity  : str  = 'concentration',
    normalize : bool = False,
    as_xarray : bool = False
) -> float | np.ndarray | xr.DataArray:
    """
    Get GRS element concentration/sigma values at the specified coordinates.

    Data (0.41 MiB) is provided by {@GRS_data.n}. The full paper discusses/analyzes the models in detail ({@GRS_paper.p}).


    Parameters
    ----------
    element : str
        Element name. Options are: ['al', 'ca', 'cl', 'fe', 'h2o', 'k', 'si', 's', 'th'].
    {param.lon}
    {param.lat}
    quantity : str, optional
        Return 'concentration' or 'sigma' values, by default 'concentration'.
    normalize : bool, optional
        If True, normalize the element quantity to a volatile-free (Cl, H2O, S) basis, by default False.

        > "The GRS instrument measures elemental abundances in the top-most tens of centimeters of the Martian surface, and thus is strongly influenced by near-surface soils, ice and dust deposits. These sediments broadly represent the bulk chemistry of the Martian upper crust when renormalized to a volatile-free basis [Taylor and McLennan, 2009] and as such, K and Th values must be renormalized to a H2O-, S-, and Cl-free basis to better reflect bulk crustal values." ({@Hahn2011.p})
    {param.as_xarray}


    Returns
    -------
    {return.GriddedData}

        Units are mass fraction (out of one).


    Raises
    ------
    ValueError
        - `element` is not one of ['al', 'ca', 'cl', 'fe', 'h2o', 'k', 'si', 's', 'th'].
        - `quantity` is not one of ['concentration', 'sigma'].
        - `normalize` is True and `element` is one of ['cl', 'h2o', 's'] -- you can't normalize a volatile element to a volatile-free basis!
    """

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
        as_xarray = as_xarray,
    )

    if normalize:
        volatiles = dat_grs.get_values(
            lon = lon,
            lat = lat,
            var = f'cl+h2o+s_{quantity}',
            as_xarray = as_xarray,
        )
        dat = dat / (1 - volatiles)

    return dat
