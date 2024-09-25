# from pathlib import Path
# from platformdirs import user_cache_dir

# import pytest

# from redplanet.DatasetManager.master import _get_fpath_dataset


# ## `_get_fpath_dataset` (internal function) -- download/cache dataset
# class Test__get_fpath_dataset:

#     ## Valid input: default cache dir
#     def test__get_fpath_dataset__valid_default_cachedir(self):
#         fpath_expected = Path(user_cache_dir()).resolve() / 'redplanet' / 'Crust' / 'dichotomy' / 'dichotomy_coordinates-JAH-0-360.txt'

#         ## delete file if it already exists
#         if (fpath_expected.is_file()):
#             fpath_expected.unlink()

#         ## download file to cache
#         fpath_actual = _get_fpath_dataset('dichotomy_coords')

#     ## Valid input: custom cache dir
#     def test__get_fpath_dataset__valid_custom_cachedir(self):
#         ...
