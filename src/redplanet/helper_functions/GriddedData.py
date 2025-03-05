from dataclasses import dataclass
from types import MappingProxyType
from pprint import pformat
from textwrap import dedent, indent

import numpy as np
import xarray as xr

from redplanet.helper_functions.misc import find_closest_indices
from redplanet.helper_functions.coordinates import (
    _verify_coords,
    _plon2slon,
    _slon2plon,
)
from redplanet.helper_functions.docstrings.main import substitute_docstrings





@dataclass(frozen=True)
class GriddedData:



    ## PUBLIC INSTANCE VARIALES -- The dataclass is frozen, meaning the attributes are immutable, so we can safely access `myobject.lon` directly.
    lon       : np.ndarray
    is_slon   : bool  ## True if the longitudes are "signed" (i.e. in the range [-180, 180]), False if they are "positive" (i.e. in the range [0, 360]).
    lat       : np.ndarray
    data_dict : dict[str, np.ndarray]  ## datasets (2D numpy arrays) must be indexed by `[lat, lon]`, corresponding to the order in `self.lat` and `self.lon` respectively.
    metadata  : dict

    @property
    def data_vars(self) -> list[str]:
        """
        Get the names/keys of the data variables in the dataset. These are potential values for the `var` parameter in the `get_values` method.
        """
        return list(self.data_dict.keys())





    def __post_init__(self):

        ## make lon/lat arrays immutable
        object.__setattr__(self, 'lon', self.lon.copy())
        object.__setattr__(self, 'lat', self.lat.copy())
        self.lon.flags.writeable = False
        self.lat.flags.writeable = False

        ## make dicts immutable
        object.__setattr__(self, 'data_dict', MappingProxyType(self.data_dict))
        object.__setattr__(self, 'metadata' , MappingProxyType(self.metadata))

        # ## make data arrays immutable -- NEVERMIND, this can be a `np.memmap` and I don't want to copy/mess with that
        # immutable_data_dict = {
        #     key: array.copy().view() for key, array in self.data_dict.items()
        # }
        # for array in immutable_data_dict.values():
        #     array.flags.writeable = False
        # object.__setattr__(self, 'data_dict', immutable_data_dict)

        return

    def __str__(self) -> str:
        l = []
        l.append(dedent(
            f'''\
            GriddedData object:

            - Data variables:
                - {self.data_vars}

            - Data shape:
                - num_lons = {len(self.lon)}  (spacing = {self.lon[1] - self.lon[0]})
                - num_lats = {len(self.lat)}  (spacing = {self.lat[1] - self.lat[0]})

            - Metadata:\
            '''
        ))
        l.append(indent(pformat(dict(self.metadata)), prefix='    '))
        l = '\n'.join(l)
        return l





    def to_dict(self) -> dict:
        return {
            'lon': self.lon,
            'lat': self.lat,
            'dat': self.data_dict,
            'metadata': self.metadata,
        }

    def to_xarray(self) -> xr.Dataset:
        """
        Convert the GriddedData object to an xarray Dataset with coordinates `(lat, lon)`, one or more data variables, and information/metadata about the dataset in the attributes.
        """
        ## TODO: return dask array if data is too large...? for now, don't expose this method for stuff like topo.
        dat_vars = {
            key: xr.DataArray(
                data = array,
                dims = ['lat', 'lon'],
                coords = {
                    'lat': self.lat,
                    'lon': self.lon,
                },
                attrs = {
                    'long_name': key,
                },
            )
            for key, array in self.data_dict.items()
        }
        return xr.Dataset(dat_vars, attrs=dict(self.metadata))




    @substitute_docstrings
    def get_values(
        self,
        lon                 : float | np.ndarray,
        lat                 : float | np.ndarray,
        var                 : str,
        as_xarray           : bool = False
    ) -> float | np.ndarray | xr.DataArray:
        """
        Get specified dataset values at the specified coordinates.

        Parameters
        ----------
        {param.lon}
        {param.lat}
        var : str
            The name of the data variable to extract (i.e. one value from `self.data_vars`).
        {param.as_xarray}

        Returns
        -------
        {return.GriddedData}

        Raises
        ------
        ValueError
            If `var` is not one of the available data variables in the dataset (i.e. one value from `self.data_vars`).

        Notes
        -----
        This indexing/accessing approach is a full order of magnitude (sometimes more) faster than accessing an xarray DataArray/Dataset when it comes to random point-like accesses (namely the coordinates in concentric rings when doing radial cross-sectioning averages).

        `GriddedDataset` is used in the following modules: `Crust.boug`, `Crust.moho`, `Crust.topo`, `GRS`, `Mag.sh`.
        """

        ## input validation
        if var not in self.data_vars:
            raise ValueError(f'Unknown data variable: "{var}".\nOptions are: {", ".join(self.data_vars)}.')

        _verify_coords(lon, lat)

        if self.is_slon:
            lon = _plon2slon(lon)
        else:
            lon = _slon2plon(lon)

        lon = np.atleast_1d(lon)
        lat = np.atleast_1d(lat)


        ## get data
        idx_lon = find_closest_indices(self.lon, lon)
        idx_lat = find_closest_indices(self.lat, lat)

        dat_full = self.data_dict[var]
        dat = dat_full[np.ix_(idx_lat, idx_lon)]

        dat = np.squeeze(dat)  ## remove singleton dimensions
        if dat.ndim == 0: dat = dat.item()


        if as_xarray:
            dat = xr.DataArray(
                data = dat,
                dims = ['lat', 'lon'],
                coords = {
                    'lat': lat,
                    'lon': lon,
                },
                attrs = dict(self.metadata),
            )

        return dat
