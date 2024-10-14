_DATASETS = {
    'GRS': {
        'url': 'https://rutgers.box.com/shared/static/3u8cokpvnbpl8k7uuka7qtz1atj9pxu5',
        'fname': '2022_Mars_Odyssey_GRS_Element_Concentration_Maps.zip',
        'dirpath': 'GRS/',
        'hash' : {
            'sha256': 'ba2b5cc62b18302b1da0c111101d0d2318e69421877c4f9c145116b41502777b',
        },
    },
    'dichotomy_coords': {
        'url': 'https://rutgers.box.com/shared/static/tekd1w26h9mvfnyw8bpy4ko4v48931ri',
        'fname': 'dichotomy_coordinates-JAH-0-360.txt',
        'dirpath': 'Crust/dichotomy/',
        'hash': {
            'sha256': '42f2b9f32c9e9100ef4a9977171a54654c3bf25602555945405a93ca45ac6bb2',
        }
    },
}


def peek_datasets():
    """
    Returns a dictionary of all available datasets -- intended for debugging/exploration purposes, should NOT be called in production code.
    """
    return _DATASETS


def _get_download_info(name: str) -> dict[str, dict[str, str | dict[str, str]]]:
    """
    Returns information to download a dataset as a dictionary with keys 'url', 'fname', 'dirpath' (relative to data cache directory), and 'hash'.
    """
    try:
        info = _DATASETS[name]
        return info
    except KeyError:
        error_msg = [
            f"Dataset not found: '{name}'. Options are: {', '.join(_DATASETS.keys())}",
            f"To see all information about the datasets, run `from redplanet.DatasetManager.dataset_info import _DATASETS; print(_DATASETS)`.",
        ]
        raise ValueError('\n'.join(error_msg))