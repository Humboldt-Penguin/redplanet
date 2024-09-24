from typing import Dict

_DATASETS = {
    'GRS': {
        'url': 'https://rutgers.box.com/shared/static/i1dy31or67y030yhof3c39ts19emigzd',
        'fname': '2022_Mars_Odyssey_GRS_Element_Concentration_Maps.zip',
        'dirpath': 'GRS/',
        'hash' : {
            'sha256': '45e047a645ae8d1bbd8e43062adab16a22786786ecb17d8e44bfc95f471ff9b7',
        },
        # 'post-processing': 'unzip', ## I've opted to unzip the file in memory rather than creating a separate directory, since that makes my hash verification incomplete since you could alter the text files without altering the zip file.
    },
    # 'Crust/topo': {},
    # 'Crust/dichotomy': {},
}


def peek_datasets():
    """
    Returns a dictionary of all available datasets -- intended for debugging/exploration purposes, should NOT be called in production code.
    """
    return _DATASETS


def _get_download_info(name: str) -> Dict[str, Dict[str, str | Dict[str, str]]]:
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