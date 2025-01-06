import numpy as np
import xarray as xr

from redplanet.Crust.boug.load import get_dataset
from redplanet.helper_functions.coordinates import (
    _verify_coords,
    _slon2plon,
)



def get_model_info() -> dict:
    return get_dataset()[1]



def get(
    lon                 : float | np.ndarray,
    lat                 : float | np.ndarray,
    as_xarray           : bool = False,
    return_exact_coords : bool = False,
) -> np.ndarray | list[np.ndarray, np.ndarray, np.ndarray] | xr.DataArray:

    ## input validation
    _verify_coords(lon, lat)
    lon = _slon2plon(lon)
    lon = np.atleast_1d(lon)
    lat = np.atleast_1d(lat)

    dat_boug, model_info = get_dataset()
    dat_lon = model_info['lons']
    dat_lat = model_info['lats']


    def find_closest_indices(sorted_array: np.ndarray, target_values: np.ndarray) -> np.ndarray:
        insertion_indices = np.searchsorted(sorted_array, target_values)
        insertion_indices = np.clip(insertion_indices, 1, len(sorted_array) - 1)
        left_neighbors = sorted_array[insertion_indices - 1]
        right_neighbors = sorted_array[insertion_indices]
        closest_indices = np.where(
            np.abs(target_values - left_neighbors) <= np.abs(target_values - right_neighbors),
            insertion_indices - 1,
            insertion_indices
        )
        return closest_indices


    idx_lon = find_closest_indices(dat_lon, lon)
    idx_lat = find_closest_indices(dat_lat, lat)
    dat = dat_boug[np.ix_(idx_lat, idx_lon)]


    if as_xarray:
        if return_exact_coords:
            lon = dat_lon[idx_lon]
            lat = dat_lat[idx_lat]
        dat = xr.DataArray(
            data = dat,
            dims = ['lat', 'lon'],
            coords = {
                'lat': lat,
                'lon': lon,
            }
        )
        return dat

    if return_exact_coords:
        lon = dat_lon[idx_lon]
        lat = dat_lat[idx_lat]
        return dat, lon, lat

    return dat
