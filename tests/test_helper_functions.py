import pytest
import numpy as np

from redplanet.helper_functions import (
    _plon2slon,
    # _verify_coords,   ## TODO: test this, low priority though
)


def test__plon2slon():
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

    ## type: scalar
    for x, y in test_values:
        yy = _plon2slon(x)
        np.testing.assert_allclose(y, yy)
        assert isinstance( yy, (int,float) )

    ## type: list
    x_list, y_list = zip(*test_values)
    yy_list = _plon2slon(x_list)
    np.testing.assert_allclose(y_list, yy_list)
    assert isinstance( yy_list, (list,tuple) )

    ## type: numpy array
    x_arr = np.array(x_list)
    y_arr = np.array(y_list)
    yy_arr = _plon2slon(x_arr)
    np.testing.assert_allclose(y_arr, yy_arr)
    assert isinstance( yy_arr, np.ndarray )

    ## empty
    assert _plon2slon([]) == []
    np.testing.assert_allclose( _plon2slon(np.array([])), np.array([]) )
