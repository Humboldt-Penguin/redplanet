import pytest
import numpy as np

from redplanet import Crust
from redplanet.DatasetManager.dataset_info import MohoDatasetNotFoundError
from redplanet.helper_functions.coordinates import CoordinateError


def test_invalid_interior_model():
    args = {
        'interior_model'   : 'meow',
        'insight_thickness': 40,
        'rho_south'        : 2900,
        'rho_north'        : 2900,
    }

    with pytest.raises(ValueError, match='Unknown interior model'):
        Crust.moho.load(**args)


def test_model_not_found():
    args = {
        'interior_model'   : 'Khan2022',
        'insight_thickness': 0,
        'rho_south'        : 0,
        'rho_north'        : 0,
    }

    ## default behavior: raise custom error `MohoDatasetNotFoundError`
    with pytest.raises(MohoDatasetNotFoundError):
        Crust.moho.load(**args)

    ## fail silently (returns False)
    found = Crust.moho.load(**args, fail_silently=True)
    assert (not found)


# TODO (too lazy teehee)
# def test_access():
