from pathlib import Path
from platformdirs import user_cache_dir
import time

import pytest

from redplanet.user_config import get_dirpath_datacache, set_dirpath_datacache
from redplanet.DatasetManager.main import _get_fpath_dataset
from redplanet.DatasetManager.dataset_info import _get_download_info
from redplanet.DatasetManager.hash import _calculate_hash_from_file

## `_get_fpath_dataset` (internal function) -- download/cache dataset
class Test__get_fpath_dataset:

    ## Valid input: default & custom cache dirs
    def test__get_fpath_dataset__valid_default_cachedir(self, tmp_path):

        base_dirs = [
            Path(Path(user_cache_dir(appname='redplanet')).resolve()),
            tmp_path,   ## TODO: p sure there's a better way to test multiple inputs but idk if it works with my fixtures/logic, too lazy rn
        ]

        for base_dir in base_dirs:

            if base_dir == tmp_path: set_dirpath_datacache(base_dir)

            ## use an actual dataset instead of mock file so we can test full integration -- mock file test in `test_download.py`
            fpath_expected: Path =  base_dir / 'Crust' / 'dichotomy' / 'dichotomy_coordinates-JAH-0-360.txt'
            known_hash: str = _get_download_info('dichotomy_coords')['hash']['sha256']

            ## download file to cache & verify
            if (fpath_expected.is_file()): fpath_expected.unlink()
            fpath_actual = _get_fpath_dataset('dichotomy_coords')

            assert fpath_actual.is_file()
            assert fpath_actual == fpath_expected
            assert _calculate_hash_from_file(fpath_actual, 'sha256') == known_hash

            ## now try to download again, but recognize that the file already exists in cache since path returns immediately
            t0 = time.time()
            fpath_actual = _get_fpath_dataset('dichotomy_coords')
            assert time.time() - t0 < 0.1, "Dataset was previously downloaded to cache, but upon second access, we couldn't find it."

            ## cleanup (TODO: maybe this should be in a fixture...? I don't always wanna delete it though, maybe make a mock dataset file instead [note this contradicts previous comment about why using actual dataset instead of mock file for full integration])
            fpath_actual.unlink()
