from collections.abc import Callable
import re
from textwrap import dedent, indent

from redplanet.helper_functions.docstrings.direct_subs import _dict_fragments
# from redplanet.helper_functions.docstrings.references import _dict_references



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

    func = _direct_substitutions(func)

    return func



def _direct_substitutions(func: Callable) -> Callable:

    ## python multiline strings are weird -- strip the leading indentation for every line, and single newline at the very start
    dict_fragments = {
        k: dedent(v.rstrip()[1:])
        for k, v in _dict_fragments.items()
    }

    ## match the key (e.g. `{lon_param}`), assuming it appears at the START of a line and might be indented (i.e. leading whitespace)
    pattern = re.compile(r"^( *)\{([^}]+)\}", re.MULTILINE)

    def repl(match):
        current_indent, key = match.groups()
        fragment = dict_fragments.get(key)
        if fragment is not None:
            ## re-indent the fragment to match the placeholder’s indent.
            return indent(fragment, current_indent)
        ## if the key isn't found, leave the placeholder unchanged.
        return match.group(0)

    ## replace all occurrences in a single pass over the docstring.
    func.__doc__ = pattern.sub(repl, func.__doc__)
    return func
