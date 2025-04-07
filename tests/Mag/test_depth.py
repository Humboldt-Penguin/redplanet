import pytest
import numpy as np

from redplanet import Mag



def test_load_get_valid():
    df = Mag.depth.get_dataset()

    assert df.shape == (412, 6)
    assert df.chi2_reduced.mean() == 1.2787405731700439

    near = Mag.depth.get_nearest(lon=10,lat=10,as_dict=True)[0]

    assert np.allclose(near['depth_km'], np.array([4., 2., 4.]))
    assert np.allclose(near['distance_km'], 283.51013951489193)


def test_get_grid():
    ### global mean
    lons = np.linspace(-180, 360, 100)
    lats = np.linspace(-90, 90, 100)
    assert np.allclose( Mag.depth.get_grid(lons, lats, 'depth_km')[0].mean() , 21.8046 )

    ### wraparound
    lons = np.linspace(-180, 0, 100)
    lats = np.array([-60, 0, 60])
    assert np.allclose(
        Mag.depth.get_grid(lons    , lats, 'depth_km'),
        Mag.depth.get_grid(lons+360, lats, 'depth_km'),
        equal_nan=True,
    )
