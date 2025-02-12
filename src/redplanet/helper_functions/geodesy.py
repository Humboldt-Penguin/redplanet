import numpy as np
import cartopy.geodesic as cg


'''
Mars reference ellipsoid (Oblate ellipsoid), 2009
- Parameters:
    - Semimajor axis   : 3395428 m
    - Flattening       : 0.005227617843759314
    - GM               : 42828372000000.0 m³/s²
    - Angular velocity : 7.0882181e-05 rad/s
- Sources:
    - Main:
        - Ardalan, A. A., Karimi, R., & Grafarend, E. W. (2009). A New Reference Equipotential Surface, and Reference Ellipsoid for the Planet Mars. Earth, Moon, and Planets, 106, 1-13.
        - https://doi.org/10.1007/s11038-009-9342-7
    - (Found it here:)
        - https://www.fatiando.org/boule/latest/ellipsoids.html
'''
_semimajor_m = 3395428
_flattening = 0.005227617843759314





'''
TODO: implement this myself at some point since I'm not using cartopy for anything else
    (for now we're just directly calling cartopy, but I wanted to put it in a module right away so it's easier to change later)

https://scitools.org.uk/cartopy/docs/latest/reference/generated/cartopy.geodesic.Geodesic.html
'''

__mars_geodesic: cg.Geodesic = None

def __get_mars_geodesic() -> cg.Geodesic:
    global __mars_geodesic
    if __mars_geodesic is None:
        __mars_geodesic = cg.Geodesic(
            radius     = _semimajor_m,
            flattening = _flattening,
        )
    return __mars_geodesic



def get_distance(
    start : list | np.ndarray,
    end   : list | np.ndarray,
) -> np.ndarray:
    """
    Calculate the geodesic distance between two points on the surface of Mars.

    Parameters
    ----------
    start : list | np.ndarray
        Array of shape (2) or (n_points, 2) containing the longitude and latitude coordinates of the starting point(s).
    end : list | np.ndarray
        Similar to `start`, but for the ending point(s).

    Returns
    -------
    np.ndarray
        Array of shape (n_points) [? verify this] containing the geodesic distances between the corresponding starting and ending point(s).

    See Also
    --------
    [cartopy.geodesic.Geodesic.circle](https://scitools.org.uk/cartopy/docs/latest/reference/generated/cartopy.geodesic.Geodesic.html)

    Notes
    -----
    Details on the Mars reference ellipsoid (oblate ellipsoid) used for these calculations:

    - Parameters:
        - Semimajor axis   : 3395428 m
        - Flattening       : 0.005227617843759314
        - GM               : 42828372000000.0 m³/s²
        - Angular velocity : 7.0882181e-05 rad/s
    - Sources:
        - Main:
            - Ardalan, A. A., Karimi, R., & Grafarend, E. W. (2009). A New Reference Equipotential Surface, and Reference Ellipsoid for the Planet Mars. Earth, Moon, and Planets, 106, 1-13.
            - https://doi.org/10.1007/s11038-009-9342-7
        - (Found it here:)
            - https://www.fatiando.org/boule/latest/ellipsoids.html

    For geodesic calculations, we use [cartopy.geodesic.Geodesic.circle](https://scitools.org.uk/cartopy/docs/latest/reference/generated/cartopy.geodesic.Geodesic.html).
    """
    geodesic = __get_mars_geodesic()
    return geodesic.inverse(start, end)



def move_forward(
    start    : list | np.ndarray,
    azimuth  : float | list | np.ndarray,
    distance : float,
) -> np.ndarray:
    """
    Calculate the coordinates of a point on the surface of Mars after moving a certain geodesic distance along a given angle.

    Parameters
    ----------
    start : list | np.ndarray
        Array of shape (2) containing the longitude and latitude coordinates of the starting point.
    azimuth : float | list | np.ndarray
        Array of shape (n_points) containing the azimuth angle(s) to "move forward" in degrees, where 0 is north and 90 is east.
    distance : float
        The geodesic distance to move forward in meters.

    Returns
    -------
    np.ndarray
        Array of shape (2) or (n_points, 2) [? verify this] containing the longitude and latitude coordinates of the point(s) after moving forward.

    See Also
    --------
    For more details about the reference ellipsoid and geodesic calculations, see `redplanet.helper_functions.geodesy.get_distance`.
    """
    geodesic = __get_mars_geodesic()
    return geodesic.direct(start, azimuth, distance)[:,:2]



def make_circle(
    lon       : float,
    lat       : float,
    radius    : float,  ## TODO: should this be suffixed with '_m' or '_km' to indicate units...?
    n_samples : int  = 180,
    endpoint  : bool = False,
) -> np.ndarray:
    """
    Generate a geodesic circle of points on the surface of Mars.

    Parameters
    ----------
    lon : float
        Longitude coordinate of the center of the circle, in range [-180, 360].
    lat : float
        Latitude coordinate of the center of the circle, in range [-90, 90].
    radius : float
        Radius of the circle in meters.
    endpoint : bool, optional
        If True, include the starting point at the end of the circle. Default is False.

    Returns
    -------
    np.ndarray
        Array of shape (n_samples, 2) [? verify this] containing the longitude and latitude coordinates of the circle points.

    See Also
    --------
    For more details about the reference ellipsoid, see `redplanet.helper_functions.geodesy.get_distance`.
    """
    geodesic = __get_mars_geodesic()
    return geodesic.circle(lon, lat, radius, n_samples, endpoint)
