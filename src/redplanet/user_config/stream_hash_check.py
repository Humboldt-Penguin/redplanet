"""
PURPOSE: Verify that downloaded data files are as expected (i.e. the author isn't distributing malicious/altered files).
"""


_enable_stream_hash_check: bool = False
## TODO: before publishing, initialize this to True -- keeping it false rn for debugging/dev purposes


def get_enable_stream_hash_check() -> bool:
    """
    Get the current value of the flag that determines whether we verify the hash of a file at URL by streaming before fully downloading it.

    Returns
    -------
    bool
    """
    return _enable_stream_hash_check


def set_enable_stream_hash_check(value: bool) -> None:
    """
    Set the flag that determines whether we verify the hash of a file at URL by streaming before fully downloading it.

    Parameters
    ----------
    value : bool
    """
    global _enable_stream_hash_check
    _enable_stream_hash_check = value
    return
