import re
from textwrap import dedent, indent


def substitute_docstrings(func):

    if not func.__doc__:
        return func

    common_docstrings = {
        'param_lon':
            '''
            lon : float | np.ndarray
                Longitude coordinate(s) in range [-180, 360].
            ''',
        'param_lat':
            '''
            lat : float | np.ndarray
                Latitude coordinate(s) in range [-90, 90].
            ''',
        'param_as_xarray':
            '''
            as_xarray : bool, optional
                If True, return the data as an `xarray.DataArray`. Default is False.
            ''',
        'return_GriddedData':
            '''
            float | np.ndarray | xr.DataArray
                Data value(s) at the the input coordinates. The return type is determined as follows:

                - float: if both `lon` and `lat` are floats.
                - numpy.ndarray (1D): if one of `lon` or `lat` is a numpy 1D array and the other is a float.
                - numpy.ndarray (2D): if both `lon` and `lat` are numpy 1D arrays. The first dimension of output array corresponds to `lat` values.
                - xarray.DataArray: see `as_xarray` parameter (this takes precedence over the above types).
            ''',
    }

    ## python multiline strings are weird -- this strips whitespace/indentation so everything is as expected
    common_docstrings = {k: dedent(v.rstrip()[1:]) for k, v in common_docstrings.items()}

    ## replace the placeholders in the docstring with the corresponding common fragments -- the complexity comes from ensuring the inserted fragments are properly indented
    for key, fragment in common_docstrings.items():
        ## match the placeholder in the docstring (e.g. `{lon_param}`), assuming it appears at the START of a line and might be indented (i.e. leading whitespace)
        placeholder = r"^( *)\{" + re.escape(key) + r"\}"
        def repl(match):
            ## get the captured indentation
            current_indent = match.group(1)
            ## re-indent the common fragment to match the placeholder’s indent
            return indent(fragment, current_indent)
        ## replace all occurrences of the placeholder with the properly indented fragment
        func.__doc__ = re.sub(placeholder, repl, func.__doc__, flags=re.MULTILINE)

    return func
