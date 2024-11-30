import copy

import numpy as np

from redplanet.DatasetManager.master import _get_fpath_dataset





_dat_dem:    np.memmap  | None = None
_model_info: dict       | None = None

def get_dataset() -> list[ np.memmap, dict ]:
    if _dat_dem is None:
        raise ValueError('Topo dataset not loaded. Use `redplanet.Crust.topo.load(<model_params>)`.')
    return [_dat_dem, _model_info]





def load(model: str = None) -> None:
    """
    Load the DEM dataset into memory.

    TODO
    """

    dem_metadata = {
        'DEM_463m': {
            'model_name' : 'Mars MGS MOLA DEM 463m',
            'resolution' : 463,
            'shape'      : (23041, 46081),
            'dtype'      : np.int16,
            'nan_value'  : -99_999,    ## data is stored as int16 which doesn't support `np.nan`, so we use this sentinel value.
            'lons_approx': -179.9960938347692 + 0.007812330461578525 * np.arange(46081),
            'lats_approx': -89.99376946560506 + 0.00781206004494716  * np.arange(23041),
        },
        'DEM_200m': {
            'model_name' : 'Mars MGS MOLA - MEX HRSC Blended DEM Global 200m',
            'resolution' : 200,
            'shape'      : (53347, 106694),
            'dtype'      : np.int16,
            'nan_value'  : -99_999,    ## data is stored as int16 which doesn't support `np.nan`, so we use this sentinel value.
            'lons_approx': -179.9983129395848 + 0.0033741208306410017 * np.arange(106694),
            'lats_approx': -89.99753689179012 + 0.0033741208306410004 * np.arange(53347),
        },
    }

    if model not in dem_metadata:
        raise ValueError(f"Invalid model: '{model}'. Valid models are: {list(dem_metadata.keys())}.")

    fpath_dataset = _get_fpath_dataset(model)

    global _dat_dem
    _dat_dem = np.memmap(
        fpath_dataset,
        mode  = 'r',
        dtype = dem_metadata[model]['dtype'],
        shape = dem_metadata[model]['shape'],
    )

    global _model_info
    _model_info = copy.deepcopy( dem_metadata[model] )

    return
