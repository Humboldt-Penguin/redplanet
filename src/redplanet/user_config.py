from pathlib import Path
from typing import Optional
from platformdirs import user_cache_dir    # type: ignore
##                                           ^ [mypy says] error: Cannot find implementation or library stub for module named "platformdirs"  [import-not-found]



_dirpath_datacache: Optional[Path] = None
# _lock_thread = Lock() ## not sure if necessary... (use like: `with _lock_thread: ...`)





def get_dirpath_datacache() -> Path:
    """
    Get the data path where datasets are downloaded/cached. Initializes to default path if not set.

    Returns:
        Path: The current data path.

    [DEV NOTES]
        - It's good design to defer initialization of default value until first access in `get_dirpath_datacache()`...
            - This way, we avoid any overhead or side-effects of executing any potentially expensive / unnecessary code (esp related to file system operations) during the module import (i.e. lazy initialization).
    """

    ## Lazy load
    global _dirpath_datacache
    if _dirpath_datacache is None:
        ## Default value is '/home/USERNAME/.cache/redplanet/'
        _dirpath_datacache = Path(user_cache_dir(appname="redplanet")).resolve()

    return _dirpath_datacache



def set_dirpath_datacache(target_path: str | Path) -> None:
    """
    Set the data path where datasets will be downloaded/cached.

    Args:
        path: str or Path
            The file system path to store datasets.
    """

    ## Type validation
    if not (isinstance(target_path, str) or isinstance(target_path, Path)):
        raise TypeError("Path must be a string or a Path object.")

    ## If given a string, convert to Path object
    if isinstance(target_path, str):
        try:
            target_path = Path(target_path).resolve()
        except Exception as e:
            raise ValueError(f"Invalid path string provided: {e}")

    ## Proceed
    global _dirpath_datacache
    _dirpath_datacache = target_path
    return