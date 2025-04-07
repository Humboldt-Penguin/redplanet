# %%
from pathlib import Path

from tqdm import tqdm

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree



import redplanet as rp

from redplanet.DatasetManager.hash import _calculate_hash_from_file

from redplanet import Mag
from redplanet.Mag.depth.loader import get_dataset
from redplanet.helper_functions import geodesy

# %%
def latlon_to_xyz(lon, lat):
    ## convert a point to 3d cartesian coordinates
    lon, lat = np.radians(lon), np.radians(lat)
    x = np.cos(lat) * np.cos(lon)
    y = np.cos(lat) * np.sin(lon)
    z = np.sin(lat)
    return np.column_stack((x, y, z))

## build global KD-tree from the dataset
_data_df = get_dataset().copy()
_xyz = latlon_to_xyz(_data_df['lon'], _data_df['lat'])
_kdtree = cKDTree(_xyz)

def get_nearest_fast(lon: float, lat: float):
    ## Find the closest dipole from the dataset to the given (lon, lat) using a two-stage approach: a fast KD-tree lookup followed by an exact geodesic distance calculation on a small candidate set.

    ## convert the query point to 3d cartesian
    query_xyz = latlon_to_xyz([lon], [lat])[0]

    ## query KD-tree for 10 nearest candidates
    _, idx_candidates = _kdtree.query(query_xyz, k=10)

    candidates = _data_df.iloc[np.atleast_1d(idx_candidates)]
    distances_km = geodesy.get_distance(
        start = np.array([lon, lat]),
        end   = candidates[['lon', 'lat']].to_numpy(),
    )[:, 0] / 1e3

    ## find candidate with smallest geodesic distance.
    min_idx = np.argmin(distances_km)
    nearest = candidates.iloc[min_idx].copy()
    nearest['distance_km'] = distances_km[min_idx]

    return nearest

# %%
lons = np.arange(-180, 180.1, 0.5)
lats = np.arange(-90, 90.1, 0.5)

n_points = lons.size * lats.size
print(f'{n_points = }\n')


dat_idx_closest = np.empty((lats.size, lons.size))
for i, lat in enumerate(tqdm(lats, desc="Processing latitudes")):
    for j, lon in enumerate(lons):
        dat_idx_closest[i, j] = get_nearest_fast(lon, lat).name


fig, ax = rp.plot(
    lons, lats, dat_idx_closest,
    figsize = 10,
    hillshade = True,
)

# %%
x = dat_idx_closest.astype(np.int16)

assert np.allclose(
    dat_idx_closest,
    dat_idx_closest.astype(np.int16)
)

dat_idx_closest = dat_idx_closest.astype(np.int16)

# %%
dirpath_out = Path.cwd() / 'output'
dirpath_out.mkdir(parents=True, exist_ok=True)
fpath_out = dirpath_out / f'magdepth_nearest_dipole.npy'

np.save(fpath_outh, dat_idx_closest)

# %%
alg = 'xxh3_64'
calculated_hash = _calculate_hash_from_file(fpath_out, alg)
print(f'- {alg}: {calculated_hash}')
