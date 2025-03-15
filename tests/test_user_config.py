from pathlib import Path
from platformdirs import user_cache_dir

import pytest

from redplanet.user_config import (
	get_dirpath_datacache,
	set_dirpath_datacache,
)





## `get_dirpath_datacache` (public function)
class Test__get_dirpath_datacache:

	## Valid input, default value
	def test__get_dirpath_datacache__default_value(self):
		current_path = get_dirpath_datacache()
		print(f'\n\t- Default data cache path: {current_path}')

		assert current_path == Path(user_cache_dir(appname="redplanet")).resolve()





## `set_dirpath_datacache` (public function)
class Test__set_dirpath_datacache:

	## Valid input: str
	def test__set_dirpath_datacache__valid_string(self):
		valid_path_str = "/tmp/redplanet_cache"
		set_dirpath_datacache(valid_path_str)

		assert get_dirpath_datacache() == Path(valid_path_str).resolve()


	## Valid input: pathlib.Path
	def test__set_dirpath_datacache__valid_path_object(self):
		valid_path_obj = Path("/tmp/redplanet_cache")
		set_dirpath_datacache(valid_path_obj)

		assert get_dirpath_datacache() == valid_path_obj.resolve()


	## Invalid input: str not valid path
	def test__set_dirpath_datacache__invalid_string(self):
		invalid_path_str = "\0"

		with pytest.raises(ValueError, match='Invalid path string provided:'):
			set_dirpath_datacache(invalid_path_str)


	## Invalid input: type not str or Path
	def test__set_dirpath_datacache__invalid_type(self):
		invalid_path_type = 12345

		with pytest.raises(TypeError, match='Path must be a string or a Path object.'):
			set_dirpath_datacache(invalid_path_type)
