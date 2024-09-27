import pytest

from redplanet.user_config import _dirpath_datacache, _enable_stream_hash_check

@pytest.fixture(autouse=True)
def reset_datacache_dir():
    """
    Reset values in `redplanet/user_config.py` before every test.
    """
    global _dirpath_datacache, _enable_stream_hash_check
    _dirpath_datacache = None
    _enable_stream_hash_check = True


# from redplanet.user_config import set_dirpath_datacache_default
# @pytest.fixture(autouse=True)
# def reset_datacache_dir():
#     """
#     Reset the data cache directory to the default location before each test.
#     """
#     set_dirpath_datacache_default()