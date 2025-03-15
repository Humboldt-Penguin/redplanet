import pandas as pd

from redplanet.Craters.loader import _get_dataset

from redplanet.helper_functions.coordinates import _verify_coords
from redplanet.helper_functions.docstrings.main import substitute_docstrings



@substitute_docstrings
def get(
    crater_id : str | list[str]     = None,
    name      : str | list[str]     = None,
    lon       : tuple[float, float] = None,
    lat       : tuple[float, float] = None,
    diameter  : tuple[float, float] = None,
    has_age   : bool                = None,
    as_dict   : bool                = False,
) -> pd.DataFrame | list[dict]:
    """
    Filter/query a dataset of craters >50km diameter, with ages/names when available. Calling this with no arguments will return the full dataset.

    We create a custom dataset (0.28 MiB) which unifies the following:

    1. Global database of Martian impact craters ({@Robbins2012_crater_db.p}).
    2. Crater ages from both Hartmann and Neukum isochron methods ({@Robbins2013_crater_ages.p}).
    3. IAU-approved crater nomenclature ({@IAU_crater_names.p}}).

    For more information and code to reproduce the dataset, see <https://github.com/Humboldt-Penguin/redplanet/tree/main/datasets/Craters>{target="_blank"} -- TODO: I'll eventually have a section on my website to describe datasets and how we modified them, add a link to that here.

    Parameters
    ----------
    crater_id : str | list[str], optional
        Unique crater identifier formatted ##-######, where the first two numbers indicate the Mars subquad and the last six number the craters in that subquad from largest to smallest diameter.
    name : str | list[str], optional
        Crater name according to official IAU nomenclature (as of 2024-11-26).
    lon : tuple[float, float], optional
        Filter craters whose center falls within this range of longitudes.

        The given range must be a subset of either [-180,180] or [0,360] -- e.g. `lon=[-170,350]` is not allowed (it doesn't make sense).
    lat : tuple[float, float], optional
        Filter craters whose center falls within this range of latitudes.
    diameter : tuple[float, float], optional
        Filter craters whose diameter falls within this range, in kilometers.
    has_age : bool, optional
        If True, only return craters with both Hartmann/Neukum isochron ages available. Default is False.
    as_dict : bool, optional
        If True, return the crater dataset as a list of dictionaries instead of a pandas DataFrame. Default is False.

    Returns
    -------
    pd.DataFrame | list[dict]
        Filtered list of craters with columns:

        - `id` : str
            - Unique crater identifier formatted ##-######, where the first two numbers indicate the Mars subquad and the last six number the craters in that subquad from largest to smallest diameter.
        - `name` : str
            - Crater name according to official IAU nomenclature (as of 2024-11-26).
        - `lat` : float
            - Latitude of the crater center.
        - `lon` : float
            - Longitude of the crater center, in range [-180,180].
        - 'plon' : float
            - Longitude of the crater center, in range [0,360].
        - `diam` : float
            - Diameter of the crater, in km.
        - `['diam_sd', 'diam_elli_major', 'diam_elli_minor', 'diam_elli_angle', 'diam_elli_major_sd', 'diam_elli_minor_sd']` : float
            - For more info, see Appendix A of {@Robbins2012_crater_db.n}.
        - `['N_H(10)', 'N_N(10)', 'N_H(25)', 'N_N(25)', 'N_H(50)', 'N_N(50)', 'Hartmann Isochron Age', 'Neukum Isochron Age', 'Hartmann Turn-Off Diameter', 'Neukum Turn-Off Diameter']` : None | list[float, float, float]
            - When available, the ages are given in a list where the first value is the estimated age and second/third are uncertainties (they will always be negative/positive respectively). All values are in billions of years (aka "giga-annums"/"Ga").
            - For more info, see Supplementary Table 3 of {@Robbins2013_crater_ages.n}.
    """

    df = _get_dataset()

    if crater_id:
        if isinstance(crater_id, str):
            crater_id = [crater_id]
        df = df[ df['id'].isin(crater_id) ]

    if name:
        if isinstance(name, str):
            name = [name]
        df = df[ df['name'].isin(name) ]


    if lon:
        _verify_coords(lon, 0)
        # lon = _plon2slon(lon)    ## this introduces unexpected/annoying behavior, TODO figure it out eventually lol (or add a plon col to df, and if any input lons are >180 then query that column instead lol)
        if lon[0] > 180 or lon[1] > 180:
            df = df[ df['plon'].between(lon[0], lon[1]) ]
        else:
            df = df[ df['lon'].between(lon[0], lon[1]) ]

    if lat:
        _verify_coords(0, lat)
        df = df[ df['lat'].between(lat[0], lat[1]) ]


    if diameter:
        df = df[ df['diam'].between(diameter[0], diameter[1]) ]

    if has_age:
        df = df[
            pd.notna(df['Hartmann Isochron Age']) &
            pd.notna(df['Neukum Isochron Age'])
        ]

    if as_dict:
        df = df.to_dict(orient='records')

    return df
