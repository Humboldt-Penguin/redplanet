from collections.abc import Callable

from redplanet.helper_functions.docstrings.direct_subs.main import _substitute_direct
from redplanet.helper_functions.docstrings.references.main import _substitute_references


def substitute_docstrings(func: Callable) -> Callable:
    """
    Substitute common docstrings into a function's docstring.

    Parameters
    ----------
    func : Callable
        The function to modify.

    Returns
    -------
    Callable
        The modified function with common docstrings substituted.
    """

    if not func.__doc__:
        return func

    func = _substitute_direct(func)
    func = _substitute_references(func)

    return func
