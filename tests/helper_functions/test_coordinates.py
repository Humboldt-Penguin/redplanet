import pytest
import numpy as np

from redplanet.helper_functions.coordinates import (
    _plon2slon,
    # _slon2plon,        ## TODO: test this, low priority though
    # _verify_coords,    ## TODO: test this, low priority though
)

class Test__plon2slon:

    test_values = (
        # (input, output)
        (-180  , -180  ),
        (-170  , -170  ),
        (-170.1, -170.1),
        (   0  ,    0  ),
        ( 170  ,  170  ),
        ( 170.1,  170.1),
        ( 180  , -180  ),
        ( 190  , -170  ),
        ( 190.1, -169.9),
        ( 350  ,  -10  ),
        ( 350.1,   -9.9),
        ( 360  ,    0  ),
    )

    def test__scalar(self):
        for x, y in self.test_values:
            yy = _plon2slon(x)
            np.testing.assert_allclose(y, yy)
            assert isinstance( yy, (int,float) )

    def test__list(self):
        x_list, y_list = zip(*self.test_values)
        yy_list = _plon2slon(x_list)
        np.testing.assert_allclose(y_list, yy_list)
        assert isinstance( yy_list, (list,tuple) )

    def test__numpy_array(self):
        x_list, y_list = zip(*self.test_values)
        x_arr = np.array(x_list)
        y_arr = np.array(y_list)
        yy_arr = _plon2slon(x_arr)
        np.testing.assert_allclose(y_arr, yy_arr)
        assert isinstance( yy_arr, np.ndarray )

    def test__empty(self):
        assert _plon2slon([]) == []
        np.testing.assert_allclose( _plon2slon(np.array([])), np.array([]) )
