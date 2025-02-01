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
    Returns info about 412 dipoles, sorted from closest to furthest from the given point.

    Columns are:
        'lon'               : float
        'lat'               : float
        'chi2_reduced'      : float
        'cap_radius_km'     : numpy array with 3 values -- best-fit, and 1-sigma lower/upper limits
        'depth_km'          : numpy array with 3 values -- best-fit, and 1-sigma lower/upper limits
        'dipole_moment_Am2' : numpy array with 3 values -- best-fit, and 1-sigma lower/upper limits
        'distance_km'       : float
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
