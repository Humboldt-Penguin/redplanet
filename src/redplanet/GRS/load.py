import zipfile

import pandas as pd
import xarray as xr

from redplanet.DatasetManager.master import _get_fpath_dataset



_dat_grs: xr.Dataset | None = None



def _get_dataset() -> xr.Dataset:
    if _dat_grs is None:
        _load()
    return _dat_grs



def _load() -> None:
    """
    NOTE:
        - This is private because there's only one GRS dataset so lazy loading upon the first access is fine.
            - To contrast, in other modules like Crust.topo / Crust.moho, we want the user to explicitly/deliberately call `load(<model_params>)` so they're aware of the different models available and which one they are choosing to use.
    """

    global _dat_grs

    fpath_dataset = _get_fpath_dataset('GRS')

    ## open zipfile and iterate over files
    with zipfile.ZipFile(fpath_dataset, 'r') as zipped_dir:
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
            df['element'] = element_name    # adds 'element' column
            df = df.set_index(['element', 'lat', 'lon'])    # multi-indexing to allow for conversion to xarray, looks like this: https://files.catbox.moe/b2wpsp.png
            ds = xr.Dataset.from_dataframe(df)
            if _dat_grs is None:
                _dat_grs = ds
            else:
                _dat_grs = xr.concat( [_dat_grs, ds], dim='element' )

    ## metadata
    _dat_grs.attrs = {
        'units': 'concentration out of 1',
        'grid_spacing': 5,
    }
