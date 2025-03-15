from pathlib import Path
from platformdirs import user_cache_dir    # type: ignore



_dirpath_datacache: Path = None
# _lock_thread = Lock() ## not sure if necessary... (use like: `with _lock_thread: ...`)



def get_dirpath_datacache() -> Path:
    """
    Get the data path where datasets are downloaded/cached. Initializes to default path ('/home/<user>/.cache/redplanet/') if not set.

    Returns
    -------
    Path

    Notes
    -----
    [DEVELOPER NOTES:]

    - It's good design to defer initialization of default value until first access in `get_dirpath_datacache()`...
        - This way, we avoid any overhead or side-effects of executing any potentially expensive / unnecessary code (esp related to file system operations) during the module import (i.e. lazy initialization).
    """
    ## Lazy load
    if _dirpath_datacache is None:
        set_dirpath_datacache(
            Path(user_cache_dir(appname='redplanet')).resolve()
        )
    return _dirpath_datacache



def set_dirpath_datacache(target_path: str | Path) -> None:
    """
    Set the data path where datasets will be downloaded/cached.

    Parameters
    ----------
    target_path : str | Path
        The file system path to store datasets.

    Raises
    ------
    TypeError
        Path must be a string or a Path object.
    ValueError
        Invalid path string provided.
    """
    ## Input type validation && conversion to Path object
    match target_path:

        case Path():
            target_path = target_path.resolve()

        case str():
            try:
                target_path = Path(target_path).resolve()
            except Exception as e:
                raise ValueError(f'Invalid path string provided: {target_path}\n{e}')

        case _:
            raise TypeError('Path must be a string or a Path object.')

    ## Proceed
    global _dirpath_datacache
    _dirpath_datacache = target_path
    return
