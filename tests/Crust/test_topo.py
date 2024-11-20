import pytest
import numpy as np

from redplanet import Crust
from redplanet.helper_functions import CoordinateError


def test_bad_model():
    with pytest.raises(ValueError, match='Invalid model'):
        Crust.topo.load('meow')

# TODO (too lazy teehee)
# def test_access():
