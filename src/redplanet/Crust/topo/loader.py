import numpy as np

from redplanet.DatasetManager.master import _get_fpath_dataset
from redplanet.helper_functions.GriddedData import GriddedData

from redplanet.helper_functions.docstrings.main import substitute_docstrings





_dat_topo: GriddedData | None = None

@substitute_docstrings
def get_dataset() -> GriddedData:
    """
    {fulldoc.get_dataset_GriddedData}
    """
    if _dat_topo is None:
        raise ValueError('Topography dataset not loaded. Use `redplanet.Crust.topo.load(<model_params>)`.')
    return _dat_topo

@substitute_docstrings
def get_metadata() -> dict:
    """
    {fulldoc.get_metadata}
    """
    return dict(get_dataset().metadata)





def load(model: str = None) -> None:
    """
    Load a topography model.

    Parameters
    ----------
    model : str
        Name of the topography model to load. Options are: ['DEM_463m', 'DEM_200m'].

    Raises
    ------
    ValueError
        If an invalid model name is provided.
    """

    info = {
        'DEM_463m': {
            'shape'    : (23041, 46081),
            'dtype'    : np.int16,
            'nan_value': -99_999,  ## data is stored as int16 which doesn't support `np.nan`, so we use this sentinel value.
            'lon'      : -179.9960938347692 + 0.007812330461578525 * np.arange(46081),
            'lat'      : -89.99376946560506 + 0.00781206004494716  * np.arange(23041),
            'metadata': {
                'title': 'Mars MGS MOLA DEM 463m',
                'units': 'm',
                'link' : 'https://astrogeology.usgs.gov/search/map/mars_mgs_mola_dem_463m',
            },
        },
        'DEM_200m': {
            'shape'    : (53347, 106694),
            'dtype'    : np.int16,
            'nan_value': -99_999,  ## data is stored as int16 which doesn't support `np.nan`, so we use this sentinel value.
            'lon'      : -179.9983129395848 + 0.0033741208306410017 * np.arange(106694),
            'lat'      : -89.99753689179012 + 0.0033741208306410004 * np.arange(53347),
            'metadata': {
                'title': 'Mars MGS MOLA - MEX HRSC Blended DEM Global 200m',
                'units': 'm',
                'link' : 'https://astrogeology.usgs.gov/search/map/mars_mgs_mola_mex_hrsc_blended_dem_global_200m',
            },
        },
    }

    if model not in info:
        raise ValueError(f"Invalid topography model: '{model}'. Options are: {list(info.keys())}.")



    if model.startswith('DEM_'):

        fpath = _get_fpath_dataset(model)

        dat = np.memmap(
            fpath,
            mode  = 'r',
            dtype = info[model]['dtype'],
            shape = info[model]['shape'],
        )

        metadata = info[model]['metadata']
        metadata['fpath'] = fpath

        global _dat_topo
        _dat_topo = GriddedData(
            lon       = info[model]['lon'],
            lat       = info[model]['lat'],
            is_slon   = True,
            data_dict = {'topo': dat},
            metadata  = metadata,
        )



    else:
        raise ValueError(f"THE DEVELOPER MESSED UP. THIS SHOULD NOT HAPPEN.")

    return
