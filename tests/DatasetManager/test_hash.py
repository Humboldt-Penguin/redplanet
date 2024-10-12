import tempfile
from pathlib import Path
from hashlib import sha256

import pytest
import xxhash

from redplanet.DatasetManager.hash import (
    _hashalgs,
    _calculate_hash_from_file,
    _calculate_hash_from_url,
)





## `_hashalgs` (private variable) -- representing available hash algorithms
class Test__hashalgs:

    ## Verify types/attrs of keys/values
    def test__hashalgs__types(self):
        assert isinstance(_hashalgs, dict)
        for alg, hash_obj in _hashalgs.items():
            assert isinstance(alg, str)
            assert hasattr(hash_obj(), 'update')
            assert hasattr(hash_obj(), 'hexdigest')





## `_calculate_hash_from_file` (internal function) -- calculate file hash with specified algorithm
class Test__calculate_hash_from_file:

    ## Valid input
    def test__calculate_hash_from_file__valid(self, tmp_path):
        # create temp file to hash
        temp_file_path = tmp_path / "testfile"
        temp_file_path.write_bytes(b'Test content for hashing')

        expected_sha256 = sha256(b'Test content for hashing').hexdigest()
        expected_xxh3_64 = xxhash.xxh3_64(b'Test content for hashing').hexdigest()

        assert _calculate_hash_from_file(fpath=temp_file_path, alg='sha256') == expected_sha256
        assert _calculate_hash_from_file(fpath=temp_file_path, alg='xxh3_64') == expected_xxh3_64


    ## Invalid input: `fpath` does not exist
    def test__calculate_hash_from_file__invalid_file(self):
        non_existent_file = Path('present_day___present_time___hahahahaha.txt')

        with pytest.raises(FileNotFoundError):
            _calculate_hash_from_file(fpath=non_existent_file, alg='sha256')


    ## Invalid input: `alg` not available
    def test__calculate_hash_from_file__invalid_alg(self, tmp_path):
        # create temp file to hash
        temp_file_path = tmp_path / "testfile"
        temp_file_path.write_bytes(b'Test content for hashing')

        with pytest.raises(ValueError, match="Unsupported algorithm"):
            _calculate_hash_from_file(fpath=temp_file_path, alg='nonexistent_algorithm')





## `_calculate_hash_from_url` (internal function) -- calculate hash from URL without downloading it, with specified algorithm
class Test__calculate_hash_from_url:

    ## Valid input
    def test__calculate_hash_from_url__valid(self):
        known_url = 'https://www.w3.org/2001/06/utf-8-test/UTF-8-demo.html'
        known_sha256 = 'c19249281275b6c8e3e7ba90edbfbde1998c47f4a3e8171c9a9ed46458495e75'
        known_xxh3_64 = '22072ea3f116681d'

        assert _calculate_hash_from_url(url=known_url, alg='sha256') == known_sha256
        assert _calculate_hash_from_url(url=known_url, alg='xxh3_64') == known_xxh3_64


    ## Invalid input: `url` is invalid
    def test__calculate_hash_from_url__invalid_url(self):
        with pytest.raises(ValueError, match="Invalid URL"):
            _calculate_hash_from_url(url='invalid_url', alg='sha256')


    ## Invalid input: `alg` not available
    def test__calculate_hash_from_url__invalid_alg(self):
        with pytest.raises(ValueError, match="Unsupported algorithm"):
            _calculate_hash_from_url(url='https://www.google.com', alg='nonexistent_algorithm')
