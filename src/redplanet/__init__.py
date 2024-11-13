## Define public API (self note: https://stackoverflow.com/questions/44834/what-does-all-mean-in-python)
__all__ = []


## TODO: current usage is `import redplanet; redplanet.set_dirpath_datacache(...)`, but since a lot more methods have been added, I'd like to created a specialized namespace to be more like `import redplanet; redplanet.user_config.set_dirpath_datacache(...)`.
from redplanet.user_config import (
    set_dirpath_datacache,
    get_dirpath_datacache,
    is_enabled_stream_hash_check,
    enable_stream_hash_check,
    get_max_size_to_calculate_hash_GiB,
    set_max_size_to_calculate_hash_GiB,
)
__all__.extend([
    'set_dirpath_datacache',
    'get_dirpath_datacache',
    'is_enabled_stream_hash_check',
    'enable_stream_hash_check',
    'get_max_size_to_calculate_hash_GiB',
    'set_max_size_to_calculate_hash_GiB',
])

from redplanet.DatasetManager.dataset_info import peek_datasets
__all__.extend([
    'peek_datasets',
])
