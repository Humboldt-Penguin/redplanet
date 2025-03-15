import numpy as np


class CoordinateError(Exception):
    """
    Exception raised for coordinate values outside of acceptable range.
    """
    pass


def _verify_coords(
    lon: float | list | np.ndarray,
    lat: float | list | np.ndarray,
) -> None:
    """
    Verify that longitude and latitude values are within valid ranges ([-180, 360] and [-90, 90] respectively), otherwise raise a CoordinateError.

    Parameters
    ----------
    lon : float | list | np.ndarray
        Longitude value(s) to validate. Values are expected to be in the range [-180, 360].
    lat : float | list | np.ndarray
        Latitude value(s) to validate. Values are expected to be in the range [-90, 90].

    Raises
    ------
    CoordinateError
        If any longitude value is outside the range [-180, 360] or if any latitude value is outside the range [-90, 90].
    """
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
    Convert positive longitudes (in range [0, 360]) to signed longitudes (in range [-180, 180]). Inputs in range [-180, 0] are returned as is.

    Parameters
    ----------
    plon : float | list | np.ndarray
        Longitude value(s) in positive format.

    Returns
    -------
    float | list | np.ndarray
        Converted longitude value(s) in signed format. The return type matches the input type.

    Notes
    -----
    Actual mapping over the full input range:

    - [-180, 180) --> [-180, 180)
    - [180, 360]  --> [-180, 0]

    Self reminder:

    - Signed longitude   [-180, 180]  -->  Arabia Terra in middle & Hellas on right.
    - Positive longitude [0, 360]     -->  Olympus Mons in middle & Hellas on left.
    """
    def convert(plon):
        return ((plon - 180) % 360) - 180

    if isinstance(plon, (float, np.ndarray)):
        return convert(plon)
    else:
        return convert(np.array(plon)).tolist()


def _slon2plon(
    slon: float | list | np.ndarray
) -> float | list | np.ndarray:
    """
    Convert signed longitudes (in range [-180, 180]) to positive longitudes (in range [0, 360]). Inputs in range [180, 360] are returned as is.

    Parameters
    ----------
    slon : float | list | np.ndarray
        Longitude value(s) in signed format.

    Returns
    -------
    float | list | np.ndarray
        Converted longitude value(s) in positive format. The return type matches the input type.

    See Also
    --------
    _plon2slon : Converts positive longitudes to signed longitudes.
    """
    def convert(slon):
        return slon % 360

    if isinstance(slon, (float, np.ndarray)):
        return convert(slon)
    else:
        return convert(np.array(slon)).tolist()
