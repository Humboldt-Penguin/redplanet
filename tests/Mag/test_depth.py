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
