import pytest

from redplanet.user_config import _dirpath_datacache

@pytest.fixture(autouse=True)
def reset_datacache_dir():
    """
    Reset the data cache directory before each test.
    """
    global _dirpath_datacache
    _dirpath_datacache = None


# from redplanet.user_config import set_dirpath_datacache_default
# @pytest.fixture(autouse=True)
# def reset_datacache_dir():
#     """
#     Reset the data cache directory to the default location before each test.
#     """
#     set_dirpath_datacache_default()