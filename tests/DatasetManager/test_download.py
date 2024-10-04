import hashlib
from pathlib import Path
import requests

import pytest

from redplanet.DatasetManager.download import _download_file_from_url





## `_download_file_from_url` (internal function) -- download file from URL to local path
class Test__download_file_from_url:

    ## Valid input
    def test__download_file_from_url(self, tmp_path):
        known_url = 'https://www.w3.org/2001/06/utf-8-test/UTF-8-demo.html'
        known_sha256 = 'c19249281275b6c8e3e7ba90edbfbde1998c47f4a3e8171c9a9ed46458495e75'

        # Use tmp_path to create a temporary file path
        fpath = tmp_path / 'tempfile.html'

        _download_file_from_url(known_url, fpath)
        assert fpath.exists(), "The file was not downloaded. This may be due to a bad network connection."

        sha256_hash = hashlib.sha256()
        with open(fpath, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b''):
                sha256_hash.update(byte_block)
        computed_hash = sha256_hash.hexdigest()

        assert computed_hash == known_sha256, f"Hash mismatch: {computed_hash} != {known_sha256}"


    ## Invalid input: `url` is invalid
    def test__download_file_from_url_invalid_url(self, tmp_path):
        invalid_url = 'http://this.url.does.not.exist/invalid.html'

        fpath = tmp_path / 'tempfile.html'

        with pytest.raises(requests.exceptions.RequestException):
            _download_file_from_url(invalid_url, fpath)
