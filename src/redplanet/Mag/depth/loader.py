from pathlib import Path
import zipfile

import numpy as np
import pandas as pd

from redplanet.DatasetManager.main import _get_fpath_dataset
from redplanet.helper_functions.coordinates import _plon2slon
from redplanet.helper_functions.docstrings.main import substitute_docstrings





_dat_depths: pd.DataFrame | None = None

@substitute_docstrings
def get_dataset(as_dict: bool = False) -> pd.DataFrame:
    """
    Get the full magnetic source depth dataset.

    Data (0.038 MiB) is provided by {@Gong2021_data.n}. The full paper discusses/analyzes the models in detail ({@Gong2021_paper.p}).


    Parameters
    ----------
    as_dict : bool, optional
        If True, return the data as a list of dictionaries. Default is False.


    Returns
    -------
    pd.DataFrame | list[dict]
        Information about all 412 dipoles. Columns are:

        - `lon` : float
            - Longitude in range [-180, 180].
        - `lat` : float
            - Latitude in range [-90, 90].
        - `chi_reduced` : float
            - "reduced chi^2 value of the best fitting model"
        - `cap_radius_km` : list[float]
            - "angular radii of the magnetized caps (best-fit, and 1-sigma lower/upper limits)"
        - `depth_km` : list[float]
            - "magnetization depth (best-fit, and 1-sigma lower/upper limits)"
        - `dipole_mment_Am2` : list[float]
            - "square root of the metric N<M^2>V^2 [in A m^2] (best-fit, and 1-sigma lower/upper limits)"

        Note that the 1-sigma lower/upper values are NaN when the minimum reduced chi^2 value of the best fitting model is outside the 1-sigma confidence level of the reduced chi^2 that were obtained from Monte Carlo simulations.
    """
    if _dat_depths is None:
        _load()
    if as_dict:
        return _dat_depths.to_dict(orient='records')
    return _dat_depths





@substitute_docstrings
def _load() -> None:
    """
    Load the magnetic source depth dataset.

    For more information on the dataset, see `help(redplanet.Mag.depth.get_nearest)`.

    {note._load}
    """

    fname2level = {
        '20_17_8_134_150.dat'      : 'middle',
        '20_17_8_134_150_lower.dat': 'lower',
        '20_17_8_134_150_upper.dat': 'upper',
    }
    cols = ['lat', 'lon', 'cap_radius_km', 'depth_km', 'dipole_moment_Am2', 'chi2_reduced']
    dict_dfs = {}

    fpath_zip = _get_fpath_dataset('Gong & Weiczorek, 2021')

    ## open zipfile and iterate over files
    with zipfile.ZipFile(fpath_zip, 'r') as zipped_dir:
        for zipped_file in zipped_dir.infolist():

            fpath_dat = zipped_file.filename

            level = fname2level.get(Path(fpath_dat).name)  ## this will be one of: ('middle', 'lower', 'upper', None)
            if level is None:
                continue

            with zipped_dir.open(fpath_dat) as fpath_dat_unzipped:
                df = pd.read_csv(
                    fpath_dat_unzipped,
                    sep = r'\s+',
                    names = cols
                )

            df['lon'] = df['lon'].apply(_plon2slon)
            df.replace( {-1e100: np.nan}, inplace=True )

            dict_dfs[level] = df


    ## directly copy constant columns
    cols_const = ['lon', 'lat', 'chi2_reduced']
    global _dat_depths
    _dat_depths = dict_dfs['middle'][cols_const].copy()

    ## for "leveled" quantities, merge them into a numpy array ordered `[middle, lower, upper]`
    cols_merge = ['cap_radius_km', 'depth_km', 'dipole_moment_Am2']
    for col in cols_merge:
        list_arrays = []
        for level in ['middle', 'lower', 'upper']:
            list_arrays.append( dict_dfs[level][col].to_numpy() )

        # _dat_depths[col] = np.column_stack(list_arrays).tolist()
        _dat_depths[col] = list( np.column_stack(list_arrays) )

    return
