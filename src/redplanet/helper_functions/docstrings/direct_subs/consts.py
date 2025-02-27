_dict_fragments = {
    'param.lon':
        '''
        lon : float | np.ndarray
            Longitude coordinate(s) in range [-180, 360].
        ''',
    'param.lat':
        '''
        lat : float | np.ndarray
            Latitude coordinate(s) in range [-90, 90].
        ''',
    'param.as_xarray':
        '''
        as_xarray : bool, optional
            If True, return the data as an `xarray.DataArray`. Default is False.
        ''',
    'return.GriddedData':
        '''
        float | np.ndarray | xr.DataArray
            Data values at the the input coordinates. The return type is determined as follows:

            - float: if both `lon` and `lat` are floats.
            - numpy.ndarray (1D): if one of `lon` or `lat` is a numpy 1D array and the other is a float.
            - numpy.ndarray (2D): if both `lon` and `lat` are numpy 1D arrays. The first dimension of output array corresponds to `lat` values.
            - xarray.DataArray: see `as_xarray` parameter (this takes precedence over the above types).
        ''',
    'fulldoc.get_dataset_GriddedData':
        '''
        Get the underlying dataset which is currently loaded.

        Returns
        -------
        GriddedData
            Instance of RedPlanet's `GriddedData` class, which stores all coordinate/data/metadata information and accessing/plotting methods.

        Raises
        ------
        ValueError
            If the dataset has not been loaded yet (see the `load` function for this module).

        See Also
        --------
        `redplanet.helper_functions.GriddedData`
        ''',
    'fulldoc.get_metadata':
        '''
        Get metadata for the dataset which is currently loaded.

        Returns
        -------
        dict
            Contains information about the dataset such as description, units, references, download links, local file path, etc.

        Raises
        ------
        ValueError
            If the dataset has not been loaded yet (see the `load` function for this module).
        ''',
    'note._load':
        '''
        NOTE: This method is private & less modular because there will only ever be one GRS dataset, so lazy loading upon the first access is fine. In contrast, in other modules like `Crust.topo` / `Crust.moho`, we want the user to explicitly/deliberately call `load(<model_params>)` so they're aware of different models and which one they're choosing.
        ''',
}
