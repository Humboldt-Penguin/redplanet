import numpy as np
import pandas as pd

from redplanet.Mag.depth.loader import get_dataset

from redplanet.helper_functions import geodesy
from redplanet.helper_functions.coordinates import _plon2slon
from redplanet.helper_functions.docstrings.main import substitute_docstrings





def get_nearest(
    lon     : float,
    lat     : float,
    as_dict : bool = False,
) -> pd.DataFrame | list[dict]:
    """
    Get magnetic source depth data, sorted from closest to furthest from the given point.

    For source of the dataset, see references of `help(redplanet.Mag.depth.get_nearest)`.

    Parameters
    ----------
    lon : float
        Longitude coordinate in range [-180, 360].
    lat : float
        Latitude coordinate in range [-90, 90].
    as_dict : bool, optional
        If True, return the data as a list of dictionaries. Default is False.

    Returns
    -------
    pd.DataFrame | list[dict]
        Information about all 412 dipoles, sorted from closest to furthest from the given input coordinate. Columns are identical to those in `redplanet.Mag.depth.get_dataset` (look there for full explanations), with the addition of a computed column:

        - `distance_km` : float
            - Distance from the given input coordinate to the dipole, in km.
    """

    lon = _plon2slon(lon)

    df_depths = get_dataset().copy()

    distances_km = geodesy.get_distance(
        start = np.array([lon, lat]),
        end   = df_depths[['lon', 'lat']].to_numpy(),
    )[:,0] / 1.e3

    df_depths['distance_km'] = distances_km
    df_depths.sort_values('distance_km', inplace=True)

    if as_dict:
        df_depths = df_depths.to_dict(orient='records')

    return df_depths



@substitute_docstrings
def get_grid(
    lon : float | np.ndarray,
    lat : float | np.ndarray,
    col : str,
) -> np.ndarray:
    """
    Similar to `get_nearest`, but significantly more optimized for accessing data over large areas by using a pre-computed grid of nearest dipole locations.

    Parameters
    ----------
    {param.lon}
    {param.lat}
    col : str
        Name of dataset column to return. See `redplanet.Mag.depth.get_dataset` for options/explanations.

    Returns
    -------
    np.ndarray
        Data values at the input coordinates, with shape `(num_lats, num_lons)`. For columns with three values (e.g. `'depth_km'`), the shape will be `(3, num_lats, num_lons)`.

    Raises
    ------
    ValueError
        If the specified column is not found in the dataset.
    """

    df_depths, dat_nearest_dipole = get_dataset(_extras=True)

    if col not in df_depths.columns:
        raise ValueError(f"Column '{col}' not found in dataset. Available columns are: {df_depths.columns.tolist()}")

    col_values = np.stack(df_depths[col])
    dat_idx = dat_nearest_dipole.get_values(lon, lat, 'dat')

    dat_return = col_values[dat_idx]

    if dat_return.ndim == 3:
        dat_return = np.moveaxis(dat_return, 2, 0)

    return dat_return
