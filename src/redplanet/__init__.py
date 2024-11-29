## Define public API (self note: https://stackoverflow.com/questions/44834/what-does-all-mean-in-python)
__all__ = []


import redplanet.user_config
__all__.extend([
    'user_config',    ## module
])
## TODO: not sure if importing `user_config` here is necessary...?


from redplanet.DatasetManager.dataset_info import peek_datasets
__all__.extend([
    'peek_datasets',    ## function
])
