import pytest
import numpy as np

from redplanet import Mag


def test_load_invalid():
    ## verify that an invalid model name raises an error
    with pytest.raises(ValueError, match='Invalid'):
        Mag.sh.load('meow')


def test_load_get_valid():
    ## verify that magnetic field values can be downloaded, loaded, and accessed
    Mag.sh.load('Langlais2019')

    ### global mean
    lons = np.linspace(-180, 360, 100)
    lats = np.linspace(-90, 90, 100)
    assert np.allclose( Mag.sh.get(lons, lats).mean()                    , 455.1033973376897 )
    assert np.allclose( Mag.sh.get(lons, lats, quantity='radial').mean() , 16.08461829256901 )
    assert np.allclose( Mag.sh.get(lons, lats, quantity='theta' ).mean() , 1.340587063287876 )
    assert np.allclose( Mag.sh.get(lons, lats, quantity='phi'   ).mean() , 4.879693707789295 )

    ### wraparound
    lons = np.linspace(-180, 0, 100)
    lats = np.array([-60, 0, 60])
    assert np.allclose(
        Mag.sh.get(lons    , lats),
        Mag.sh.get(lons+360, lats)
    )
