import numpy as np

from redplanet import Crust
from redplanet import Craters

from redplanet.helper_functions import geodesy





def get_concentric_ring_coords(
    lon                 : float,
    lat                 : float,
    radius_km           : float,
    dist_btwn_rings_km  : float = 5,
    num_rings           : int   = None,
    dist_btwn_points_km : float = 5,
) -> list[ np.ndarray, list[np.ndarray] ]:

    '''Type checking'''
    if not (bool(dist_btwn_rings_km) ^ bool(num_rings)):  ## XOR
        raise ValueError('Must specify either `dist_btwn_rings_km` or `num_rings`, not neither/both.')


    '''Get radii for a series of concentric rings, starting at the center and going up to a distance of `radius_km`.'''
    if dist_btwn_rings_km:
        ring_radius_km__per_ring = np.arange  (0, radius_km, dist_btwn_rings_km)
    else:
        ring_radius_km__per_ring = np.linspace(0, radius_km, num_rings)


    '''Calculate the number of points that can fit in each ring such that each point is `dist_btwn_points_km` away from its neighbors.'''
    ## Given a circle with radius `r`, the number of points you could fit around the circumference (`2*pi*r`) such that every point is distance `x` from its neighbors is given by `2*pi*r/x`.
    num_points__per_ring = np.ceil(2 * np.pi * ring_radius_km__per_ring / dist_btwn_points_km).astype(int)
    ## note: we're using ceil here to ensure atleast 1 point per ring :)    (i think???)

    ## enforce a minimum number of points per ring, this is fairly subjective
    min_num_points = 10
    num_points__per_ring[ num_points__per_ring < min_num_points ] = min_num_points


    '''Generate (lon,lat) coordinates for each point on each ring.'''
    ring_coords__per_ring = []
    for (ring_radius_km, num_points) in zip(ring_radius_km__per_ring, num_points__per_ring):
        ## Generate the (lon,lat) coordinates of `num_points` points around the circle of radius `ring_radius_km`.
        ring_coords = geodesy.make_circle(
            lon = lon,
            lat = lat,
            radius = ring_radius_km * 1e3,
            n_samples = num_points,
            endpoint = False,
        )
        ring_coords__per_ring.append(ring_coords)

    return [ ring_radius_km__per_ring, ring_coords__per_ring ]





def get_topo_profile(
    ring_coords__per_ring : list[np.ndarray],
    model                 : str = 'DEM_463m',
) -> np.ndarray:
    """
    This function computes a one-dimensional radial profile of a given dataset by averaging values along multiple radial slices from a specified center coordinate out to a given radius.
    """

    Crust.topo.load(model=model)

    elevations_km__per_ring = []
    for ring_coords in ring_coords__per_ring:
        elevations_km = []
        for (lon,lat) in ring_coords:
            elevations_km.append(Crust.topo.get(lon,lat) / 1e3)
        elevations_km__per_ring.append(elevations_km)

    avg_elevation_km__per_ring = np.array([np.mean(elevations_km) for elevations_km in elevations_km__per_ring])

    return avg_elevation_km__per_ring