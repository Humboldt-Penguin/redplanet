import numpy as np
import pandas as pd

from redplanet.DatasetManager.main import _get_fpath_dataset

from redplanet.helper_functions.coordinates import _slon2plon
from redplanet.helper_functions.docstrings.main import substitute_docstrings



_df_craters: pd.DataFrame | None = None


def _get_dataset() -> pd.DataFrame:
    """
    Returns the full crater dataset. If the dataset has not been loaded yet, it will be loaded.

    Returns
    -------
    pd.DataFrame
        For description of columns, see `help(redplanet.Craters.get)`.
    """
    if _df_craters is None:
        _load()
    return _df_craters


@substitute_docstrings
def _load() -> None:
    """
    Load the crater dataset.

    We create a custom database which unifies the following:

    1. Global database of Martian impact craters ({@Robbins2012_crater_db.p}).
    2. Crater ages from both Hartmann and Neukum isochron methods ({@Robbins2013_crater_ages.p}).
    3. IAU-approved crater nomenclature ({@IAU_crater_names.p}}).

    For more information and our code, see <https://github.com/Humboldt-Penguin/redplanet/tree/main/datasets/Craters>{target="_blank"}.

    - TODO: I'll eventually have a section on my website to describe datasets and how we modified them, add a link to that here.

    {note._load}
    """
    fpath_df = _get_fpath_dataset('crater_db')
    global _df_craters
    _df_craters = pd.read_csv(fpath_df)

    _df_craters['plon'] = _slon2plon(_df_craters['lon'])
    _df_craters = _df_craters.replace(np.nan, None)

    ## convert ages (e.g. '4.00;-0.08;0.05') to a list of floats
    columns_to_convert = [col for col in _df_craters.columns if col.startswith('N_') or col.endswith('Age')]
    def convert(val):
        if isinstance(val, str):
            parts = val.split(';')
            if len(parts) == 3:
                try:
                    return [float(part) for part in parts]
                except ValueError:
                    return None
        return None
    for col in columns_to_convert:
        _df_craters[col] = _df_craters[col].apply(convert)

    return
