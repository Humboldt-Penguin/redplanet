import pytest

import redplanet.user_config as rpcfg

@pytest.fixture(autouse=True)
def reset_user_config():
    """
    Reset values in `redplanet.user_config` before every test.
    """
    rpcfg.datacache._dirpath_datacache                  = None
    rpcfg.max_hash_size._max_size_to_calculate_hash_GiB = None
    rpcfg.stream_hash_check._enable_stream_hash_check   = True
