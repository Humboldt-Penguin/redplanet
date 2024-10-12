import pytest

from redplanet.DatasetManager.dataset_info import _get_download_info



## `_get_download_info` (internal function) -- returns information to download a dataset
class Test__get_download_info:

    ## Valid input
    def test__get_download_info__grs_fname(self):
        result = _get_download_info(name='GRS')
        assert result['fname'] == '2022_Mars_Odyssey_GRS_Element_Concentration_Maps.zip'

    ## Invalid input: `name` not available
    def test__get_download_info__invalid_dataset(self):
        with pytest.raises(ValueError, match='Dataset not found:'):
            _get_download_info(name='https://fauux.neocities.org/')