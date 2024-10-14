import zipfile
from pathlib import Path
from datetime import datetime
import os

from redplanet.DatasetManager.hash import (
    get_available_algorithms,
    _calculate_hash_from_file,
)

from redplanet.DatasetManager.download import _download_file_from_url


## inputs
files = {
    'README_EBH_SK_AR_SK.txt': 'https://repository.lsu.edu/cgi/viewcontent.cgi?filename=18&article=1000&context=geo_psl&type=additional',
    'Al_GS2010_5x5.txt'      : 'https://repository.lsu.edu/cgi/viewcontent.cgi?filename=9&article=1000&context=geo_psl&type=additional',
    'Ca_GS2010_5x5.txt'      : 'https://repository.lsu.edu/cgi/viewcontent.cgi?filename=10&article=1000&context=geo_psl&type=additional',
    'Cl_GS2010_5x5.txt'      : 'https://repository.lsu.edu/cgi/viewcontent.cgi?filename=11&article=1000&context=geo_psl&type=additional',
    'Fe_GS2010_5x5.txt'      : 'https://repository.lsu.edu/cgi/viewcontent.cgi?filename=12&article=1000&context=geo_psl&type=additional',
    'H2O_GS2010_5x5.txt'     : 'https://repository.lsu.edu/cgi/viewcontent.cgi?filename=13&article=1000&context=geo_psl&type=additional',
    'K_GS2010_5x5.txt'       : 'https://repository.lsu.edu/cgi/viewcontent.cgi?filename=14&article=1000&context=geo_psl&type=additional',
    'S_GS2010_5x5.txt'       : 'https://repository.lsu.edu/cgi/viewcontent.cgi?filename=15&article=1000&context=geo_psl&type=additional',
    'Si_GS2010_5x5.txt'      : 'https://repository.lsu.edu/cgi/viewcontent.cgi?filename=16&article=1000&context=geo_psl&type=additional',
    'Th_GS2010_5x5.txt'      : 'https://repository.lsu.edu/cgi/viewcontent.cgi?filename=17&article=1000&context=geo_psl&type=additional',
}
fname_final = '2022_Mars_Odyssey_GRS_Element_Concentration_Maps.zip'
modtime = datetime(2022, 7, 5, 0, 0, 0).timestamp()
### Note: using zip (as opposed to tar.gz) and setting a fixed modification time ensures consistent hash -- 2022/07/05 is publication date of dataset



## download/zip files
dirpath_output = Path.cwd() / 'output'
dirpath_output.mkdir(exist_ok=True)
fpath_output = dirpath_output / fname_final

with zipfile.ZipFile(fpath_output, "w", zipfile.ZIP_DEFLATED) as zipf:
    for fname, url in files.items():
        fpath_data = dirpath_output / fname

        _download_file_from_url(url, fpath_data)
        os.utime(fpath_data, times=(modtime, modtime))
        zipf.write(fpath_data, arcname=fname)
        fpath_data.unlink()


## print hashes
print(f'{fname_final}')
for alg in get_available_algorithms():
    print(f'- {alg}: {_calculate_hash_from_file(fpath_output, alg)}')

'''
(expected output:)

2022_Mars_Odyssey_GRS_Element_Concentration_Maps.zip
- xxh3_64: a87a1b3db0e0a3a9
- md5: 4f1cf60587e1304a5761f9c009e98e2b
- sha256: ba2b5cc62b18302b1da0c111101d0d2318e69421877c4f9c145116b41502777b
'''

assert _calculate_hash_from_file(fpath_output, 'sha256') == 'ba2b5cc62b18302b1da0c111101d0d2318e69421877c4f9c145116b41502777b'