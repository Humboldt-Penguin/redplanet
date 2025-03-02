import pytest

from redplanet import Crust


def test_load_invalid():
    ## invalid model
    with pytest.raises(ValueError, match='Invalid'):
        Crust.topo.load('meow')

# not testing load/get since the datasets are huge
