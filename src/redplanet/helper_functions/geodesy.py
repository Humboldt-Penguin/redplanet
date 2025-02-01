"""TODO: CLEAN THIS UP LMAO"""



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



################################################################################
# ## overly complicated :/
# _mars_geodesic: cg.Geodesic = None

# def _get_geodesic_default() -> cg.Geodesic:
#     global _mars_geodesic
#     if _mars_geodesic is None:
#         _mars_geodesic = cg.Geodesic(
#             radius     = _semimajor_m,
#             flattening = _flattening,
#         )
#     return _mars_geodesic



# def _get_geodesic(
#     semimajor : float,
#     flattening: float,
# ) -> cg.Geodesic:
#     if semimajor == _semimajor_m and flattening == _flattening:
#         return get_default_geodesic()
#     return cg.Geodesic(
#         radius     = semimajor,
#         flattening = flattening,
#     )



################################################################################
# ## precomputing the geodesic saves like 10^-4 sec lol
# _default_geodesic = cg.Geodesic(
#     radius     = _semimajor_m,
#     flattening = _flattening,
# )

# def _get_geodesic(
#     semimajor : float = _semimajor_m,
#     flattening: float = _flattening,
# ) -> cg.Geodesic:
#     if semimajor == _semimajor_m and flattening == _flattening:
#         return _default_geodesic
#     else:
#         return cg.Geodesic(
#             radius     = semimajor,
#             flattening = flattening,
#         )



################################################################################

# def _get_geodesic(
#     semimajor : float = _semimajor_m,
#     flattening: float = _flattening,
# ) -> cg.Geodesic:
#     return cg.Geodesic(
#         radius     = semimajor,
#         flattening = flattening,
#     )


# def make_circle(
#     lon       : float,
#     lat       : float,
#     radius    : float,
#     n_samples : int  = 180,
#     endpoint  : bool = False,
# ) -> np.ndarray:
#     geodesic = _get_geodesic()
#     return geodesic.circle(lon, lat, radius, n_samples, endpoint)




################################################################################

'''
TODO: implement this myself at some point since I'm not using cartopy for anything else
    (for now we're just directly calling cartopy, but I wanted to put it in a module right away so it's easier to change later)
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



def make_circle(
    lon       : float,
    lat       : float,
    radius    : float,  ## TODO: should this be suffixed with '_m' or '_km' to indicate units...?
    n_samples : int  = 180,
    endpoint  : bool = False,
) -> np.ndarray:
    geodesic = __get_mars_geodesic()
    return geodesic.circle(lon, lat, radius, n_samples, endpoint)


def get_distance(start, end) -> np.ndarray:
    geodesic = __get_mars_geodesic()
    return geodesic.inverse(start, end)


def move_forward(start, azimuth, distance) -> np.ndarray:
    geodesic = __get_mars_geodesic()
    return geodesic.direct(start, azimuth, distance)[:,:2]

## https://scitools.org.uk/cartopy/docs/latest/reference/generated/cartopy.geodesic.Geodesic.html
