from tqdm import tqdm

from redplanet import user_config

from redplanet.DatasetManager.main import _get_fpath_dataset
from redplanet.DatasetManager.dataset_info import _DATASETS


def prefetch() -> None:
    """
    Download a few key datasets to cache. This is primarily meant for the demo notebook.
    """

    print(f'Cache directory: {user_config.get_dirpath_datacache()}')

    ## declare which datasets to download (these correspond to keys in `redplanet.DatasetManager.dataset_info._DATASETS`)
    names = [
        'GRS_v2',
        'dichotomy_coords',
        # 'DEM_200m',
        # 'DEM_463m',
        # 'SH_5km',
        'SH_10km',
        'moho_registry',
        'crater_db',
        'Langlais2019',
        # 'Genova2016',
        'MOLA_shape_719',
        'Gong & Weiczorek, 2021',
    ]

    # ## DEBUG: delete all if they exist
    # for name in names:
    #     fpath = _get_fpath_dataset(name)
    #     if fpath.exists():
    #         fpath.unlink()

    ## calculate size of all datasets (not accounting for what's already downloaded)
    sum_size_mib = 0
    for name in names:
        sum_size_mib += _DATASETS[name]['size_mib']
    print(f'(Total download size: {sum_size_mib:.2f} MiB)')
    print()

    # ## download all (superseded by progress bar)
    # for name in names:
    #     print(f'Downloading: "{name}" ({_DATASETS[name]["size_mib"]:0.2f} MiB)')
    #     fpath = _get_fpath_dataset(name)

    ## download all, with progress bar
    with tqdm(total=len(names), desc="Downloading datasets") as pbar:
        for name in names:
            pbar.set_postfix(current=f'"{name}" ({_DATASETS[name]["size_mib"]:0.2f} MiB)')
            _get_fpath_dataset(name)
            pbar.update(1)
