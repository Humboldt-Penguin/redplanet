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

        - `'SH_10km'` (17 MB) — Spherical harmonic model of topography from {@MOLA_shcoeffs.n} evaluated to degree 1066, corresponding to a spatial resolution of 10 km.
        - `'SH_5km'` (70 MB) — Same as `'SH_10km'` but evaluated to degree 2133, corresponding to a spatial resolution of 5 km.
        - `'DEM_463m'` (2 GB) — MGS MOLA Digital Elevation Model 463m ({@DEM_463m.p}).
        - `'DEM_200m'` (11 GB) — MGS MOLA - MEX HRSC Blended Digital Elevation Model 200m ({@DEM_200m.p}).

        For description of our modifications to the original data, see notes section.

    Raises
    ------
    ValueError
        If an invalid model name is provided.

    Notes
    -----
    For 'SH_' options, we start with a spherical harmonic model of the shape of Mars based on MOLA data, provided by {@MOLA_shcoeffs.n}. Then we subtract the geoid height and geoid reference radius, which yields the planet's surface relief with respect to the geoid (i.e. topography). We assume a spherical harmonic model of degree $L$ has spatial resolution $\\frac{2 \\pi R_{\\text{Mars}}}{2L+1}$. Results are saved as a binary file, which can be loaded as a memory-mapped 2D numpy array of 16-bit integers for very fast access speeds without occupying RAM. For more information and our code, see ["datasets/Crust/topo/SH" in the GitHub repo.](https://github.com/Humboldt-Penguin/redplanet/tree/main/datasets/Crust/topo/SH){target="_blank"} -- TODO*

    For 'DEM_' options, we modify the original data files by reprojecting to the "Mars 2000 Sphere" model (radius = 3,396,190 km). We convert the original "TIFF" file format to a binary file, which can be loaded as a memory-mapped 2D numpy array of 16-bit integers for very fast access speeds without occupying RAM. For more information and our code, see ["datasets/Crust/topo/DEM" in the GitHub repo.](https://github.com/Humboldt-Penguin/redplanet/tree/main/datasets/Crust/topo/DEM){target="_blank"} -- TODO*

    * I'll eventually have a section on my website to describe datasets and how we modified them -- add a link to that here.
    """

    info = {
        'SH_10km': {
            'shape'    : (2135, 4269),
            'dtype'    : np.int16,
            'lon'      : np.linspace(0, 360, 4269),
            'lat'      : np.linspace(-90, 90, 2135),
            'metadata': {
                'title'   : 'Spherical harmonic models of the shape of Mars (MOLA) — 10 km resolution, corresponding to degree 1066',
                'units'   : 'm',
                'citation': 'Wieczorek, M. (2024). Spherical harmonic models of the shape of Mars (MOLA) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.10820719',
            },
        },
        'SH_5km': {
            'shape'    : (4269, 8537),
            'dtype'    : np.int16,
            'lon'      : np.linspace(0, 360, 8537),
            'lat'      : np.linspace(-90, 90, 4269),
            'metadata': {
                'title'   : 'Spherical harmonic models of the shape of Mars (MOLA) — 5 km resolution, corresponding to degree 2133',
                'units'   : 'm',
                'citation': 'Wieczorek, M. (2024). Spherical harmonic models of the shape of Mars (MOLA) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.10820719',
            },
        },
        'DEM_463m': {
            'shape'    : (23041, 46081),
            'dtype'    : np.int16,
            'nan_value': -99_999,  ## data is stored as int16 which doesn't support `np.nan`, so we use this sentinel value.
            'lon'      : -179.9960938347692 + 0.007812330461578525 * np.arange(46081),
            'lat'      : -89.99376946560506 + 0.00781206004494716  * np.arange(23041),
            'metadata': {
                'title'   : 'Mars MGS MOLA DEM 463m',
                'units'   : 'm',
                'citation': 'Goddard Space Flight Center (2003). Mars MGS MOLA DEM 463m [Dataset]. Astrogeology PDS Annex, U.S. Geological Survey. https://astrogeology.usgs.gov/search/map/mars_mgs_mola_dem_463m',
            },
        },
        'DEM_200m': {
            'shape'    : (53347, 106694),
            'dtype'    : np.int16,
            'nan_value': -99_999,  ## data is stored as int16 which doesn't support `np.nan`, so we use this sentinel value.
            'lon'      : -179.9983129395848 + 0.0033741208306410017 * np.arange(106694),
            'lat'      : -89.99753689179012 + 0.0033741208306410004 * np.arange(53347),
            'metadata': {
                'title'   : 'Mars MGS MOLA - MEX HRSC Blended DEM Global 200m',
                'units'   : 'm',
                'citation': 'Fergason, R. L., Hare, T. M., & Laura, J. (2018). Mars MGS MOLA - MEX HRSC Blended DEM Global 200m v2 [Dataset]. Astrogeology PDS Annex, U.S. Geological Survey. https://astrogeology.usgs.gov/search/map/mars_mgs_mola_mex_hrsc_blended_dem_global_200m',
            },
        },
    }

    if model not in info:
        raise ValueError(f"Invalid topography model: '{model}'. Options are: {list(info.keys())}.")


    # if model.startswith('DEM_'):

    fpath = _get_fpath_dataset(model)

    dat = np.memmap(
        fpath,
        mode  = 'r',
        dtype = info[model]['dtype'],
        shape = info[model]['shape'],
    )

    metadata = info[model]['metadata']
    metadata['fpath'] = fpath

    is_slon = info[model]['lon'][0] < 0

    global _dat_topo
    _dat_topo = GriddedData(
        lon       = info[model]['lon'],
        lat       = info[model]['lat'],
        is_slon   = is_slon,
        data_dict = {'topo': dat},
        metadata  = metadata,
    )


    # else:
    #     raise ValueError(f"THE DEVELOPER MESSED UP. THIS SHOULD NOT HAPPEN.")

    return
