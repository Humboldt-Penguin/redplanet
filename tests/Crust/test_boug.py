import pytest
import numpy as np

from redplanet import Crust


def test_load_invalid():
    ## verify that an invalid model name raises an error
    with pytest.raises(ValueError, match='Invalid'):
        Crust.boug.load('meow')


def test_load_get_valid():
    ## verify that bouguer data can be downloaded, loaded, and accessed
    Crust.boug.load('Genova2016')

    ### global mean
    lons = np.linspace(-180, 360, 100)
    lats = np.linspace(-90, 90, 100)
    assert np.allclose( Crust.boug.get(lons, lats).mean() , -18.574545132436604 )

    ### wraparound
    lons = np.linspace(-180, 0, 100)
    lats = np.array([-60, 0, 60])
    assert np.allclose(
        Crust.boug.get(lons    , lats),
        Crust.boug.get(lons+360, lats)
    )
