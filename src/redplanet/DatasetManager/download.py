import shutil
import time
from urllib.error import URLError, HTTPError

def download_file_from_url(
    url: str,
    dest_path: Path,
    retries: int = 3,
    timeout: int = 10,
    chunk_size: int = 2**13,
) -> None:
    """
    Downloads a file from a URL and saves it to the destination path.

    Parameters:
    -----------
    url : str
        The URL from which to download the file.
    dest_path : Path
        The destination path where the file will be saved.
    retries : int
        The number of times to retry the download in case of failure (default 3).
    timeout : int
        The timeout (in seconds) for the request (default 10 seconds).
    chunk_size : int
        The size (in bytes) of each chunk to be written to disk (default 2**13 = 8192 bytes).

    Returns:
    --------
    None

    Raises:
    -------
    Exception
        If the download fails after the specified number of retries.
    """

    # Ensure the destination directory exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    attempt = 0
    while attempt < retries:
        try:
            with request.urlopen(url, timeout=timeout) as response:
                # Use shutil.copyfileobj to efficiently copy the stream in chunks
                with open(dest_path, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file, chunk_size)
            break  # Exit loop if download is successful

        except (URLError, HTTPError) as e:
            attempt += 1
            if attempt >= retries:
                raise Exception(f"Download failed after {retries} attempts. Error: {e}")
            else:
                # print(f"Download failed, retrying {attempt}/{retries}... Error: {e}")
                time.sleep(2)  # Backoff before retrying
