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
    Get magnetic source depth data from Gong & Wieczorek 2021, sorted from closest to furthest from the given point.

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
        Information about 412 dipoles provided by Gong & Wieczorek 2021, sorted from closest to furthest from the given point. Columns are:

        - lon: float
        - lat: float
        - chi_reduced: float, "reduced chi^2 value of the best fitting model"
        - cap_radius_km: list[float], "angular radii of the magnetized caps (best-fit, and 1-sigma lower/upper limits)"
        - depth_km: list[float], "magnetization depth (best-fit, and 1-sigma lower/upper limits)"
        - dipole_mment_Am2: list[float], "square root of the metric N<M^2>V^2 [in A m^2] (best-fit, and 1-sigma lower/upper limits)"
        - distance_km: float, "distance from the given point to the dipole in km"

        Note that the 1-sigma lower/upper values are NaN when the minimum reduced chi^2 value of the best fitting model is outside the 1-sigma confidence level of the reduced chi^2 that were obtained from Monte Carlo simulations.
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
