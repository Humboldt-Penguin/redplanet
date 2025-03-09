import numpy as np
import pyshtools as pysh

from redplanet.DatasetManager.main import _get_fpath_dataset
from redplanet.helper_functions.GriddedData import GriddedData

from redplanet.helper_functions.docstrings.main import substitute_docstrings

from redplanet.DatasetManager.dataset_info import MohoDatasetNotFoundError
from redplanet.Crust.moho.consts import _interior_models





_dat_moho: GriddedData | None = None

@substitute_docstrings
def get_dataset() -> GriddedData:
    """
    {fulldoc.get_dataset_GriddedData}
    """
    if _dat_moho is None:
        raise ValueError('Bouguer dataset not loaded. Use `redplanet.Crust.moho.load(<model_params>)`.')
    return _dat_moho

@substitute_docstrings
def get_metadata() -> dict:
    """
    {fulldoc.get_metadata}
    """
    return dict(get_dataset().metadata)





@substitute_docstrings
def load(
    interior_model    : str,
    insight_thickness : int | str,
    rho_south         : int | str,
    rho_north         : int | str,
    fail_silently     : bool = False,    ##  False [default] -> return None,  True -> return type(bool)
) -> None | bool:
    """
    Load a model of the Mohorovičić discontinuity (crust-mantle interface) with the given parameters. For a list of valid combinations of parameters (total 21,894 options), run `redplanet.Crust.moho.get_registry()` (returns a pandas DataFrame).

    Spherical harmonic coefficients are precomputed in {@Wieczorek2022_icta.n} and downloaded on-the-fly from our own mirror. The full paper discusses/analyzes the models in detail ({@Wieczorek2022_icta_paper.p}). We process spherical harmonic coefficients with `pyshtools` ({@shtools_code.p}; {@shtools_paper.p}).


    Parameters
    ----------
    interior_model : str
        Name of the interior model used for the mantle and core (see notes for more information).

        Options are: ['DWAK', 'DWThot', 'DWThotCrust1', 'DWThotCrust1r', 'EH45Tcold', 'EH45TcoldCrust1', 'EH45TcoldCrust1r', 'EH45ThotCrust2', 'EH45ThotCrust2r', 'Khan2022', 'LFAK', 'SANAK', 'TAYAK', 'YOTHotRc1760kmDc40km', 'YOTHotRc1810kmDc40km', 'ZG_DW']. See notes for more information.
    insight_thickness : int | str
        Assumed crustal thickness beneath the InSight landing site, in km.
    rho_south : int | str
        Average crustal thickness south of the dichotomy boundary, in kg/m^3.
    rho_north : int | str
        Average crustal thickness north of the dichotomy boundary, in kg/m^3.
    fail_silently : bool, optional
        - If False (default), raise `MohoDatasetNotFoundError` if there is no dataset for the given parameters.
        - If True, return True if the dataset was loaded successfully, or False if there is no dataset for the given parameters.


    Returns
    -------
    None | bool
        Return is determined as follows:

        |                         | **Successfully Loaded** | **Model Doesn't Exist**          |
        | ----------------------- | ----------------------- | -------------------------------- |
        | **fail_silently=False** | `None`                  | Raise `MohoDatasetNotFoundError` |
        | **fail_silently=True**  | `True`                  | `False`                          |


    Raises
    ------
    ValueError
        If `interior_model` is not one of the available options.
    MohoDatasetNotFoundError
        If the dataset is not found and `fail_silently` is False.


    Notes
    -----
    - More information on reference interior models:
        - [`ctplanet` function to read reference interior models (we don't use it, but it may be helpful if you're implementing this yourself)](https://markwieczorek.github.io/ctplanet/source/generated/ctplanet.ReadRefModel.html){target="_blank"}
        - [interior model files](https://github.com/MarkWieczorek/ctplanet/tree/74e8550080d4adc68ae291a500e8d198a40d437c/examples/Data/Mars-reference-interior-models){target="_blank"}
    """

    ## load moho

    if interior_model not in _interior_models:
        raise ValueError(
            f'Unknown interior model: "{interior_model}".\n'
            f'Options are: {", ".join(_interior_models)}.'
        )

    try:
        fpath_moho = _get_fpath_dataset(
            f'Moho-Mars-{interior_model}-{insight_thickness}-{rho_south}-{rho_north}'
        )
    except MohoDatasetNotFoundError as e:
        if fail_silently:
            return False
        else:
            raise

    ds_moho = (
        pysh.SHCoeffs.from_file(fpath_moho)
        .expand()
        .to_xarray()
        .isel(lat=slice(None, None, -1))  ## in pysh, lats are always decreasing at first
    )



    ## load shape

    fpath_shape = _get_fpath_dataset('MOLA_shape_719')

    ds_shape = (
        pysh.SHCoeffs.from_file(
            fpath_shape,
            lmax   = 90,
            format = 'bshc'
        )
        .expand()
        .to_xarray()
        .isel(lat=slice(None, None, -1))
    )



    ## GriddedData

    global _dat_moho

    _dat_moho = GriddedData(
        lon       = ds_moho.lon.values,
        lat       = ds_moho.lat.values,
        is_slon   = False,
        data_dict = {
            'moho'   : ds_moho.values,
            'crthick': (ds_shape - ds_moho).values,
        },
        metadata  = {
            'title': f'{interior_model}-{insight_thickness}-{rho_south}-{rho_north}',
            'units': 'm',
            'model_params': {
                'interior_model'      : interior_model,
                'insight_thickness_km': insight_thickness,
                'rho_south'           : rho_south,
                'rho_north'           : rho_north,
            },
            'lmax': 90,
            'source' : 'https://doi.org/10.5281/zenodo.6477509',
            'fpath': fpath_moho,
        },
    )



    if fail_silently:
        return True
    return
