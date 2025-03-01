import zipfile

import pandas as pd
import xarray as xr

from redplanet.DatasetManager.main import _get_fpath_dataset
from redplanet.helper_functions.GriddedData import GriddedData

from redplanet.helper_functions.docstrings.main import substitute_docstrings





_dat_grs: GriddedData | None = None

@substitute_docstrings
def get_dataset() -> GriddedData:
    """
    {fulldoc.get_dataset_GriddedData}
    """
    if _dat_grs is None:
        _load()
    return _dat_grs

@substitute_docstrings
def get_metadata() -> dict:
    """
    {fulldoc.get_metadata}
    """
    return dict(get_dataset().metadata)





@substitute_docstrings
def _load() -> None:
    """
    Load the GRS dataset.

    For more information on the dataset, see `help(redplanet.GRS.get)`.

    {note._load}
    """

    fpath = _get_fpath_dataset('GRS_v2')

    df = pd.read_excel(
        fpath,
        engine='calamine',  # `python-calamine` takes ~0.09s, while `openpyxl` takes ~0.6s! Old method (unzipping) takes ~0.1-0.2s altogether.
        na_values=0,
    ).dropna(axis=1, how='all')


    df.columns = (
        df.columns
        .str.lower()
        .str.replace('latitude', 'lat')
        .str.replace('longitude', 'lon')
        .str.replace(' wt%', '_concentration')
        .str.replace(' wt %', '_concentration')
        .str.replace(' ppm', '_concentration')
        .str.replace(' sigma', '_sigma')
    )

    for col in df.columns:
        if col in ['lat', 'lon']:
            continue

        if 'th' in col:
            scale_factor = 0.000001  # convert "ppm" to mass fraction (out of 1)
        else:
            scale_factor = 0.01      # convert "weight percent" (0-100) to mass fraction (out of 1)
        df[col] = df[col] * scale_factor

    df = df.set_index(['lat', 'lon'])


    ds = xr.Dataset.from_dataframe(df)
    ds['cl+h2o+s_concentration'] = ds['cl_concentration'] + ds['h2o_concentration'] + ds['s_concentration']
    ds['cl+h2o+s_sigma'] = ds['cl_sigma'] + ds['h2o_sigma'] + ds['s_sigma']

    # ds['cl+h2o+s_concentration'] = ds['cl+h2o+s_concentration'].fillna(0)
    # ds['cl+h2o+s_sigma'] = ds['cl+h2o+s_sigma'].fillna(0)


    data_dict = {}
    for var in ds.data_vars:
        data_dict[var] = ds[var].values

    global _dat_grs
    _dat_grs = GriddedData(
        lon       = ds.lon.values,
        lat       = ds.lat.values,
        is_slon   = True,
        data_dict = data_dict,
        metadata  = {
            'description'   : '2001 Mars Odyssey Gamma Ray Spectrometer Element Concentration Maps',
            'units'         : 'mass fraction (out of 1)',
            'grid_spacing'  : 5,
            'links'         : {
                'paper'     : 'https://doi.org/10.1029/2022GL099235',
                'download'  : 'https://data.mendeley.com/datasets/3jd9whd78m/1',
            },
            'fpath'         : fpath,
        },
    )

    return
