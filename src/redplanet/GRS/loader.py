import zipfile

import pandas as pd
import xarray as xr

from redplanet.DatasetManager.master import _get_fpath_dataset
from redplanet.helper_functions.GriddedData import GriddedData





_dat_grs: GriddedData | None = None

def get_dataset() -> GriddedData:
    if _dat_grs is None:
        _load()
    return _dat_grs





def _load():
    """
    NOTE:
        - This is private & less modular because there will only ever be one GRS dataset, so lazy loading upon the first access is fine.
        - In contrast, in other modules like Crust.topo / Crust.moho, we want the user to explicitly/deliberately call `load(<model_params>)` so they're aware of different models and which one they're choosing.
    """

    fpath = _get_fpath_dataset('GRS')
    ds = None

    ## open zipfile and iterate over files
    with zipfile.ZipFile(fpath, 'r') as zipped_dir:
        for zipped_file in zipped_dir.infolist():
            filename = zipped_file.filename
            if filename.startswith('README'):
                continue
            element_name = filename.split('_')[0].lower()


            ## read data file to pandas dataframe
            with zipped_dir.open(filename) as unzipped_file:
                df = pd.read_csv(
                    unzipped_file,
                    sep       = r'\s+',
                    na_values = 9999.999,
                    header    = 0,
                    usecols   = [0, 1, 2, 3],
                    names     = ['lat', 'lon', 'concentration', 'sigma']
                )


            ## convert units
            if element_name == 'th':
                scale_factor = 0.000001  # convert "ppm"            to concentration out of 1
            else:
                scale_factor = 0.01      # convert "weight percent" to concentration out of 1
            df[['concentration','sigma']] *= scale_factor


            ## convert to `pandas.DataFrame` to `xarray.DataSet`, and append to existing
            df['element'] = element_name  # adds 'element' column
            df = df.set_index(['element', 'lat', 'lon'])  # multi-indexing to allow for conversion to xarray, looks like this: https://files.catbox.moe/b2wpsp.png
            this_ds = xr.Dataset.from_dataframe(df)
            if ds is None:
                ds = this_ds
            else:
                ds = xr.concat( [ds, this_ds], dim='element' )


    ## Precompute volatiles
    volatiles = (
        ds
        .sel(element=['cl','h2o','s'])
        .sum(dim='element')
        .expand_dims({'element': ['cl+h2o+s']})
    )
    ds = xr.concat( [ds, volatiles], dim='element' )


    ## Now convert from xarray.DataSet to redplanet.GriddedData
    data_dict = {}

    for element in list(ds.element.values):
        for quantity in list(ds.data_vars):
            data_dict[f'{element}_{quantity}'] = ds[quantity].sel(element=element).values


    global _dat_grs
    _dat_grs = GriddedData(
        lon       = ds.lon.values,
        lat       = ds.lat.values,
        is_slon   = True,
        data_dict = data_dict,
        metadata  = {
            'description' : '2001 Mars Odyssey Gamma Ray Spectrometer Element Concentration Maps',
            'units'       : 'concentration out of 1',
            'elements'    : list(ds.element.values),
            'grid_spacing': 5,
            'links': {
                'download': 'https://repository.lsu.edu/geo_psl/1/',
                'paper'   : 'https://doi.org/10.1029/2022GL099235',
            },
            'fpath'       : fpath,
        },
    )
