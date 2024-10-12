import numpy as np


def _plon2slon(plon: float) -> float:
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
    return ((plon-180) % 360) - 180



def _verify_coords(
    lon: float | np.ndarray,
    lat: float | np.ndarray,
) -> None:

    lon = np.array(lon)
    lat = np.array(lat)

    if np.any(lon < -180) or np.any(lon > 360):
        raise ValueError(f'Input coordinate in `lons` is out of range [-180, 360].')
    if np.any(lat < -90) or np.any(lat > 90):
        raise ValueError(f'Input coordinate in `lats` is out of range [-90, 90].')
