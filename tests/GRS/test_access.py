import pytest
import numpy as np

from redplanet import GRS
from redplanet.helper_functions import CoordinateError

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

        ## TODO: array inputs/outputs
        ## nearest value (i.e. no interpolation)
        assert np.isclose(
            GRS.get('th', 2.5, -7.5),
            GRS.get('th', 2.51, -7.51),
        )

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
            with pytest.raises(CoordinateError, match="One or more of input coordinates"):
                GRS.get('th', 361, 0)
            with pytest.raises(CoordinateError, match="One or more of input coordinates"):
                GRS.get('th', 0, 91)
