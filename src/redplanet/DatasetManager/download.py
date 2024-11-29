from pathlib import Path
import requests
from requests.exceptions import RequestException
from time import sleep

def _download_file_from_url(
    url       : str,
    dest_path : Path,
    retries   : int = 3,
    timeout   : int = 10,
    chunk_size: int = 512 * 1024,  # 512KB
) -> None:
    """
    Download a file from a URL to a specified local path.

    Parameters
    ----------
    url : str
        The URL of the file to download.
    dest_path : Path
        The local file path where the downloaded file will be saved.
    retries : int, optional
        The number of times to retry the download in case of failures.
    timeout : int, optional
        The timeout in seconds for the download request.
    chunk_size : int, optional
        The size of each chunk to read from the response.

    Raises
    ------
    RequestException
        If the download fails after the specified number of retries.
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    attempt = 0
    while attempt < retries:
        try:
            with requests.get(url, stream=True, timeout=timeout) as response:
                response.raise_for_status()
                with open(dest_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:  # Filter out keep-alive new chunks
                            f.write(chunk)
                break  # Exit the retry loop if download succeeds
        except RequestException as e:
            attempt += 1
            if attempt == retries:
                raise e  # Re-raise the exception if max retries exceeded
            sleep(1)  # Wait before retrying
