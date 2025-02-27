import pytest

from redplanet.DatasetManager.dataset_info import (
    _get_download_info,
    DatasetNotFoundError,
    MohoDatasetNotFoundError,
)



## `_get_download_info` (internal function) -- returns information to download a dataset
class Test__get_download_info:

    ## Valid input
    def test__get_download_info__grs_fname(self):
        result = _get_download_info(name='dichotomy_coords')
        assert result['fname'] == 'dichotomy_coordinates-JAH-0-360.txt'

    ## Invalid input: `name` not available
    def test__get_download_info__invalid_dataset(self):
        with pytest.raises( DatasetNotFoundError ):
            _get_download_info(name='https://fauux.neocities.org/')
