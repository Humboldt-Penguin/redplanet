import pytest
import numpy as np

from redplanet import Crust
from redplanet.helper_functions import CoordinateError


def test__Crust_dichotomy__valid():

    ## ensure data integrity
    dat_dichotomy_coords = Crust.get_dichotomy_coords()
    assert dat_dichotomy_coords.shape == (1467, 2)
    assert dat_dichotomy_coords.mean() == 95.79914792285959

    ## test the poles (sanity-check)
    lon = np.arange(-180,360,1)
    assert  Crust.is_above_dichotomy(lon,  90).all()
    assert ~Crust.is_above_dichotomy(lon, -90).all()

    ## test some points around the equator to make sure lons are correct
    assert  Crust.is_above_dichotomy(np.arange(-180, -80), 0).all()
    assert ~Crust.is_above_dichotomy(np.arange( -75, 120), 0).all()
    assert  Crust.is_above_dichotomy(np.arange( 130, 270), 0).all()
    assert ~Crust.is_above_dichotomy(np.arange( 285, 360), 0).all()


def test__Crust_dichotomy__invalid():

    ## out-of-range coordinates
    with pytest.raises(CoordinateError, match="Longitude"):
        Crust.is_above_dichotomy(-181, 0)
    with pytest.raises(CoordinateError, match="Longitude"):
        Crust.is_above_dichotomy(361, 0)
    with pytest.raises(CoordinateError, match="Latitude"):
        Crust.is_above_dichotomy(0, -91)
    with pytest.raises(CoordinateError, match="Latitude"):
        Crust.is_above_dichotomy(0, 91)
