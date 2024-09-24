import hashlib
from pathlib import Path
from typing import List
import requests

import xxhash



_hashalgs = {
    'xxh3_64': xxhash.xxh3_64,
    'sha256': hashlib.sha256,
}
## Note: There's no significant difference for small files (for <1MB, it's on the order of thousandths of a second) -- but it matters for large files (e.g. a 5GB file, sha256 takes 13 seconds, while xxh3 takes 2 seconds).


def get_hashalgs() -> List[str]:
    """
    Get the list of supported hashing algorithms.

    Returns:
        List[str]: List of supported hashing algorithms.
    """
    return list(_hashalgs.keys())



def calculate_hash_from_file(fpath: Path, alg: str) -> str:
    """
    Calculate the hash of a file using the specified algorithm.

    Args:
        fpath: Path
            Path to the file.
        alg: str
            Hashing algorithm to use (for options, call `from redplanet.DatasetManager.hash import get_hashalgs(); print(get_hashalgs())`).

    Returns:
        str: The hexadecimal hash of the file.
    """

    ## Input validation
    if not fpath.is_file():
        raise FileNotFoundError(f"File not found: {fpath}")
    if alg not in _hashalgs:
        raise ValueError(f"Unsupported algorithm: '{alg}'. Options are: {', '.join(get_hashalgs())}")

    ## Calculate hash
    hash_obj = _hashalgs[alg]()

    with fpath.open('rb') as f:
        CHUNK_SIZE = 2**13    # 2^13=8192 bytes per chunk
        while chunk := f.read(CHUNK_SIZE):
            hash_obj.update(chunk)

    return hash_obj.hexdigest()



def calculate_hash_from_url(url: str, alg: str) -> str:
    """
    Calculate the hash of a file on the internet given its download URL, without actually downloading it.
    This is intended for verifying the integrity of a file.

    Args:
        url: str
            URL of the file.
        alg: str
            Hashing algorithm to use (for options, call `from redplanet.DatasetManager.hash import get_hashalgs(); print(get_hashalgs())`).

    Returns:
        str: The hexadecimal hash of the file.
    """

    ## Input validation
    if alg not in _hashalgs:
        raise ValueError(f"Unsupported algorithm: '{alg}'. Options are: {', '.join(get_hashalgs())}")

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
