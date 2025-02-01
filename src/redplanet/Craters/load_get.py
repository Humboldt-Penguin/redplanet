import numpy as np
import pandas as pd

from redplanet.DatasetManager.master import _get_fpath_dataset
from redplanet.helper_functions.coordinates import (
    _verify_coords,
    # _plon2slon,
    _slon2plon,
)



_df_craters: pd.DataFrame | None = None



def get_dataset() -> pd.DataFrame:
    if _df_craters is None:
        _load()
    return _df_craters



def _load() -> None:
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




def get(
    crater_id : str | list[str]     = None,
    name      : str | list[str]     = None,
    lon       : tuple[float, float] = None,
    lat       : tuple[float, float] = None,
    diameter  : tuple[float, float] = None,
    has_age   : bool                = None,
    as_dict   : bool                = False,
) -> pd.DataFrame:

    df = get_dataset()

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
