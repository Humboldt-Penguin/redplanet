import numpy as np
import pyshtools as pysh

from redplanet.DatasetManager.main import _get_fpath_dataset
from redplanet.helper_functions.GriddedData import GriddedData

from redplanet.helper_functions.docstrings.main import substitute_docstrings





_dat_mag: GriddedData | None = None

@substitute_docstrings
def get_dataset() -> GriddedData:
    """
    {fulldoc.get_dataset_GriddedData}
    """
    if _dat_mag is None:
        raise ValueError('Bouguer dataset not loaded. Use `redplanet.Mag.sh.load(<model_params>)`.')
    return _dat_mag

@substitute_docstrings
def get_metadata() -> dict:
    """
    {fulldoc.get_metadata}
    """
    return dict(get_dataset().metadata)





@substitute_docstrings
def load(
    model : str = None,
    lmax  : int = 134,
) -> None:
    """
    Load a magnetic field model for Mars.

    Parameters
    ----------
    model : str
        Name of the magnetic field model to load. Options are:

        - `'Langlais2019'` (0.081 MiB) — Spherical harmonic model of the magnetic field of Mars with a spatial resolution of ~160 km at the surface, corresponding to spherical harmonic degree 134. Integrates data from MGS magnetometer, MGS electron reflectometer, and MAVEN magnetometer.
            - Dataset downloaded from {@Langlais2019_data.n}. The full paper discusses/analyzes the models in detail ({@Langlais2019_paper.p}).
            - We process spherical harmonic coefficients with `pyshtools` ({@shtools_code.p}; {@shtools_paper.p}).
    lmax : int, optional
        The maximum spherical harmonic degree of the coefficients to load. Default is 134 (maximum for 'Langlais2019').

    Raises
    ------
    ValueError
        If an invalid model name is provided.
    """

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

    return
