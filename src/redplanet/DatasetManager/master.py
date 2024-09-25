from pathlib import Path
from urllib import request

from redplanet.user_config import get_dirpath_datacache
from redplanet.DatasetManager.dataset_info import get_download_info
from redplanet.DatasetManager.download import _download_file_from_url
from redplanet.DatasetManager.hash import (
    calculate_hash_from_file,
    calculate_hash_from_url,
    get_hashalgs
)



def _get_fpath_dataset(dataset_name: str) -> Path:
    """
    Get the file path of a dataset...
        1. The first time, we download it to a local cache folder (you can see the default location with `import redplanet; redplanet.get_dirpath_datacache()` or change with with `set_dirpath_datacache()`. Since downloading random files from the internet is risky (you're essentially trusting me with unrestricted access to your computer, not to mention a potential man-in-the-middle attack although unlikely) we take the following two safety measures:
            i. Before downloading, we verify the integrity of the file at the URL by calculating its hash "on the fly" (i.e. streaming it as opposed to fully downloading it) -- this ensures we don't download malicious/altered files, assuming you trust my intended file/hash.
            ii. After downloading, we again verify integrity of file on disk by calculating its hash, immediately deleting if it doesn't match. I can't think of any realistic case this would occur, but why not.
        2. Subsequent times, we see if a file with the correct name/hash already exists in the cache folder.

    Parameters:
    -----------
    dataset_name : str
        The name of the dataset to be retrieved.

    Returns:
    --------
    Path
        The file path to the cached or newly downloaded dataset.

    Raises:
    -------
    Exception
        If there is a hash mismatch for either the file already in cache or the streamed/downloaded file.
    """

    ## Get download info for dataset
    info: dict = get_download_info(dataset_name)
    fpath_dataset: Path = get_dirpath_datacache() / info['dirpath'] / info['fname']


    ## Out of hashes listed in metadata, pick the fastest (assuming `get_hashalgs()` lists them from fastest to slowest)
    known_hash_value = None
    for hashalg in get_hashalgs():
        known_hash_alg = hashalg
        known_hash_value = info['hash'].get(known_hash_alg)
        if known_hash_value is not None:
            break
    if (known_hash_value is None):
        raise ValueError(f"[Internal/unexpected error] Hash value not found for dataset '{dataset_name}'. Pester the developer.")


    ## Case 1: File not found in cache, download it.
    if (not fpath_dataset.is_file()):

        ## First, verify the integrity of the file at the URL by calculating its hash "on the fly" (i.e. streaming it as opposed to fully downloading it) -- this ensures we don't download malicious/altered files, assuming you trust my intended file/hash
        calculated_hash_value_fromStream = calculate_hash_from_url(info['url'], known_hash_alg)
        if (calculated_hash_value_fromStream != known_hash_value):
            error_msg = [
                f"We need to download the dataset from the known URL [1], but the calculated hash of the file at that URL [2] doesn't match the known hash [3]:",
                f"    > [1] Known URL: \t{info['url']}",
                f"    > [2] Calculated hash: \t{known_hash_alg}-{calculated_hash_value_fromStream}",
                f"    > [3] Known hash: \t{known_hash_alg}-{known_hash_value}",
                f"To see all known information about the datasets, run `import redplanet; from pprint import pprint; pprint(redplanet.peek_datasets())`.",
                f"=> DOWNLOAD ABORTED.",
            ]
            raise Exception('\n'.join(error_msg))

        ## Second, proceed to download the file to `fpath_dataset`
        _download_file_from_url(info['url'], fpath_dataset)

        ## (Optional) Third, just to be sure, verify integrity of the recently-downloaded file by calculating the hash. I can't think of any realistic case this would fail, but why not.
        calculated_hash_value = calculate_hash_from_file(fpath_dataset, known_hash_alg)
        if (calculated_hash_value != known_hash_value):
            fpath_dataset.unlink()  # Deletes the recently-downloaded file for safety
            error_msg = [
                f"We already verified the integrity of the file at the URL [1] from its hash [2] -- however, after downloading it to disk [3] and recalculating the hash for safety [4], it doesn't match the known hash [5] for some unknown reason:",
                f"    > [1] Known URL: \t{info['url']}",
                f"    > [2] Calculated hash at URL: \t{known_hash_alg}-{calculated_hash_value_fromStream}",
                f"    > [3] File path (now deleted): \t{fpath_dataset}",
                f"    > [4] Calculated hash: \t{known_hash_alg}-{calculated_hash_value}",
                f"    > [5] Known hash: \t{known_hash_alg}-{known_hash_value}",
                f"**The downloaded file has been deleted for safety.**",
                f"To see all known information about the datasets, run `import redplanet; from pprint import pprint; pprint(redplanet.peek_datasets())`.",
                f"=> PROCESS ABORTED.",
            ]
            raise Exception('\n'.join(error_msg))


    # Case 2: File already exists in cache, verify the hash
    else:

        ## Error case: calculated hash of file on disk does not match the known hash.
        calculated_hash_value = calculate_hash_from_file(fpath_dataset, known_hash_alg)
        if (calculated_hash_value != known_hash_value):
            error_msg = [
                f"Dataset already exists in cache folder [1], but the calculated hash [2] doesn't match the known hash [3]:",
                f"    > [1] File path: \t{fpath_dataset}",
                f"    > [2] Calculated hash: \t{known_hash_alg}-{calculated_hash_value}",
                f"    > [3] Known hash: \t{known_hash_alg}-{known_hash_value}",
                f"This may occur because a user/process manually changed the dataset file, or the dataset was updated in `redplanet`. We suggest you delete or move the old dataset file and try again.",
                f"To see all known information about the datasets, run `import redplanet; from pprint import pprint; pprint(redplanet.peek_datasets())`.",
                f"=> PROCESS ABORTED.",
            ]
            raise Exception('\n'.join(error_msg))




    return fpath_dataset
