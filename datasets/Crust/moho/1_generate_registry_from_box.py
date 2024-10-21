# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "box-sdk-gen[jwt]",
#     "pandas",
#     "tqdm",
# ]
# ///


from typing import List, Callable
from datetime import datetime
from pathlib import Path, PurePosixPath
import logging
from pprint import pp

from tqdm import tqdm
import pandas as pd

from box_sdk_gen import JWTConfig, BoxJWTAuth, BoxClient # box authentication
from box_sdk_gen import AddShareLinkToFileSharedLink, UpdateSharedLinkOnFileSharedLink, AddShareLinkToFileSharedLinkPermissionsField, UpdateSharedLinkOnFileSharedLinkPermissionsField # box link sharing (lol)



''' ######################################################################## '''
'''                                   MAIN                                   '''
''' ######################################################################## '''

def main():

    ''' ———————————————————————————— User inputs ——————————————————————————— '''

    root_folder_id : str = '270589643170'   # path: 'rubox:shared_permalinks/redplanet/redplanet_cache/' (https://rutgers.app.box.com/folder/270589643170)

    # fpath_jwt_config : Path = list((Path.cwd() / '.secret/').glob('*.json'))[0]
    fpath_jwt_config : Path = Path('.secret') / '1190807008_sblhtn5v_config.json'   # token from personal account:"iltcc", app:"redplanet_export_v4"



    ''' —————————————————————————————— Logging ————————————————————————————— '''

    log        : logging.Logger
    fpath_logs : Path
    log, fpath_logs = setup_logger()

    log.info(f'Logging to file: {fpath_logs}')



    ''' ———————————————————————————— Box Auth ———————————————————————————— '''

    client : BoxClient = authenticate_box(fpath_jwt_config)

    log.info('')
    log.info('Authenticated with Box API.')
    log.info('')
    log.info(f'[Root folder info:]')
    log.info(f"    - '{_get_folder_name(client, root_folder_id)}/' (id: {root_folder_id})")



    ''' ——————————————————————— Build Registry Part 1 —————————————————————— '''

    # func_exclude_str = "lambda path: path.name == 'shcoeffs'"

    # log.info('')
    # log.info(f'[Exclude function:]')
    # log.info(f'    - `{func_exclude_str}`')
    log.info('')
    log.info(f'...traversing...')

    registry_noshcoeffs : dict = add_fileinfo_to_registry(
        client,
        root_folder_id,
        # func_exclude = eval(func_exclude_str)
    )

    log.info('')
    log.info(f'[Built registry with # files:]')
    log.info(f'    - {len(registry_noshcoeffs)}')



    ''' ——————————————————————— Build Registry Part 2 —————————————————————— '''

    registry_noshcoeffs_dlurls, dict_fileshare_statuses = add_filedlurls_to_registry(client, registry_noshcoeffs, log)

    log.info('')
    log.info('')
    log.info('')
    log.info(f'[SUMMARY:]')
    log.info(f'    - Added share link: {dict_fileshare_statuses['num_added_share']}')
    log.info(f'    - Fixed share link: {dict_fileshare_statuses['num_fixed_share']}')
    log.info(f'    - Already shared:   {dict_fileshare_statuses['num_already_shared']}')



    ''' —————————————————————————————— Export —————————————————————————————— '''

    fpath_output = export_registry_to_csv(registry_noshcoeffs_dlurls)

    log.info('')
    log.info('')
    log.info(f'[EXPORTED REGISTRY TO CSV:]')
    log.info(f'    - {fpath_output = }')





''' ######################################################################## '''
'''                             HELPER FUNCTIONS                             '''
''' ######################################################################## '''


''' ———————————————————————————————— Logging ——————————————————————————————— '''

def _create_console_handler(
    min_level : int = logging.INFO,
    fmt       : str = '[%(asctime)s, %(levelname)s]\t%(message)s',
    datefmt   : str = '%I:%M:%S %p',
    # datefmt   : str = '%H:%M:%S',
) -> logging.Handler:

    console_handler = logging.StreamHandler()
    formatter       = logging.Formatter(fmt, datefmt)

    console_handler.setLevel(min_level)
    console_handler.setFormatter(formatter)

    return console_handler


def _create_file_handler(
    logfile   : str,
    min_level : int = logging.DEBUG,
    # fmt       : str = '[%(asctime)s, %(levelname)s]    %(message)s',
    fmt       : str = '[%(asctime)s, %(levelname)s] %(message)s',
    datefmt   : str = '%Y/%m/%d %I:%M:%S %p',
    # datefmt   : str = '%Y/%m/%d %H:%M:%S',
) -> logging.Handler:

    file_handler = logging.FileHandler(logfile)
    formatter    = logging.Formatter(fmt, datefmt)

    file_handler.setLevel(min_level)
    file_handler.setFormatter(formatter)

    return file_handler


def setup_logger(
    fpath_logs  : Path = None,
    logger_name : str  = 'user_logger'
) -> List:

    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)

    if fpath_logs is None:
        dirpath_output = Path.cwd() / '.logs'
        dirpath_output.mkdir(exist_ok=True)
        fpath_logs = dirpath_output / f"redplanet_registry_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.log"

    file_handler    : logging.Handler = _create_file_handler(fpath_logs)
    console_handler : logging.Handler = _create_console_handler()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Prevent the logger from propagating messages to the root logger
    logger.propagate = False


    return [logger, fpath_logs]


''' ——————————————————————————————— Box Auth ——————————————————————————————— '''

def authenticate_box(fpath_jwt_config : Path) -> BoxClient:
    jwt_config : JWTConfig  = JWTConfig.from_config_file(config_file_path=fpath_jwt_config)
    auth       : BoxJWTAuth = BoxJWTAuth(config=jwt_config)
    user_auth  : BoxJWTAuth = auth.with_user_subject(user_id="34633045408")   # impersonating user from account:"iliketochacha" ("Kasane Teto")
    client     : BoxClient  = BoxClient(auth=user_auth)
    return client


''' ————————————————————————— Box Folder Accessors ————————————————————————— '''

def _get_folder_dict(
    client             : BoxClient,
    folder_id          : str,
    entries_per_search : int = 100,
    offset             : int = 0,
) -> dict:
    """
    RETURN:
        `dict`, which looks like this:
            {'id': '270589643170',
            'etag': '1',
            'type': 'folder',
            'sequence_id': '1',
            'name': 'redplanet_cache',
            'created_at': '2024-06-18T00:30:18-07:00',
            'modified_at': '2024-06-22T23:58:19-07:00',
            'description': '',
            'size': 11322836466,
            'path_collection': {'total_count': 2,
                                'entries': [{'id': '0',
                                            'type': 'folder',
                                            'name': 'All Files'},
                                            {'id': '270582896601',
                                            'etag': '1',
                                            'type': 'folder',
                                            'sequence_id': '1',
                                            'name': 'redplanet'}]},
            'created_by': {'id': '18595935892',
                            'type': 'user',
                            'name': 'Zain Kamal',
                            'login': 'zk117@rutgers.edu'},
            'modified_by': {'id': '18595935892',
                            'type': 'user',
                            'name': 'Zain Kamal',
                            'login': 'zk117@rutgers.edu'},
            'content_created_at': '2024-06-18T00:30:18-07:00',
            'content_modified_at': '2024-06-22T23:58:19-07:00',
            'owned_by': {'id': '18595935892',
                        'type': 'user',
                        'name': 'Zain Kamal',
                        'login': 'zk117@rutgers.edu'},
            'parent': {'id': '270582896601',
                        'etag': '1',
                        'type': 'folder',
                        'sequence_id': '1',
                        'name': 'redplanet'},
            'item_status': 'active',
            'item_collection': {'limit': 100,
                                'total_count': 3,
                                'offset': 0,
                                'order': [{'by': 'type', 'direction': 'ASC'},
                                        {'by': 'name', 'direction': 'ASC'}],
                                'entries': [{'id': '271456434555',
                                            'etag': '0',
                                            'type': 'folder',
                                            'sequence_id': '0',
                                            'name': 'Crust'},
                                            {'id': '271455606507',
                                            'etag': '0',
                                            'type': 'folder',
                                            'sequence_id': '0',
                                            'name': 'GRS'},
                                            {'id': '271457846138',
                                            'etag': '0',
                                            'type': 'folder',
                                            'sequence_id': '0',
                                            'name': 'Mag'}]}}

    """
    folder_dict : dict = client.folders.get_folder_by_id(
        folder_id = folder_id,
        limit     = entries_per_search,
        offset    = offset,
    ).to_dict()
    return folder_dict


def _get_folder_name(client: BoxClient, folder_id: str) -> str:
    empty_folder_dict : dict = _get_folder_dict(
        client             = client,
        folder_id          = folder_id,
        entries_per_search = 0,
    )
    folder_name : str = empty_folder_dict['name']
    return folder_name


def _get_folder_entries(client: BoxClient, folder_id: str) -> List[dict]:
    """
    We can't just call `get_folder_dict(...)` and then access `['item_collection']['entries']`, since the API call only returns up to 1,000 entries at a time. Therefore we need to repeatedly access the folder while incrementing the `offset` argument.

    RETURN:
        `List[dict]`, where FOLDERS look like:
            {
                'id'         : '271456434555',
                'etag'       : '0',
                'type'       : 'folder',
                'sequence_id': '0',
                'name'       : 'Crust'
            }
        and FILES look like:
            {
                'id'          : '1568917463274',
                'etag'        : '1',
                'type'        : 'file',
                'sequence_id' : '1',
                'name'        : '._Moho-Mars-Khan2022-18-2550-2550.sh',
                'sha1'        : '1abc429954206064f4ceed2886e22e1ffb65703a',
                'file_version': {
                    'id'  : '1724084185674',
                    'type': 'file_version',
                    'sha1': '1abc429954206064f4ceed2886e22e1ffb65703a'
                },
            }

    """

    empty_folder_dict : dict = _get_folder_dict(
        client             = client,
        folder_id          = folder_id,
        entries_per_search = 0,
    )
    num_entries        : int        = empty_folder_dict['item_collection']['total_count']

    entries            : List[dict] = []
    entries_per_search : int        = 1_000

    for offset in range(0, num_entries, entries_per_search):
        this_folder_dict : dict = _get_folder_dict(
            client             = client,
            folder_id          = folder_id,
            entries_per_search = entries_per_search,
            offset             = offset,
        )
        this_entries : List[dict] = this_folder_dict['item_collection']['entries']
        entries += this_entries

    return entries



''' —————————————————————————— Box File Accessors —————————————————————————— '''

def _get_file_dict(client: BoxClient, file_id: str) -> dict:
    """
    RETURN:
        `dict`, which looks like this:
            {'id': '1568919222016',
            'etag': '1',
            'type': 'file',
            'sequence_id': '1',
            'name': '2022_Mars_Odyssey_GRS_Element_Concentration_Maps.zip',
            'sha1': '5aa4778a4600c5fb85df1c6e363bd429e9c9e096',
            'file_version': {'id': '1724085982816',
                            'type': 'file_version',
                            'sha1': '5aa4778a4600c5fb85df1c6e363bd429e9c9e096'},
            'description': '',
            'size': 208819,
            'path_collection': {'total_count': 4,
                                'entries': [{'id': '0',
                                            'type': 'folder',
                                            'name': 'All Files'},
                                            {'id': '270582896601',
                                            'etag': '1',
                                            'type': 'folder',
                                            'sequence_id': '1',
                                            'name': 'redplanet'},
                                            {'id': '270589643170',
                                            'etag': '1',
                                            'type': 'folder',
                                            'sequence_id': '1',
                                            'name': 'redplanet_cache'},
                                            {'id': '271455606507',
                                            'etag': '0',
                                            'type': 'folder',
                                            'sequence_id': '0',
                                            'name': 'GRS'}]},
            'created_at': '2024-06-22T21:59:11-07:00',
            'modified_at': '2024-06-22T21:59:11-07:00',
            'content_created_at': '2024-03-08T02:44:12-08:00',
            'content_modified_at': '2024-03-08T02:44:12-08:00',
            'created_by': {'id': '18595935892',
                            'type': 'user',
                            'name': 'Zain Kamal',
                            'login': 'zk117@rutgers.edu'},
            'modified_by': {'id': '18595935892',
                            'type': 'user',
                            'name': 'Zain Kamal',
                            'login': 'zk117@rutgers.edu'},
            'owned_by': {'id': '18595935892',
                        'type': 'user',
                        'name': 'Zain Kamal',
                        'login': 'zk117@rutgers.edu'},
            'shared_link': {'url': 'https://rutgers.box.com/s/i1dy31or67y030yhof3c39ts19emigzd',
                            'effective_access': 'open',
                            'effective_permission': 'can_download',
                            'is_password_enabled': False,
                            'download_count': 0,
                            'preview_count': 0,
                            'download_url': 'https://rutgers.box.com/shared/static/i1dy31or67y030yhof3c39ts19emigzd.zip',
                            'access': 'open',
                            'permissions': {'can_download': True,
                                            'can_preview': True,
                                            'can_edit': False}},
            'parent': {'id': '271455606507',
                        'etag': '0',
                        'type': 'folder',
                        'sequence_id': '0',
                        'name': 'GRS'},
            'item_status': 'active'}

    """
    file_dict : dict = client.files.get_file_by_id(file_id=file_id).to_dict()
    return file_dict


def _get_file_name(client: BoxClient, file_id: str) -> str:
    file_dict : dict = _get_file_dict(client=client, file_id=file_id)
    file_name : str = file_dict['name']
    return file_name




''' ——————————————————————————— Box File Sharing ——————————————————————————— '''

def _get_file_sharestatus(client: BoxClient, file_id: str) -> str:
    """
    RETURNS:
        One of the following lists:
            ['not shared']
            ['incorrect sharing permissions', file_shareinfo_dict]
            ['correct sharing permissions',   file_shareinfo_dict, download_url]
    """
    file_dict : dict = _get_file_dict(client=client, file_id=file_id)

    file_shareinfo_dict : dict = file_dict.get('shared_link')
    """
    file_shareinfo_dict looks like this:
        {'url'                : 'https://rutgers.box.com/s/i1dy31or67y030yhof3c39ts19emigzd',
        'effective_access'    : 'open',
        'effective_permission': 'can_download',
        'is_password_enabled' : False,
        'download_count'      : 0,
        'preview_count'       : 0,
        'download_url'        : 'https://rutgers.box.com/shared/static/i1dy31or67y030yhof3c39ts19emigzd.zip',
        'access'              : 'open',
        'permissions'         : {'can_download': True,
                                 'can_preview' : True,
                                 'can_edit'    : False}}
    """


    ''' ———————————————————————— CASE 1: Not shared ———————————————————————— '''
    if file_shareinfo_dict is None:
        return ['not shared']


    ''' —————————————————— CASE 2: Bad sharing permissions ————————————————— '''
    proper_perms = {
        'effective_access'    : 'open',
        'effective_permission': 'can_download',
        'is_password_enabled' : False,
        'access'              : 'open',
        'permissions'         :
            {
                'can_download': True,
                'can_preview' : True,
                'can_edit'    : False
            }
    }   # NOTE: only paid accounts can change time-until-unshare (optional key "unshared_at"), so those are undetected and must be resolved manually.

    def _is_subset_dict(subset_dict, main_dict):
        return all(item in main_dict.items() for item in subset_dict.items())

    if not _is_subset_dict(proper_perms, file_shareinfo_dict):
        return ['incorrect sharing permissions', file_shareinfo_dict]


    ''' ————————————————— CASE 3: Good sharing permissions ————————————————— '''
    return ['correct sharing permissions', file_shareinfo_dict, file_shareinfo_dict['download_url']]


def _add_file_dlurl(client: BoxClient, file_id: str) -> str:
    file_dict : dict = client.shared_links_files.add_share_link_to_file(
        file_id = file_id,
        fields = "shared_link",
        shared_link = AddShareLinkToFileSharedLink(
            access      = 'open', # AddShareLinkToFileSharedLinkAccessField.OPEN.value
            password    = None,
            unshared_at = None,
            permissions = AddShareLinkToFileSharedLinkPermissionsField(
                can_download = True,
                can_preview  = True,
                can_edit     = False,
            ),
        ),
    ).to_dict()
    file_download_url : str = file_dict['shared_link']['download_url']
    return file_download_url


def _update_file_dlurl(clinet: BoxClient, file_id: str) -> str:
    file_dict : dict = client.shared_links_files.update_shared_link_on_file(
        file_id = file_id,
        fields = "shared_link",
        shared_link = UpdateSharedLinkOnFileSharedLink(
            access      = 'open',
            password    = None,
            unshared_at = None,
            permissions = UpdateSharedLinkOnFileSharedLinkPermissionsField(
                can_download = True,
                can_preview  = True,
                can_edit     = False,
            ),
        ),
    ).to_dict()
    file_download_url : str = file_dict['shared_link']['download_url']
    return file_download_url



''' ————————————————————————— Registry Constructors ———————————————————————— '''


def add_fileinfo_to_registry(
    client         : BoxClient,
    root_folder_id : str,
    func_include   : Callable[[PurePosixPath], bool] = lambda x: True,
    func_exclude   : Callable[[PurePosixPath], bool] = lambda x: False,
    registry       : dict = None,
) -> dict:
    if registry is None:
        registry = {}

    def _traverse_folder(
        this_folder_id : str,
        this_registry  : dict,
        path_stack     : List[str] = [],
    ) -> dict:
        path_stack.append(_get_folder_name(client, this_folder_id))

        for entry in _get_folder_entries(client, this_folder_id): # List[dict]

            this_entry_fullpath : PurePosixPath = PurePosixPath(*path_stack, entry['name'])

            if (not func_include(this_entry_fullpath)) or (func_exclude(this_entry_fullpath)):
                continue

            match entry['type']:
                case 'folder':
                    _traverse_folder(
                        this_folder_id = entry['id'],
                        this_registry  = this_registry,
                        path_stack     = path_stack,
                    )
                case 'file':
                    this_registry[str(this_entry_fullpath)] = {
                        'box_id': entry['id'],
                        'sha1': entry['sha1'],
                    }

        path_stack.pop()
        return this_registry

    return _traverse_folder(root_folder_id, registry)



def add_filedlurls_to_registry(
    client       : BoxClient,
    registry_v1  : dict,
    log          : logging.Logger,
    progress_bar : bool = True,
) -> dict:
    """
    Assume that `registry_v1` is dict of sub-dicts, where sub-dicts look like:
        'redplanet_cache/Mag/Langlais2019.sh': {
            'box_id': '1568919057294',
            'sha1'       : '0625c76c9594d1bf22e3bfa6c17ca8ee36ac2d2a'
        }
    """
    registry_v2 : dict = {}

    idx_progress       : int = 1
    num_added_share    : int = 0
    num_fixed_share    : int = 0
    num_already_shared : int = 0

    iterable = tqdm(registry_v1.items(), desc="Adding download URLs to registry") if progress_bar else registry_v1.items()

    log.debug('')
    log.debug('')
    log.debug('')

    for filepath, fileinfo in iterable:

        file_id          : str  = fileinfo['box_id']

        progress_idx_str : str = f"{idx_progress:0{len(str(len(registry_v1)))}}/{len(registry_v1)}" # basically just "01/10", "02/10", ...
        log.debug(f'[{progress_idx_str}]')
        idx_progress += 1
        log.debug(f'    - [FILE INFO:]')
        log.debug(f'        - {filepath = }')
        # log.debug(f'        - {file_id = }')
        log.debug(f'        - {fileinfo = }')

        file_sharestatus : list = _get_file_sharestatus(client, file_id)
        file_dlurl       : str

        file_sharestatus_code = file_sharestatus[0]

        log.debug(f'    - [FILE SHARE STATUS:]')
        # log.debug(f'        - {file_sharestatus_code = }')
        log.debug(f'        - {file_sharestatus = }')

        match file_sharestatus[0]:
            case 'not shared':
                file_dlurl = _add_file_dlurl(client, file_id)
                num_added_share += 1

            case 'incorrect sharing permissions':
                file_dlurl = _update_file_dlurl(client, file_id)
                num_fixed_share += 1

            case 'correct sharing permissions':
                file_dlurl = file_sharestatus[2]
                num_already_shared += 1

        registry_v2[filepath] = fileinfo | {'download_url': file_dlurl}

        log.debug(f'        - {file_dlurl = }')

    return [registry_v2, {'num_added_share'    : num_added_share,
                          'num_fixed_share'    : num_fixed_share,
                          'num_already_shared' : num_already_shared,} ]


''' ———————————————————————————————— Export ———————————————————————————————— '''

def export_registry_to_csv(
    registry  : dict,
    fpath_csv : Path = None
) -> Path:
    if fpath_csv is None:
        dirpath_output = Path.cwd() / 'output'
        dirpath_output.mkdir(exist_ok=True)
        fpath_csv = dirpath_output / f"redplanet_registry_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"

    registry_list : List[dict] = [{'filepath': k, **v} for k, v in registry.items()]
    df = pd.DataFrame(registry_list)
    df.to_csv(fpath_csv, index=False)
    return fpath_csv


''' ######################################################################## '''
'''                                   Main                                   '''
''' ######################################################################## '''

if __name__ == '__main__':
    main()
