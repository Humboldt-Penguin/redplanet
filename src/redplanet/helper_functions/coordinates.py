import numpy as np



class CoordinateError(Exception): pass



def _verify_coords(
    lon: float | list | np.ndarray,
    lat: float | list | np.ndarray,
) -> None:

    lon = np.atleast_1d(lon)
    lat = np.atleast_1d(lat)

    invalid_lon = np.where((lon < -180) | (lon > 360))[0]
    invalid_lat = np.where((lat < -90) | (lat > 90))[0]

    if invalid_lon.size > 0:
        invalid_lon_values = lon[invalid_lon]
        error_msg = [
            f"Longitude coordinates must be in range [-180, 360].",
            f"The following input values were outside of this range:\n\t- {invalid_lon_values.tolist()}.",
            f"Corresponding input array indices:\n\t- {invalid_lon.tolist()}.",
        ]
        raise CoordinateError("\n".join(error_msg))

    if invalid_lat.size > 0:
        invalid_lat_values = lat[invalid_lat]
        error_msg = [
            f"Latitude coordinates must be in range [-90, 90].",
            f"The following input values were outside of this range:\n\t- {invalid_lat_values.tolist()}.",
            f"Corresponding input array indices:\n\t- {invalid_lat.tolist()}.",
        ]
        raise CoordinateError("\n".join(error_msg))



def _plon2slon(
    plon: float | list | np.ndarray
) -> float | list | np.ndarray:
    """
    Converts "positive" longitude in range [0,360] to "signed"/"standard" longitude in range [0,180]U[-180,0]. Input values less than 0 are unchanged.

    [Notes]
        - Actual mapping over full input range:
            - [-180, 180) --> [-180, 180)
            - [ 180, 360] --> [-180,   0]

        - self reminder:
            - signed lon   [-180,180]  -->  Arabia Terra in middle.
            - positive lon [   0,360]  -->  Olympus Mons in middle.
    """
    def convert(plon):
        return ((plon-180) % 360) - 180

    if isinstance(plon, (float, np.ndarray)):
        return convert(plon)
    else:
        return convert( np.array(plon) ).tolist()



def _slon2plon(
    slon: float | list | np.ndarray
) -> float | list | np.ndarray:
    """
    See `_plon2slon` for details.
    """
    def convert(slon):
        return slon % 360

    if isinstance(slon, (float, np.ndarray)):
        return convert(slon)
    else:
        return convert( np.array(slon) ).tolist()
