import pandas as pd

from redplanet.DatasetManager.main import _get_fpath_dataset



def get_registry() -> pd.DataFrame:
    """
    Get a list of all available Moho models.

    Returns
    -------
    pd.DataFrame
        DataFrame with the following columns: ['interior_model', 'insight_thickness', 'rho_south', 'rho_north']. For an explanation of these columns, see parameters of `redplanet.Crust.moho.load()`.
    """
    registry = pd.read_csv(
        _get_fpath_dataset('moho_registry'),
        usecols = ['model_name'],
    )
    registry = registry['model_name'].str.split('-', expand=True)
    registry.columns = ['interior_model', 'insight_thickness', 'rho_south', 'rho_north']
    registry.iloc[:,1:] = registry.iloc[:,1:].astype(int)
    return registry



'''
For info/sources on reference interior models, see:
    1. https://markwieczorek.github.io/ctplanet/source/generated/ctplanet.ReadRefModel.html
    2. https://github.com/MarkWieczorek/ctplanet/tree/74e8550080d4adc68ae291a500e8d198a40d437c/examples/Data/Mars-reference-interior-models
'''
_interior_models: list[str] = (
    'DWAK',
    'DWThot',
    'DWThotCrust1',
    'DWThotCrust1r',
    'EH45Tcold',
    'EH45TcoldCrust1',
    'EH45TcoldCrust1r',
    'EH45ThotCrust2',
    'EH45ThotCrust2r',
    'Khan2022',
    'LFAK',
    'SANAK',
    'TAYAK',
    'YOTHotRc1760kmDc40km',
    'YOTHotRc1810kmDc40km',
    'ZG_DW',
)
