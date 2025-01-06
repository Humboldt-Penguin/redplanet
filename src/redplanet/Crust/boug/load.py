import copy

import numpy as np

from redplanet.DatasetManager.master import _get_fpath_dataset





_dat_boug   : np.memmap  | None = None
_model_info : dict       | None = None

def get_dataset() -> list[ np.memmap, dict ]:
    if _dat_boug is None:
        raise ValueError('Bouguer dataset not loaded. Use `redplanet.Crust.boug.load(<model_params>)`.')
    return [_dat_boug, _model_info]





def load(model: str = None) -> None:

    ## DEV NOTE: this is a bit over-complicated right now, but it will be useful when we have multiple models like DEM

    metadata = {
        'Genova2016': {
            'description' : 'Bouguer gravity anomaly map computed from truncated GMM-3 solution (degree 2 to 90). See: https://pds-geosciences.wustl.edu/mro/mro-m-rss-5-sdp-v1/mrors_1xxx/data/rsdmap/',
            'shape'       : (2880, 5760),
            'dtype'       : np.float64,
            ## from lbl file, see that resolution is 16 pixels per degree, so...
            'lons'        : np.linspace(  0, 360, 5760, endpoint=False) + 1 / (2 * 16),
            'lats'        : np.linspace(-90,  90, 2880, endpoint=False) + 1 / (2 * 16),
            'post-process': np.flipud,
        },
    }

    if model not in metadata:
        raise ValueError(f"Invalid model: '{model}'. Valid models are: {list(metadata.keys())}.")

    fpath = _get_fpath_dataset(model)

    global _dat_boug
    _dat_boug = np.memmap(
        fpath,
        mode  = 'r',
        dtype = metadata[model]['dtype'],
        shape = metadata[model]['shape'],
    )
    # _dat_boug = np.flipud(_dat_boug)  ## make lats increasing
    _dat_boug = metadata[model]['post-process'](_dat_boug)  ## make lats increasing

    global _model_info
    _model_info = copy.deepcopy(metadata[model])

    return
