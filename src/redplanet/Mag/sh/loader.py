import numpy as np
import pyshtools as pysh

from redplanet.DatasetManager.master import _get_fpath_dataset
from redplanet.helper_functions.GriddedData import GriddedData





_dat_mag: GriddedData | None = None

def get_dataset() -> GriddedData:
    if _dat_mag is None:
        raise ValueError('Bouguer dataset not loaded. Use `redplanet.Mag.sh.load(<model_params>)`.')
    return _dat_mag

def get_metadata() -> dict:
    return dict(get_dataset().metadata)





def load(
    model: str = None,
    lmax : int = 134,
):

    ## I expect to add more later, so users should explicitly choose Genova2016 for forward compatibility. Mittelholz might be publishing hers soon.
    info = {
        'Langlais2019': {
            'metadata': {
                'description': 'Martian magnetic field model, based on 14386 ESD, inversion using MGS MAG, MGS ER and MAVEN MAG, field predicted at 150km altitude. SH model, ref surface =3393.5 km, from Langlais/Thebault/Houliez/Purucker/Lillis internal coefficients.',
                'units'      : 'nT',
                'lmax'       : lmax,
                'links'      : {
                    'data' : 'https://doi.org/10.5281/zenodo.3876714',
                    'paper': 'https://doi.org/10.1029/2018JE005854',
                },
            },
        },
    }

    if model not in info:
        raise ValueError(f"Invalid magnetic field model: '{model}'. Options are: {list(info.keys())}.")



    if model == 'Langlais2019':

        fpath = _get_fpath_dataset(model)

        '''
        - Arguments for `from_file` are taken directly from the `pyshtools` source code (`pyshools.datasets.Mars.Langlais2019()`).
            - I rewrite it so the dataset is downloaded to `redplanet` cache rather than `pyshtools` cache, ensuring `redplanet` can fully manage/clear its own dataset cache.
        '''
        ds = (
            pysh.shclasses.SHMagCoeffs.from_file(
                fpath,
                lmax       = lmax,
                skip       = 4,
                r0         = 3393.5e3,
                header     = False,
                file_units = 'nT',
                units      = 'nT',
                encoding   = 'utf-8',
            )
            .expand()
            .to_xarray()
            .isel(lat=slice(None, None, -1))  ## in pysh, lats are always decreasing at first
        )


        data_dict = {}
        for data_var in list(ds.data_vars):
            data_dict[data_var] = ds[data_var].values

        metadata = info[model]['metadata']
        metadata['fpath'] = fpath


        global _dat_mag
        _dat_mag = GriddedData(
            lon       = ds.lon.values,
            lat       = ds.lat.values,
            is_slon   = False,
            data_dict = data_dict,
            metadata  = metadata,
        )



    else:
        raise ValueError(f"THE DEVELOPER MESSED UP. THIS SHOULD NOT HAPPEN.")
