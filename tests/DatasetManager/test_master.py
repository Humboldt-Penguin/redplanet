from pathlib import Path
from platformdirs import user_cache_dir

import pytest

from redplanet.user_config import get_dirpath_datacache, set_dirpath_datacache
from redplanet.DatasetManager.master import _get_fpath_dataset
from redplanet.DatasetManager.dataset_info import _get_download_info
from redplanet.DatasetManager.hash import _calculate_hash_from_file

## `_get_fpath_dataset` (internal function) -- download/cache dataset
class Test__get_fpath_dataset:

    ## Valid input: default cache dir
    def test__get_fpath_dataset__valid_default_cachedir(self):
        fpath_expected: Path = Path(user_cache_dir()).resolve() / 'redplanet' / 'Crust' / 'dichotomy' / 'dichotomy_coordinates-JAH-0-360.txt'
        known_hash: str = _get_download_info('dichotomy_coords')['hash']['sha256']

        ## delete file if it already exists
        if (fpath_expected.is_file()):
            fpath_expected.unlink()

        ## download file to cache
        fpath_actual = _get_fpath_dataset('dichotomy_coords')

        ## check file was downloaded properly
        assert fpath_actual == fpath_expected
        assert fpath_actual.is_file()
        assert _calculate_hash_from_file(fpath_actual, 'sha256') == known_hash

        ## now try to download again, but recognize that the file already exists
        ## TODO: i test this by seeing if it returns the path in under 0.1 seconds, i think??? further testing needed.
        fpath_actual = _get_fpath_dataset('dichotomy_coords')





    ## Valid input: custom cache dir
    def test__get_fpath_dataset__valid_custom_cachedir(self):
        ...
