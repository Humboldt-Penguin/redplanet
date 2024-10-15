import numpy as np


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



def _verify_coords(
    lon: float | list | np.ndarray,
    lat: float | list | np.ndarray,
) -> None:

    lon = np.array(lon)
    lat = np.array(lat)

    if np.any(lon < -180) or np.any(lon > 360):
        raise ValueError(f'One or more of input coordinates ({lon = }) is out of range [-180, 360].')
    if np.any(lat < -90) or np.any(lat > 90):
        raise ValueError(f'One or more of input coordinates ({lat = }) is out of range [-90, 90].')
