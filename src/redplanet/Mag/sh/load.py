import pyshtools as pysh
import xarray as xr

from redplanet.DatasetManager.master import _get_fpath_dataset





_dat_mag: xr.DataArray | None = None

def get_dataset() -> xr.DataArray:
    if _dat_mag is None:
        raise ValueError('Mag dataset not loaded. Use `redplanet.Mag.sh.load(<model_params>)`.')
    return _dat_mag





def load(
    model : str = None,
    lmax : int = 134,
) -> None | bool:

    options = ['Langlais2019']  ## I expect to add more later, maybe when Mittelholz publishes hers?

    if model not in options:
        raise ValueError(f'Unknown magnetic field model: \"{model}\".\nOptions are: \"{"\", \"".join(options)}\".')    # (lol)

    fpath = _get_fpath_dataset(model)

    global _dat_mag

    ## this is taken near verbatim from the `pyshtools` source code -- I rewrite it here for convenience
    _dat_mag = (
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
        .sortby('lat')
    )

    return
