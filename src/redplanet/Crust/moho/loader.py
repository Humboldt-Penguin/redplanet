import numpy as np
import pyshtools as pysh

from redplanet.DatasetManager.master import _get_fpath_dataset
from redplanet.helper_functions.GriddedData import GriddedData

from redplanet.DatasetManager.dataset_info import MohoDatasetNotFoundError

from redplanet.Crust.moho.consts import _interior_models





_dat_moho: GriddedData | None = None

def get_dataset() -> GriddedData:
    if _dat_moho is None:
        raise ValueError('Bouguer dataset not loaded. Use `redplanet.Crust.moho.load(<model_params>)`.')
    return _dat_moho





def load(
    interior_model    : str,
    insight_thickness : int | str,
    rho_south         : int | str,
    rho_north         : int | str,
    fail_silently     : bool = False,    ##  False [default] -> return None,  True -> return type(bool)
) -> None | bool:

    ## load moho

    if interior_model not in _interior_models:
        raise ValueError(
            f'Unknown interior model: \"{interior_model}\".\n'
            f'Options are: \"{"\", \"".join(_interior_models)}\".'
        )

    try:
        fpath_moho = _get_fpath_dataset(
            f'Moho-Mars-{interior_model}-{insight_thickness}-{rho_south}-{rho_north}'
        )
    except MohoDatasetNotFoundError as e:
        if fail_silently:
            return False
        else:
            raise

    ds_moho = (
        pysh.SHCoeffs.from_file(fpath_moho)
        .expand()
        .to_xarray()
        .isel(lat=slice(None, None, -1))  ## in pysh, lats are always decreasing at first
    )



    ## load shape

    fpath_shape = _get_fpath_dataset('MOLA_shape_719')

    ds_shape = (
        pysh.SHCoeffs.from_file(
            fpath_shape,
            lmax   = 90,
            format = 'bshc'
        )
        .expand()
        .to_xarray()
        .isel(lat=slice(None, None, -1))
    )



    ## GriddedData

    global _dat_moho

    _dat_moho = GriddedData(
        lon       = ds_moho.lon.values,
        lat       = ds_moho.lat.values,
        is_slon   = False,
        data_dict = {
            'moho'   : ds_moho.values,
            'crthick': (ds_shape - ds_moho).values,
        },
        metadata  = {
            'title': f'{interior_model}-{insight_thickness}-{rho_south}-{rho_north}',
            'units': 'm',
            'model_params': {
                'interior_model'      : interior_model,
                'insight_thickness_km': insight_thickness,
                'rho_south'           : rho_south,
                'rho_north'           : rho_north,
            },
            'lmax': 90,
            'source' : 'https://doi.org/10.5281/zenodo.6477509',
            'fpath': fpath_moho,
        },
    )



    if fail_silently:
        return True
    return
