## Define public API (self note: https://stackoverflow.com/questions/44834/what-does-all-mean-in-python)
__all__ = []



from redplanet.user_config import set_dirpath_datacache, get_dirpath_datacache
__all__.extend([
    'set_dirpath_datacache',
    'get_dirpath_datacache',
])

# from redplanet import DatasetManager
# __all__.extend([
#     'DatasetManager'
# ])
