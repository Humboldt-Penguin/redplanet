from collections.abc import Callable
import re
from textwrap import indent
from importlib.resources import files

from redplanet.helper_functions.docstrings.references.Bibtex import BibtexDatabase


__bibtex_db: BibtexDatabase = BibtexDatabase(
    fpath = files('redplanet.helper_functions.docstrings.references') / 'references.bib'
)

## match {@key} anywhere in the docstring (even mid-sentence), capturing preceding whitespace (if any)
__pattern = re.compile(r'\{@([^}]+)\}')


def __cite_intext(key: str) -> list[str, str]:
    """
    Format an intext citation

    Parameters
    ----------
    key : str
        Format is "ref.f", where "ref" references the bib file, and "f" is the format of intext citation which can be "p" (parenthetical) or "n" (textual).

    Returns
    -------
    list[str, str]
        Formatted intext and full citations respectively.

    Raises
    ------
    ValueError
        If the `key` is not in the correct format (see parameter definition).
    KeyError
        If the "ref" part of the `key` is not in the bib file.
    """

    parts = key.rsplit('.', 1)

    if len(parts) == 1:
        raise ValueError(f'Invalid intext citation: "{key}" -- Must be in the form "key.f", where "key" references the bib file, and "f" is the format of intext citation which can be "p" (parenthetical) or "n" (textual).')

    ref_key, citation_format = parts

    ## note: errors for `ref_key` not in bib file or an invalid `citation_format` are handled by `BibtexDatabase.cite()`
    return [
        __bibtex_db.cite(ref_key, citation_format),
        __bibtex_db.cite(ref_key, 'full')
    ]



def _substitute_references(func: Callable) -> Callable:

    ## 1/2: substitute the intext citations.
    full_citations = set()

    def repl(match: re.Match) -> str:
        ref_key = match.group(1)
        intext, full = __cite_intext(ref_key)
        full_citations.add(full)
        return intext

    func.__doc__ = __pattern.sub(repl, func.__doc__)

    if not full_citations:
        return func

    ## 2/2: add the full citations to the end of the docstring.
    full_citations = sorted(list(full_citations))

    refs = [
        'References',
        '----------',
    ]
    refs.extend(f'{i}. {cite}' for i, cite in enumerate(full_citations, 1))
    refs = '\n'.join(refs)

    ## add indentation to match the rest of the docstring, which is taken from the first non-empty line
    for line in func.__doc__.split('\n'):
        if line.strip():
            indentation = line[:len(line) - len(line.lstrip())]
            refs = indent(refs, indentation)
            break

    func.__doc__ += f'\n\n{refs}'

    return func
