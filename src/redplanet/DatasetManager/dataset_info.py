from pathlib import Path

import pandas as pd


_DATASETS = {
    'GRS': {
        'url'    : 'https://rutgers.box.com/shared/static/3u8cokpvnbpl8k7uuka7qtz1atj9pxu5',
        'fname'  : '2022_Mars_Odyssey_GRS_Element_Concentration_Maps.zip',
        'dirpath': 'GRS/',
        'hash'   : {
            'sha256': 'ba2b5cc62b18302b1da0c111101d0d2318e69421877c4f9c145116b41502777b',
        },
    },
    'dichotomy_coords': {
        'url'    : 'https://rutgers.box.com/shared/static/tekd1w26h9mvfnyw8bpy4ko4v48931ri',
        'fname'  : 'dichotomy_coordinates-JAH-0-360.txt',
        'dirpath': 'Crust/dichotomy/',
        'hash'   : {
            'sha256': '42f2b9f32c9e9100ef4a9977171a54654c3bf25602555945405a93ca45ac6bb2',
        },
    },
    'DEM_200m': {
        'url'    : 'https://rutgers.box.com/shared/static/8xfyuf8qw6sbyqgzjjx0g2twehui9595',
        'fname'  : 'Mars_HRSC_MOLA_BlendDEM_Global_200mp_v2.memmap',
        'dirpath': 'Crust/topo/',
        'hash'   : {
            'xxh3_64': 'e8cc649a36ea4fab',
            'md5'    : '74cedd82aaf200b62ebb64affffe0e7e',
            'sha1'   : '0c7704155a3e9fb6bef284980fdb37aa559457c5',
            'sha256' : '691b6ce6a1cacc5fcea4b95ef1832fac50e421e1ec8f7fb33e5c791396aa4a4f',
        },
    },
    'DEM_463m': {
        'url'    : 'https://rutgers.box.com/shared/static/s2iu6egz4og7ht310ctebgrloinf81dq',
        'fname'  : 'Mars_MGS_MOLA_DEM_mosaic_global_463m.memmap',
        'dirpath': 'Crust/topo/',
        'hash'   : {
            'xxh3_64': '6eed1a19495d736f',
            'md5'    : '0f2378e55a01c217b2662b7ba07a3f27',
            'sha1'   : 'f3547e5423bd447179e5126e37b262e4136adcac',
            'sha256' : '7788fa9287c633456fbf2de8b0e674a7e375014d2b58731b45f991be284879c4',
        },
    },
    'moho_registry': {
        'url'    : 'https://rutgers.box.com/shared/static/dcyysy7k1jbhkzt20hgkyt9qxvij79wn',
        'fname'  : 'moho_registry.csv',
        'dirpath': 'Crust/moho/',
        'hash'   : {
            'sha256': '0be4a1ff14df2ee552034487e91ae358dd2e8a907bc37123bbfa5235d1f98dba',
        },
    },
}



def peek_datasets() -> dict:
    """
    Returns a dictionary of all available datasets -- intended for debugging/exploration purposes, should NOT be called in production code.
    """
    return _DATASETS


def _get_download_info(name: str) -> dict:
    """
    Returns information to download a dataset as a dictionary with keys 'url', 'fname', 'dirpath' (relative to data cache directory), and 'hash'.
    """
    info = _DATASETS.get(name)

    if info is None:
        error_msg = [
            f"Dataset not found: '{name}'. Options are: {', '.join(_DATASETS.keys())}",
            f"To see all information about the datasets, run `from redplanet.DatasetManager.dataset_info import _DATASETS; print(_DATASETS)`.",
        ]
        raise DatasetNotFoundError('\n'.join(error_msg))

    return info


def _get_download_info_moho(
    model_name: str,
    fpath_moho_registry: Path,
) -> dict:
    """
    Parameters:
        - `model_name`: str
            - Model name in the format 'MODEL-THICK-RHOS-RHON', e.g. 'Khan2022-38-2900-2900'.
        - `fpath_moho_registry`: Path
            - Path to the CSV file containing the registry of Moho models.
    """

    df = pd.read_csv(fpath_moho_registry)
    result = df[ df['model_name'] == model_name ]

    if result.empty:
        raise MohoDatasetNotFoundError(f"Moho model '{model_name}' not found in the registry.")

    box_download_code, sha1 = result.values.tolist()[0][1:]
    result = {
        'url'    : f'https://rutgers.box.com/shared/static/{box_download_code}',
        'fname'  : f'Moho-Mars-{model_name}.sh',
        'dirpath': 'Crust/moho/shcoeffs/',
        'hash'   : {
            'sha1': sha1,
        },
    }
    return result



class DatasetNotFoundError(Exception):
    pass

class MohoDatasetNotFoundError(Exception):
    pass
