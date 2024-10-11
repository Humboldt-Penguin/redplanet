import pytest

import redplanet.user_config as uc

@pytest.fixture(autouse=True)
def reset_datacache_dir():
    """
    Reset values in `redplanet/user_config.py` before every test.
    """
    uc._dirpath_datacache = None
    uc._enable_stream_hash_check = True