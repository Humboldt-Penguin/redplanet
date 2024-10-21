import hashlib
from pathlib import Path
from collections.abc import Callable
import requests

import xxhash



_hashalgs: dict[str, Callable] = {
    'xxh3_64': xxhash.xxh3_64,
    'md5'    : hashlib.md5,
    'sha1'   : hashlib.sha1,
    'sha256' : hashlib.sha256,
}
## Note: There's no significant difference between algorithms for time it takes to hash small files (for <1MB, it's on the order of thousandths of a second) -- but it DOES matter for large files (e.g. a 5GB file, sha256 takes 13 seconds, while xxh3 takes 2 seconds).


def get_available_algorithms() -> list[str]:
    """
    Get a list of supported hashing algorithms.
    """
    return list(_hashalgs.keys())



def _calculate_hash_from_file(fpath: Path, alg: str) -> str:
    """
    Calculate the hash of a file using the specified algorithm.

    Args:
        fpath: Path
            Path to the file.
        alg: str
            Hashing algorithm to use (for options, call `from redplanet.DatasetManager.hash import get_available_algorithms(); print(get_available_algorithms())`).

    Returns:
        str: The hexadecimal hash of the file.
    """

    ## Input validation
    fpath = fpath.resolve()
    if not fpath.is_file():
        raise FileNotFoundError(f"File not found: {fpath}")
    if alg not in _hashalgs:
        raise ValueError(f"Unsupported algorithm: '{alg}'. Options are: {', '.join(get_available_algorithms())}")

    ## Calculate hash
    hash_obj = _hashalgs[alg]()

    with fpath.open('rb') as f:
        CHUNK_SIZE = 2**13    # 2^13=8192 bytes per chunk
        while chunk := f.read(CHUNK_SIZE):
            hash_obj.update(chunk)

    return hash_obj.hexdigest()



def _calculate_hash_from_url(url: str, alg: str) -> str:
    """
    Calculate the hash of a file on the internet given its download URL, without actually downloading it.
    This is intended for verifying the integrity of a file.

    Args:
        url: str
            URL of the file.
        alg: str
            Hashing algorithm to use (for options, call `from redplanet.DatasetManager.hash import get_available_algorithms(); print(get_available_algorithms())`).

    Returns:
        str: The hexadecimal hash of the file.
    """

    ## Input validation
    if alg not in _hashalgs:
        raise ValueError(f"Unsupported algorithm: '{alg}'. Options are: {', '.join(get_available_algorithms())}")

    hash_obj = _hashalgs[alg]()

    ## Make the request with streaming enabled to avoid loading the whole file in memory
    response = requests.get(url, stream=True)

    ## Check if the request was successful
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch the file from URL: {url}. Status code: {response.status_code}")

    ## Read the content in chunks and update the hash object
    CHUNK_SIZE = 2**13  # 8192 bytes per chunk
    for chunk in response.iter_content(CHUNK_SIZE):
        if chunk:  # filter out keep-alive new chunks
            hash_obj.update(chunk)

    return hash_obj.hexdigest()
