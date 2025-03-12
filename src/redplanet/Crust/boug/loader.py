import numpy as np

from redplanet.DatasetManager.main import _get_fpath_dataset
from redplanet.helper_functions.GriddedData import GriddedData

from redplanet.helper_functions.docstrings.main import substitute_docstrings





_dat_boug: GriddedData | None = None

@substitute_docstrings
def get_dataset() -> GriddedData:
    """
    {fulldoc.get_dataset_GriddedData}
    """
    if _dat_boug is None:
        raise ValueError('Bouguer dataset not loaded. Use `redplanet.Crust.boug.load(<model_params>)`.')
    return _dat_boug

@substitute_docstrings
def get_metadata() -> dict:
    """
    {fulldoc.get_metadata}
    """
    return dict(get_dataset().metadata)





@substitute_docstrings
def load(model: str = None) -> None:
    """
    Load Bouguer gravity anomaly dataset.

    Parameters
    ----------
    model : str
        Name of the Bouguer model to load. Options are:

        - `'Genova2016'` (127 MiB) — Bouguer gravity anomaly map from {@Genova2016_boug_data.n}, computed from truncated GMM-3 solution (degree 2 to 90) ({@Genova2016_boug_paper.p}).

    Raises
    ------
    ValueError
        If an invalid model name is provided.
    """

    ## I expect to add more later, so users should explicitly choose Genova2016 for forward compatibility.
    info = {
        'Genova2016': {
            'shape'          : (2880, 5760),
            'dtype'          : np.float64,
            'post-processing': lambda arr: np.flipud(arr),
            'lon'            : np.linspace(  0, 360, 5760, endpoint=False) + 1 / (2 * 16),
            'lat'            : np.linspace(-90,  90, 2880, endpoint=False) + 1 / (2 * 16),
            'metadata': {
                'description': 'Bouguer gravity anomaly map computed from truncated GMM-3 solution (degree 2 to 90).',
                'units'      : 'mGal',
                'links'      : {
                    'download': 'https://pds-geosciences.wustl.edu/mro/mro-m-rss-5-sdp-v1/mrors_1xxx/data/rsdmap/',
                    'lbl'     : 'https://pds-geosciences.wustl.edu/mro/mro-m-rss-5-sdp-v1/mrors_1xxx/data/rsdmap/ggmro_120_bouguer_90.lbl',
                },
            },
        },
    }

    if model not in info:
        raise ValueError(f"Invalid Bouguer model: '{model}'. Options are: {list(info.keys())}.")



    if model == 'Genova2016':

        fpath = _get_fpath_dataset(model)

        dat = np.memmap(
            fpath,
            mode  = 'r',
            dtype = info[model]['dtype'],
            shape = info[model]['shape'],
        )
        dat = info[model]['post-processing'] (dat)

        metadata = info[model]['metadata']
        metadata['fpath'] = fpath

        global _dat_boug
        _dat_boug = GriddedData(
            lon       = info[model]['lon'],
            lat       = info[model]['lat'],
            is_slon   = False,
            data_dict = {'boug': dat},
            metadata  = metadata,
        )



    else:
        raise ValueError(f"THE DEVELOPER MESSED UP. THIS SHOULD NOT HAPPEN.")

    return
