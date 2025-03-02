import pytest
import numpy as np

from redplanet import Crust
from redplanet.DatasetManager.dataset_info import MohoDatasetNotFoundError



def test_load_invalid():

    ## invalid interior (`ValueError`)
    with pytest.raises(ValueError, match='Unknown interior model'):
        Crust.moho.load(
            interior_model    = 'meow',
            insight_thickness = 40,
            rho_south         = 2900,
            rho_north         = 2900,
        )

    ## valid interior, but model not found -- 1/2: custom error `MohoDatasetNotFoundError`
    with pytest.raises(MohoDatasetNotFoundError):
        Crust.moho.load(
            interior_model    = 'Khan2022',
            insight_thickness = 0,
            rho_south         = 0,
            rho_north         = 0,
        )

    ## valid interior, but model not found -- 2/2: fail silently
    found = Crust.moho.load(
        interior_model    = 'Khan2022',
        insight_thickness = 0,
        rho_south         = 0,
        rho_north         = 0,
        fail_silently     = True,
    )
    assert (not found)



def test_registry():
    Crust.moho.get_registry().shape == (21894, 4)



def test_load_get_valid():
    ## verify that moho spherical harmonic coefficients can be downloaded, loaded, accessed (plain value and crustal thickness), and switched between models
    lons = np.linspace(-180, 360, 100)
    lats = np.linspace(-90, 90, 100)

    Crust.moho.load(
        interior_model = 'Khan2022',
        insight_thickness = 39,
        rho_south = 2700,
        rho_north = 2700,
    )
    assert np.allclose( Crust.moho.get(lons, lats).mean()               , 3335011.619244110 )
    assert np.allclose( Crust.moho.get(lons, lats, crthick=True).mean() , 51386.64291032735 )

    Crust.moho.load(
        interior_model = 'Khan2022',
        insight_thickness = 41,
        rho_south = 2900,
        rho_north = 2900,
    )
    assert np.allclose( Crust.moho.get(lons, lats).mean()               , 3327826.760446502 )
    assert np.allclose( Crust.moho.get(lons, lats, crthick=True).mean() , 58571.50170793515 )


    ## wraparound
    lons = np.linspace(-180, 0, 100)
    lats = np.array([-60, 0, 60])
    assert np.allclose(
        Crust.moho.get(lons    , lats),
        Crust.moho.get(lons+360, lats)
    )
