from pathlib import Path

import pandas as pd


_DATASETS = {
    # 'GRS': {
    #     'url'    : 'https://rutgers.box.com/shared/static/3u8cokpvnbpl8k7uuka7qtz1atj9pxu5',
    #     'fname'  : '2022_Mars_Odyssey_GRS_Element_Concentration_Maps.zip',
    #     'dirpath': 'GRS/',
    #     'hash'   : {
    #         'sha256': 'ba2b5cc62b18302b1da0c111101d0d2318e69421877c4f9c145116b41502777b',
    #     },
    # },
    'GRS_v2': {  # TODO: rename this to 'GRS' at some point
        'url'    : 'https://data.mendeley.com/public-files/datasets/3jd9whd78m/files/a0c6ddc8-fbca-4119-b6f5-533a5775b719/file_downloaded',
        # 'url'    : 'https://rutgers.box.com/shared/static/qxfzuv7ka5c57k5awj83ueknr27dmyi4', # alt mirror on my own box account
        'fname'  : 'Rani2022_new_GRS_data.xlsx',
        'dirpath': 'GRS/',
        'hash'   : {
            'sha256': '06f7b8cfc89a803c714a7dd69beba0d65ba9f26ccf8eb5ddc276e280c4e5b917',
        },
        'size_mib': 0.4064617156982422,
    },
    'dichotomy_coords': {
        'url'    : 'https://rutgers.box.com/shared/static/tekd1w26h9mvfnyw8bpy4ko4v48931ri',
        'fname'  : 'dichotomy_coordinates-JAH-0-360.txt',
        'dirpath': 'Crust/dichotomy/',
        'hash'   : {
            'sha256': '42f2b9f32c9e9100ef4a9977171a54654c3bf25602555945405a93ca45ac6bb2',
        },
        'size_mib': 0.04616832733154297,
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
        'size_mib': 10856.2561378479,
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
        'size_mib': 2025.1318378448486,
    },
    'SH_5km': {
        'url'    : 'https://rutgers.box.com/shared/static/ff1tmj9ovgqugl524az8zt920nwktlh7',
        'fname'  : 'Mars_MOLA_topography_5km.memmap',
        'dirpath': 'Crust/topo/',
        'hash'   : {
            'xxh3_64': 'c342253082d163dd',
        },
        'size_mib': 69.51227760314941,
    },
    'SH_10km': {
        'url'    : 'https://rutgers.box.com/shared/static/mt2aysgkf4s8vqrdo77fjzsnuz1fmapw',
        'fname'  : 'Mars_MOLA_topography_10km.memmap',
        'dirpath': 'Crust/topo/',
        'hash'   : {
            'xxh3_64': '3a8d69acce1a0799',
        },
        'size_mib': 17.38417625427246,
    },
    'moho_registry': {
        'url'    : 'https://rutgers.box.com/shared/static/dcyysy7k1jbhkzt20hgkyt9qxvij79wn',
        'fname'  : 'moho_registry.csv',
        'dirpath': 'Crust/moho/',
        'hash'   : {
            'sha256': '0be4a1ff14df2ee552034487e91ae358dd2e8a907bc37123bbfa5235d1f98dba',
        },
        'size_mib': 2.0612106323242188,
    },
    'crater_db': {
        'url'    : 'https://rutgers.box.com/shared/static/imou5t0f2inyvx8ldcxfk234oeit7z3q',
        'fname'  : 'craters_with_names_and_ages_50km.csv',
        'dirpath': 'Craters/',
        'hash'   : {
            'xxh3_64': 'ea14d77f25f090c4',
            'md5'    : '4e63fd2a7f1367d131ee606edcdfb5f7',
            'sha1'   : '79113d236836e1d8bb53e517ab3cfc4afad2cac2',
            'sha256' : 'e48808ef670e39e812149e4731634d59964b7b3465b1be38eda920f890125bdc',
        },
        'size_mib': 0.2772712707519531,
    },
    'Langlais2019': {
        'url'    : 'https://zenodo.org/records/3876714/files/Langlais2019.sh.gz?download=1',
        'fname'  : 'Langlais2019.sh.gz',
        'dirpath': 'Mag/sh/',
        'hash'   : {
            'md5'    : '39245feef66555366108aecb6d5c0f67',
            'sha256' : '3cad9e268f0673be1702f1df504a4cbcb8dba4480c7b3f629921911488fe247b',
        },
        'size_mib': 0.08092212677001953,
    },
    'Genova2016': {
        ## directly downloaded from here (also see associated lbl file): https://pds-geosciences.wustl.edu/mro/mro-m-rss-5-sdp-v1/mrors_1xxx/data/rsdmap/
        'url'    : 'https://rutgers.box.com/shared/static/cw5ijchyxi021iwmj6qyw2i07hyt24wq',
        'fname'  : 'ggmro_120_bouguer_90.img',
        'dirpath': 'Crust/boug/',
        'hash'   : {
            'md5'    : '95423874e702b8a55f3a4b17b3ef744a',
            'sha256' : 'd3657c9bd80bf5e452ad0d0216078e9295065b5d1e0a04d0fab7bf22e3b50438',
        },
        'size_mib': 126.5625,
    },
    'MOLA_shape_719': {
        'url'    : 'https://zenodo.org/records/10820719/files/Mars_MOLA_shape_719.bshc.gz?download=1',
        'fname'  : 'Mars_MOLA_shape_719.bshc.gz',
        'dirpath': 'Crust/moho/shape/',
        'hash'   : {
            'md5'    : '77c213978e7403c722e38b78e0202d7c',
        },
        'size_mib': 3.7924137115478516,
    },
    'Gong & Weiczorek, 2021': {
        'url'    : 'https://zenodo.org/records/4686358/files/MarsMagnetizationDepth.zip?download=1',
        'fname'  : 'MarsMagnetizationDepth.zip',
        'dirpath': 'Mag/depth/',
        'hash'   : {
            'md5'    : '16780170ee3e0dccaaf719fc201e4281',
        },
        'size_mib': 0.03770160675048828,
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
        interior_model, insight_thickness, rho_south, rho_north = model_name.split('-')
        raise MohoDatasetNotFoundError(
            f'Moho model not found for the given parameters: {interior_model=}, {insight_thickness=}, {rho_south=}, {rho_north=}\n'
            f'To see available models: `redplanet.Crust.moho.get_registry()`'
        )

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
