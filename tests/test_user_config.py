from pathlib import Path
from platformdirs import user_cache_dir

import pytest

from redplanet.user_config import set_dirpath_datacache, get_dirpath_datacache




## Default data cache path
def test__get_dirpath_datacache__with_default_value():
	current_path = get_dirpath_datacache()
	print(f'\n\t- Default data cache path: {current_path}')
	assert current_path == Path(user_cache_dir(appname="redplanet")).resolve()


## Valid input: string
def test__set_dirpath_datacache__with_valid_string():
	valid_path_str = "/tmp/redplanet_cache"
	set_dirpath_datacache(valid_path_str)
	assert get_dirpath_datacache() == Path(valid_path_str)


## Valid input: pathlib.Path
def test__set_dirpath_datacache__with_valid_path_object():
	valid_path_obj = Path("/tmp/redplanet_cache")
	set_dirpath_datacache(valid_path_obj)
	assert get_dirpath_datacache() == valid_path_obj


## Invalid input: bad string/path
def test__set_dirpath_datacache__with_invalid_string():
	invalid_path_str = "\0"
	with pytest.raises(ValueError):
		set_dirpath_datacache(invalid_path_str)


## Invalid input: not string/path
def test__set_dirpath_datacache__with_invalid_type():
	invalid_path_type = 12345
	with pytest.raises(TypeError):
		set_dirpath_datacache(invalid_path_type)