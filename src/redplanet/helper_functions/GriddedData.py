from dataclasses import dataclass, field
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





@dataclass(frozen=True)
class GriddedData:



    ## PUBLIC INSTANCE VARIALES -- The dataclass is frozen, meaning the attributes are immutable, so we can safely access `myobject.lon` directly.
    lon       : np.ndarray
    is_slon   : bool
    lat       : np.ndarray
    data_dict : dict[str, np.ndarray]  ## datasets (2D numpy arrays) must be indexed by `[lat, lon]`, corresponding to the order in `self.lat` and `self.lon` respectively.
    metadata  : dict

    @property
    def data_vars(self) -> list[str]:
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
        return xr.Dataset(dat_vars, attrs=self.metadata)





    def get_values(
        self,
        lon                 : float | np.ndarray,
        lat                 : float | np.ndarray,
        var                 : str,
        return_exact_coords : bool = False,
        as_xarray           : bool = False
    ) -> float | np.ndarray | dict[str, np.ndarray] | xr.Dataset:

        ## input validation
        if var not in self.data_vars:
            raise ValueError(f'Unknown data variable: \"{var}\".\nOptions are: \"{"\", \"".join(self.data_vars)}\".')

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


        ## TODO: test these return types more, I barely use them and I'm not sure if they fully work as intended... (for swaths, also add a `unique_coords` option)
        if as_xarray:
            if return_exact_coords:
                lon = self.lon[idx_lon]
                lat = self.lat[idx_lat]
            dat = xr.DataArray(
                data = dat,
                dims = ['lat', 'lon'],
                coords = {
                    'lat': lat,
                    'lon': lon,
                },
                attrs = self.metadata,
            )
            return dat

        if return_exact_coords:
            return {
                "lon": self.lon[idx_lon],
                "lat": self.lat[idx_lat],
                "values": dat
            }

        return dat
