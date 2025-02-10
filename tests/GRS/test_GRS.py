import pytest
import numpy as np

from redplanet import GRS
from redplanet.helper_functions.coordinates import CoordinateError

## `get` (public function) -- get GRS data
class Test__GRS_get:

    def test__GRS_get__valid(self):

        ## plain concentration
        assert np.isclose(
            GRS.get('th', 2.5, -7.5),
            0.572947204e-6
        )


        ## plain sigma
        assert np.isclose(
            GRS.get('th', 2.5, -7.5, quantity='sigma'),
            0.047707241e-6
        )


        ## nearest value (i.e. no interpolation)
        assert np.isclose(
            GRS.get('th', 2.5, -7.5),
            GRS.get('th', 2.51, -7.51),
        )


        ## array inputs
        expected_dat = np.array([
            [6.24730945e-07, 6.15593433e-07, 6.23700500e-07, 6.23700500e-07],
            [5.72947204e-07, 5.93936563e-07, 6.16395473e-07, 6.16395473e-07],
            [5.63852787e-07, 6.22758865e-07, 6.61521018e-07, 6.61521018e-07],
            [5.63852787e-07, 6.22758865e-07, 6.61521018e-07, 6.61521018e-07]
        ])
        expected_lons = np.array([  2.5,  7.5,  12.5,  12.5])
        expected_lats = np.array([ -2.5, -7.5, -12.5, -12.5])

        #### array input: list
        lons = [  4,  8,  12,  12.1 ]
        lats = [ -4, -8, -12, -12.1 ]
        actual_dat = GRS.get('th', lons, lats)
        assert np.allclose(actual_dat, expected_dat)

        #### array input: np.ndarray
        lons = np.array(lons)
        lats = np.array(lats)
        actual_dat = GRS.get('th', lons, lats)
        assert np.allclose(actual_dat, expected_dat)


        ## wraparound / slon<->plon conversion
        assert np.isclose(
            GRS.get('th', -180, 2.5),
            GRS.get('th',  180, 2.5),
        )
        assert np.isclose(
            GRS.get('th',   0, 2.5),
            GRS.get('th', 360, 2.5),
        )
        assert np.isclose(
            GRS.get('th', -90, 2.5),
            GRS.get('th', 270, 2.5),
        )


        ## normalize
        assert np.isclose(
            GRS.get('th', 2.5, -7.5, normalize=True),
            (
                GRS.get('th', 2.5, -7.5)
                / (1 - (   GRS.get('cl' , 2.5, -7.5)
                         + GRS.get('h2o', 2.5, -7.5)
                         + GRS.get('s'  , 2.5, -7.5) ))
            ),
        )



    def test__GRS_get__invalid(self):

            ## invalid element
            with pytest.raises(ValueError, match="not in list of supported elements"):
                GRS.get('invalid_element', 2.5, -7.5)

            ## can't normalize volatile elements
            for element in ['cl', 'h2o', 's']:
                with pytest.raises(ValueError, match="Can't normalize a volatile element"):
                    GRS.get(element, 2.5, -7.5, normalize=True)

            ## out-of-range coordinates
            with pytest.raises(CoordinateError, match="Longitude"):
                GRS.get('th', 361, 0)
            with pytest.raises(CoordinateError, match="Latitude"):
                GRS.get('th', 0, 91)
