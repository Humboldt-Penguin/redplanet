import numpy as np
import pandas as pd

from redplanet.Mag.depth.loader import get_dataset

from redplanet.helper_functions import geodesy
from redplanet.helper_functions.coordinates import _plon2slon





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
