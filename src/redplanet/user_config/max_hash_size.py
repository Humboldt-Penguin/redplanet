"""
PURPOSE: Save yourself time by not calculating hashes for large local files (i.e. you're certain you haven't altered them, nor are they out of date).
"""


_max_size_to_calculate_hash_GiB: float | None = 1.0
## TODO: before publishing, initialize this to `None` so all hashes are calculated by default, and the user can decide if they want to disable the security feature. The logic for this is already in place in `redplanet.DatasetManager.main._get_fpath_dataset()`, so you just need to change the default value here.


def get_max_size_to_calculate_hash_GiB() -> float | None:
    """
    Get the maximum size of a local file (in GiB) for which a hash will be calculated in order to verify its integrity. If the file is larger than this size, the hash will not be calculated.

    Returns
    -------
    float | None

    Notes
    -----
    IMPLEMENTATION NOTE: if this returns `None`, then all hashes are calculated by default (to see implementation logic, check `redplanet.DatasetManager.main._get_fpath_dataset()`).
    """
    return _max_size_to_calculate_hash_GiB


def set_max_size_to_calculate_hash_GiB(value: float) -> None:
    """
    Set the maximum size of a local file (in GiB) for which a hash will be calculated in order to verify its integrity. If the file is larger than this size, the hash will not be calculated.

    Parameters
    ----------
    value : float
    """
    global _max_size_to_calculate_hash_GiB
    _max_size_to_calculate_hash_GiB = value
    return
