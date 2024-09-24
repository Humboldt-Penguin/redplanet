import hashlib
from pathlib import Path
from platformdirs import user_cache_dir

import pytest

from redplanet.DatasetManager.download import _download_file_from_url


## `_download_file_from_url` (internal function) -- download file from URL to local path
def test__download_file_from_url():
    """
    Test the _download_file_from_url function by downloading a known file and verifying its SHA256 hash.
    """

    known_url = 'https://www.w3.org/2001/06/utf-8-test/UTF-8-demo.html'
    known_sha256 = 'c19249281275b6c8e3e7ba90edbfbde1998c47f4a3e8171c9a9ed46458495e75'

    fpath = Path(user_cache_dir(appname="redplanet")).resolve() / 'tempfile__delete_this_if_you_see_it.html'
    fpath.parent.mkdir(parents=True, exist_ok=True)

    ## delete tempfile if it already exists
    if fpath.exists():
        fpath.unlink()

    try:
        _download_file_from_url(known_url, fpath)
        assert fpath.exists(), "The file was not downloaded."

        sha256_hash = hashlib.sha256()
        with open(fpath, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b''):
                sha256_hash.update(byte_block)
        computed_hash = sha256_hash.hexdigest()

        assert computed_hash == known_sha256, f"Hash mismatch: {computed_hash} != {known_sha256}"

    finally:
        ## delete the file when the test is done
        if fpath.exists():
            fpath.unlink()
