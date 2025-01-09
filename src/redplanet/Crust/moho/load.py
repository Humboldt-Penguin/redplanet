import copy

import pandas as pd
import xarray as xr
import pyshtools as pysh

from redplanet.DatasetManager.master import _get_fpath_dataset
from redplanet.DatasetManager.dataset_info import MohoDatasetNotFoundError





def get_registry() -> pd.DataFrame:
    registry = pd.read_csv(
        _get_fpath_dataset('moho_registry'),
        usecols = ['model_name'],
    )
    registry = registry['model_name'].str.split('-', expand=True)
    registry.columns = ['interior_model', 'insight_thickness', 'rho_south', 'rho_north']
    registry.iloc[:,1:] = registry.iloc[:,1:].astype(int)
    return registry





_dat_moho  : xr.DataArray         | None = None
_model_info: dict[ str, str|int ] | None = None

def get_dataset() -> list[ xr.DataArray, dict[str, str|int] ]:
    if _dat_moho is None:
        raise ValueError('Moho dataset not loaded. Use `redplanet.Crust.moho.load(<model_params>)`.')
    return [_dat_moho, copy.deepcopy(_model_info)]





def load(
    interior_model    : str,
    insight_thickness : int,
    rho_south         : int,
    rho_north         : int,
    fail_silently     : bool = False,    ##  False [default] -> return None,    True -> return type(bool)
) -> None | bool:

    if interior_model not in _interior_models:
        raise ValueError(f'Unknown interior model: \"{interior_model}\".\nOptions are: \"{"\", \"".join(_interior_models)}\".')    # (lol)

    try:
        fpath_moho = _get_fpath_dataset(f'Moho-Mars-{interior_model}-{insight_thickness}-{rho_south}-{rho_north}')
    except MohoDatasetNotFoundError:
        if fail_silently: return False
        else: raise

    global _model_info
    _model_info = {
        'interior_model'   : interior_model,
        'insight_thickness': int(insight_thickness),
        'rho_south'        : int(rho_south),
        'rho_north'        : int(rho_north),
    }

    global _dat_moho
    _dat_moho = (
        pysh.SHCoeffs.from_file(fpath_moho)
        .expand()
        .to_xarray()
        .sortby('lat')
    )

    if fail_silently:
        return True
    return





_interior_models: list[str] = (
    'DWAK',
    'DWThot',
    'DWThotCrust1',
    'DWThotCrust1r',
    'EH45Tcold',
    'EH45TcoldCrust1',
    'EH45TcoldCrust1r',
    'EH45ThotCrust2',
    'EH45ThotCrust2r',
    'Khan2022',
    'LFAK',
    'SANAK',
    'TAYAK',
    'YOTHotRc1760kmDc40km',
    'YOTHotRc1810kmDc40km',
    'ZG_DW',
)





_dat_shape: xr.DataArray | None = None

def _get_shape() -> xr.DataArray:
    global _dat_shape
    if _dat_shape is None:

        fpath_shape = _get_fpath_dataset('MOLA_shape_719')

        _dat_shape = (
            pysh.SHCoeffs.from_file(
                fpath_shape,
                lmax   = 90,
                format = 'bshc'
            )
            .expand()
            .to_xarray()
            .sortby('lat')
        )

    return _dat_shape
