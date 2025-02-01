## Define public API (self note: https://stackoverflow.com/questions/44834/what-does-all-mean-in-python)
__all__ = []



from redplanet import (
    ## meta package management
    user_config,

    ## load/access datasets
    Craters,
    Crust,
    GRS,
    Mag,

    ## high-level analysis
    analysis,
)

__all__.extend([
    'user_config',

    'Craters',
    'Crust',
    'GRS',
    'Mag',

    'analysis',
])
