import pytest
import numpy as np

from redplanet import Crust
from redplanet.helper_functions.coordinates import CoordinateError


def test_bad_model():
    with pytest.raises(ValueError, match='Invalid'):
        Crust.topo.load('meow')

# TODO (too lazy teehee)
# def test_access():
# def test_unloaded():
