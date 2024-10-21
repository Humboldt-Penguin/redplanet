# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
# ]
# ///

from pathlib import Path

import pandas as pd



def main():
    fpath_registry = Path('/home/lain/root/100_work/110_projects/111_mars/code-repos/redplanet_datasets__cloud_upload_V2wUV/output/redplanet_registry_2024-10-19_18-35.csv')
    reg_old = pd.read_csv(fpath_registry).to_dict(orient='list')

    reg_new = []

    needle = 'Moho-Mars-'

    for filepath, sha1, url in zip(reg_old['filepath'], reg_old['sha1'], reg_old['download_url']):
        filestem = Path(filepath).stem
        if not filestem.startswith(needle):
            continue
        model_name = filestem[ len(needle) : ]
        download_code = url.split('/')[-1][:-3]
        reg_new.append([model_name, download_code, sha1])

    reg_new = pd.DataFrame(reg_new, columns=['model_name', 'box_download_code', 'sha1'])
    reg_new.sort_values(by='model_name', inplace=True)

    reg_new.to_csv('moho_registry.csv', index=False)



if __name__ == '__main__':
    main()



'''
Basic search function:

    ```
    import pandas as pd

    def search_moho_registry(model_name, fpath_moho_registry) -> list[str,str]:
        """
        Parameters:
            - `model_name`: str
                - Model name in the format 'MODEL-THICK-RHOS-RHON', e.g. 'Khan2022-38-2900-2900'.

        Returns:
            - list[str,str]
                - `box_download_code`, which yields a download link when appended to 'https://rutgers.box.com/shared/static/'.
                - `sha1` hash.
        """
        df = pd.read_csv(fpath_moho_registry)
        result = df[ df['model_name'] == model_name ]
        if result.empty:
            result = None
        else:
            result = result.values.tolist()[0][1:]
        return result


    model_name = 'Khan2022-38-2900-2900'
    fpath_moho_registry = Path('moho_registry.csv')
    result = search_moho_registry(model_name, fpath_moho_registry)
    print(f'{result = }')
    ```








------------------------------


ALT REGISTRY METHOD (nested json which gets rid of redundant text by structuring/aceessing like `registry['Khan2022'][38][2900][2900]`, but it ends up being the same size ~2mb as a plain csv lol rip):

    ```
    from pathlib import Path
    import json

    import pandas as pd



    fpath_registry = Path('/home/lain/root/100_work/110_projects/111_mars/code-repos/redplanet_datasets__cloud_upload_V2wUV/output/redplanet_registry_2024-10-19_18-35.csv')

    registry = pd.read_csv(fpath_registry)
    registry = registry.to_dict(orient='list')

    new = {}

    for filepath, sha1, url in zip(registry['filepath'], registry['sha1'], registry['download_url']):
        if 'Moho-Mars' not in filepath:
            continue

        url = url.split('/')[-1]

        filename = Path(filepath).stem
        moho_code = filename.split('-')[2:]

        for i in [1,2,3]:
            moho_code[i] = int(moho_code[i])

        pointer = new
        for value in moho_code[:-1]:
            if value not in pointer:
                pointer[value] = {}
            pointer = pointer[value]
        pointer[ moho_code[-1] ] = [url, sha1]



    fpath_new_registry = Path('registry.json')
    if fpath_new_registry.is_file(): fpath_new_registry.unlink()

    with open(fpath_new_registry, 'w') as f:
        json.dump(new, f)



    ######################################################
    """ensure new registry was constructed properly"""

    i = 0
    hashes = set()

    def count_items(d):
        global i
        global hashes
        for value in d.values():
            if isinstance(value, dict):
                count_items(value)
            else:
                i += 1
                this_hash = value[1]
                # if this_hash in hashes:
                #     print(f'{value = }')
                hashes.add(this_hash)

    """
    Expected output:
    num entries: 21894
    num unique files (by hash): 17092
    """

    count_items(new)
    print(f'num entries: {i}')
    print(f'num unique files (by hash): {len(hashes)}')
    ```



'''
