from collections.abc import Callable
import re
from textwrap import dedent, indent

from redplanet.helper_functions.docstrings.direct_subs.consts import _dict_fragments


## python multiline strings are weird -- remove the common indentation and first/last newlines.
__cached_fragments = {
    k: dedent(v.rstrip()[1:])
    for k, v in _dict_fragments.items()
}

## match the key (e.g. `{param.lon}`), assuming it appears at the START of a line and might be indented (i.e. leading whitespace)
__pattern = re.compile(r"^( *)\{([^}]+)\}", re.MULTILINE)

## replace the key with the corresponding fragment, indented to match the placeholder’s indent.
def __repl(match):
    current_indent, key = match.groups()
    fragment = __cached_fragments.get(key)
    if fragment is not None:
        ## re-indent the fragment to match the placeholder’s indent.
        return indent(fragment, current_indent)
    ## if the key isn't found, leave the placeholder unchanged.
    return match.group(0)


def _substitute_direct(func: Callable) -> Callable:
    ## replace all occurrences in a single pass over the docstring.
    func.__doc__ = __pattern.sub(__repl, func.__doc__)
    return func
