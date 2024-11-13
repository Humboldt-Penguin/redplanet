from pathlib import Path
from platformdirs import user_cache_dir    # type: ignore





_dirpath_datacache: Path | None = None
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
    if _dirpath_datacache is None:
        set_dirpath_datacache_default()
    return _dirpath_datacache



def set_dirpath_datacache_default() -> None:
    """
    Default user cache dir is '/home/USERNAME/.cache/redplanet/'
    """
    set_dirpath_datacache(
        Path(user_cache_dir(appname='redplanet')).resolve()
    )
    return



def set_dirpath_datacache(target_path: str | Path) -> None:
    """
    Set the data path where datasets will be downloaded/cached.

    Args:
        path: str or Path
            The file system path to store datasets.
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





_enable_stream_hash_check: bool = False

def is_enabled_stream_hash_check() -> bool:
    """
    Get the current value of the flag that determines whether we verify the hash of a file at URL by streaming before fully downloading it.
    """
    return _enable_stream_hash_check

def enable_stream_hash_check(value: bool) -> None:
    """
    Set the flag that determines whether we verify the hash of a file at URL by streaming before fully downloading it.
    """
    global _enable_stream_hash_check
    _enable_stream_hash_check = value
    return



_max_size_to_calculate_hash_GiB: float = 1.0
## TODO: maybe initially make this `999` | `None` | `-1` so all hashes are calculated by default, and the user can decide if they want to disable the security feature.

def get_max_size_to_calculate_hash_GiB() -> float:
    return _max_size_to_calculate_hash_GiB

def set_max_size_to_calculate_hash_GiB(value: float) -> None:
    global _max_size_to_calculate_hash_GiB
    _max_size_to_calculate_hash_GiB = value
    return
