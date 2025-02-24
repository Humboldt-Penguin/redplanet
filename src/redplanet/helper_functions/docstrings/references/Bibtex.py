from pathlib import Path
from importlib.resources import files
from dataclasses import dataclass, field





@dataclass(frozen=True)
class Name:
    raw: str

    @property
    def full(self) -> str:
        # e.g. "Hahn, Brian C." -> "Hahn, B. C."
        # e.g. "Goddard Space Flight Center" -> "Goddard Space Flight Center"
        if self._is_human:
            return f'{self.last}, {self._initials}'
        return self._cleaned

    @property
    def last(self) -> str:
        # e.g. "Hahn, Brian C." -> "Hahn"
        # e.g. "Goddard Space Flight Center" -> "Goddard Space Flight Center"
        if self._is_human:
            return self._cleaned.split(', ', 1)[0]
        return self._cleaned

    @property
    def _cleaned(self) -> str:
        return self.raw.strip()

    @property
    def _is_human(self) -> bool:
        # assume that human names will always have a comma, e.g. "Hahn, Brian C."
        return ',' in self._cleaned

    @property
    def _initials(self) -> str:
        # e.g. "Hahn, Brian C." -> "B. C."
        if self._is_human:
            # to get initials, split the first name(s) (e.g. "Brian C.") into tokens (e.g. ["Brian", "C."]) and abbreviate each one (e.g. ["B.", "C."])
            first = self._cleaned.split(', ', 1)[1]
            return ' '.join(f'{token[0]}.' for token in first.split())
        return ''





@dataclass(frozen=True)
class BibtexEntry:
    key: str
    entry_type: str
    fields: dict[str, str | list[str] | list[Name]]


    def cite(self, format: str) -> str:
        match format:

            case 'full':

                match self.entry_type:
                    case 'article':
                        return self._cite_full_article()
                    case 'misc':
                        return self._cite_full_misc()
                    case _:
                        raise ValueError(f'Function `cite()` received an invalid value for `entry_type` -- must be one of "article" or "misc", but got: {self.entry_type=}')

            case 'narrative':
                return f'{self._authors_intext(parenthetical=False)} ({self.fields["year"]})'

            case 'parenthetical':  # note: you must add the parentheses yourself
                return f'{self._authors_intext(parenthetical=True)}, {self.fields["year"]}'

            case _:
                raise ValueError(f'Function `cite()` received an invalid value for `format` -- must be one of "full", "narrative", or "parenthetical", but got: {format=}')


    def _cite_full_article(self) -> str:
        """
        Build a full APA citation for an article.
        """
        authors = self._authors_full()
        year    = self.fields['year']
        title   = self.fields['title']

        journal = self.fields['journal']
        volume  = self.fields.get('volume', '')
        issue   = self.fields.get('number', '')
        pages   = self.fields.get('pages' , '')

        link = self.fields.get('doi') or self.fields.get('url')
        if not link: raise ValueError(f'No DOI or URL found for entry {self.key}')

        # build the journal info (italicized using asterisks)
        journal_info = f'*{journal}*'
        if volume:
            journal_info += f', {volume}'
        if issue:
            journal_info += f'({issue})'
        if pages:
            journal_info += f', {pages}'

        return f'{authors} ({year}). {title}. {journal_info}. {link}'


    def _cite_full_misc(self) -> str:
        """
        Build a full APA citation for a misc type reference (e.g. dataset).
        """
        authors = self._authors_full()
        year    = self.fields['year']
        title   = self.fields['title']

        publisher = self.fields['publisher']  # data host, e.g. "USGS" or "Zenodo"

        link = self.fields.get('doi') or self.fields.get('url')
        if not link: raise ValueError(f'No DOI or URL found for entry {self.key}')

        title = f'*{title}*'
        if 'dataset' in self.fields.get('keywords', []):
            title += ' [Dataset]'

        return f'{authors} ({year}). {title}. {publisher}. {link}'


    def _authors_full(self) -> str:
        """
        Format a list of authors for a *full* APA citation.

        Input : [ Name(raw='Hahn, B. C.'), Name(raw='McLennan, S. M.'), Name(raw='Klein, E. C.') ]
        Output: "Hahn, B. C., McLennan, S. M., & Klein, E. C."
        """
        authors: list[Name] = self.fields['author']
        if len(authors) == 1:
            return authors[0].full
        else:
            return ', '.join(a.full for a in authors[:-1]) + f', & {authors[-1].full}'


    def _authors_intext(
        self,
        parenthetical: bool,
    ) -> str:
        """
        Format a list of authors for *narrative or parenthetical* APA citations.
            - For one author, use the last name.
            - For two authors, join last names with "and" (narrative) or "&" (parenthetical).
            - For three or more, use only the first author's last name plus "et al."

        Input : ['Gong, Shengxia', 'Wieczorek, Mark']
        Output: "Gong and Wieczorek" (parenthetical=False)
        Output: "Gong & Wieczorek"   (parenthetical=True)

        Input:  ['Hahn, Brian C.', 'McLennan, S. M.', 'Klein, E. C.']
        Output: "Hahn et al."
        """
        authors: list[Name] = self.fields['author']
        match len(authors):
            case 1:
                return authors[0].last
            case 2:
                join  = '&' if parenthetical else 'and'
                return f'{authors[0].last} {join} {authors[1].last}'
            case _:
                return f'{authors[0].last} et al.'





@dataclass(frozen=True)
class BibtexDatabase:
    fpath: Path
    entries: dict[str, BibtexEntry] = field(init=False)


    def __post_init__(self):
        bib_dict = self._read_bibtex_file(self.fpath)
        bib_dict = self._postprocess_clean_strings(bib_dict)
        bib_dict = self._postprocess_separate_list(bib_dict, 'keywords', ', ')
        bib_dict = self._postprocess_separate_list(bib_dict, 'author', ' and ')
        bib_dict = self._postprocess_format_names(bib_dict)

        entries = {}

        for key in bib_dict:
            entry = BibtexEntry(
                key = key,
                entry_type = bib_dict[key]['type'],
                fields = bib_dict[key],
            )
            entries[key] = entry

        # self.entries = entries
        object.__setattr__(self, 'entries', entries)



    def cite(self, key: str, format: str) -> str:
        try:
            return self.entries[key].cite(format)
        except KeyError:
            raise KeyError(f'Key "{key}" not found in the BibTeX database. Options are: {list(self.entries.keys())}')



    @staticmethod
    def _read_bibtex_file(fpath: Path) -> dict[str, dict]:
        """
        Read a BibTeX file and convert to a dictionary with minimal processing.

        Sample input (contents of file):
            ```
            @misc{Goddard2003,
                author = {Goddard Space Flight Center},
                title = {{Mars MGS MOLA DEM 463m}},
                year = {2003},
            }
            ```

        Sample output (python dictionary):
            ```
            'Goddard2003': {
                'type': 'misc',
                'author': '{Goddard Space Flight Center}',
                'title': '{{Mars MGS MOLA DEM 463m}}',
                'year': '{2003}',
            }
            ```
        """
        lines = [
            line.strip()
            for line in
                fpath.read_text().split('\n')
        ]

        entries = {}
        current_key = None

        for i, line in enumerate(lines):

            # case 1: skip comments and non-fields (empty or closing brace)
            if line.startswith('%') or not line or line.startswith('}'):
                continue

            # case 2: new entry (e.g., '@article{...' )
            elif line.startswith('@'):
                this_type = line.split('{')[0][1:].lower()
                this_key = line.split('{')[1].split(',')[0].strip()
                entries[this_key] = {'type': this_type}
                current_key = this_key
                continue

            # case 3: field
            else:
                if '=' not in line:
                    raise ValueError(f"Invalid line {i} (missing equals sign): {line}")
                    # continue
                if not line.endswith(','):
                    raise ValueError(f"Invalid line {i} (missing comma): {line}")
                    # continue

                (field_name, field_val) = line.split('=', 1)
                field_name = field_name.strip().lower()
                field_val = field_val.strip().rstrip(',')

                entries[current_key][field_name] = field_val

        return entries



    @staticmethod
    def _postprocess_clean_strings(d: dict[str, dict]) -> dict[str, dict]:
        """
        Convert all fields in a dictionary of BibTeX entries (see output of `_read_bibtex_file`) to plain strings. This basically means removing curly braces and quotes.

        Sample input:
            ```
            'Goddard2003': {
                'type': 'misc',
                'author': '{Goddard Space Flight Center}',
                'title': '{{Mars MGS MOLA DEM 463m}}',
                'year': '"2003"'
            }
            ```

        Sample output:
            ```
            'Goddard2003': {
                'type': 'misc',
                'author': 'Goddard Space Flight Center',
                'title': 'Mars MGS MOLA DEM 463m',
                'year': '2003'
            }
            ```
        """
        for key in d:
            for name, val in d[key].items():
                if name == 'type':
                    continue

                if val.startswith('{{') and val.endswith('}}'):
                    val = val[2:-2]
                elif (val.startswith('{') and val.endswith('}')) or (val.startswith('"') and val.endswith('"')):
                    val = val[1:-1]
                else:
                    raise ValueError(f"Invalid value: {val}")
                    # continue

                d[key][name] = val.strip()

        return d



    @staticmethod
    def _postprocess_separate_list(
        d          : dict[str, dict],
        field_name : str,
        sep        : str,
    ) -> dict[str, dict]:
        """
        In a dictionary of BibTeX entries (see output of `parse_bibtex_file`), convert a field from a single string to a list of strings.

        Input:  "dataset, MOLA, DEM"
        Output: ['dataset', 'MOLA', 'DEM']

        Input:  "Hahn, B. C. and McLennan, S. M. and Klein, E. C."
        Output: ['Hahn, B. C.', 'McLennan, S. M.', 'Klein, E. C.']
        """
        for key in d:
            if field_name in d[key]:
                d[key][field_name] = d[key][field_name].split(sep)
        return d



    @staticmethod
    def _postprocess_format_names(d: dict[str, dict]) -> dict[str, dict]:
        """
        In a dictionary of BibTeX entries (see output of `parse_bibtex_file`), convert author names from list[str] to list[Name].
        """
        for key in d:
            if 'author' in d[key]:
                d[key]['author'] = [Name(name) for name in d[key]['author']]
        return d
