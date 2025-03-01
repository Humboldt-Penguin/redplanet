import numpy as np

from redplanet.DatasetManager.main import _get_fpath_dataset
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





@substitute_docstrings
def load(model: str = None) -> None:
    """
    Load a topography model.

    Parameters
    ----------
    model : str
        Name of the topography model to load. Options are:

        - `'DEM_463m'` (2GB) — Mars MGS MOLA DEM 463m ({@DEM_463m.p}).
        - `'DEM_200m'` (11GB) — Mars MGS MOLA - MEX HRSC Blended DEM 200m ({@DEM_200m.p}).

        For description of our modifications to the original data, see notes section.

    Raises
    ------
    ValueError
        If an invalid model name is provided.

    Notes
    -----
    We modify the original data files by reprojecting to the "Mars 2000 Sphere" model (radius = 3,396,190 km) and converting from the "TIFF" file format to a simple binary file containing the raw bytes of the array data for faster & less memory-intensive loading. For more information and our code, see <https://github.com/Humboldt-Penguin/redplanet/tree/main/datasets/Crust/topo/DEM>{target="_blank"} -- TODO: I'll eventually have a section on my website to describe datasets and how we modified them, add a link to that here.
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
