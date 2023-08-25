#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2008-2022
#  National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________
"""This module provides general utilities for producing formatted I/O

.. autosummary::

   tostr
   tabular_writer
   wrap_reStructuredText
   StreamIndenter
"""

import re
import types
from pyomo.common.sorting import sorted_robust


def tostr(value, quote_str=False):
    """Convert a value to a string

    This function is a thin wrapper around `str(value)` to resolve a
    problematic __str__ implementation in the standard Python container
    types (tuple, list, and dict).  Those classes implement __str__ the
    same as __repr__ (by calling repr() on each contained object).  That
    is frequently undesirable, as you may wish the string representation
    of a container to contain the string representations of the
    contained objects.

    This function generates string representations for native Python
    containers (tuple, list, and dict) that contains the string
    representations of the contained objects.  In addition, it also
    applies the same special handling to any types that derive from the
    standard containers without overriding either __repn__ or __str__.

    Parameters
    ----------
    value: object
        the object to convert to a string
    quote_str: bool
        if True, and if `value` is a `str`, then return a "quoted
        string" (as generated by repr()).  This is primarily used when
        recursively processing native Python containers.

    Returns
    -------
    str

    """
    # Override the generation of str(list), but only if the object is
    # using the default implementation of list.__str__.  Note that the
    # default implementation of __str__ (in CPython) is to call __repr__,
    # so we will test both.  This is particularly important for
    # collections.namedtuple, which reimplements __repr__ but not
    # __str__.
    _type = type(value)
    if _type not in tostr.handlers:
        # Default to the None handler (just call str()), but override it
        # in particular instances:
        tostr.handlers[_type] = tostr.handlers[None]
        if isinstance(value, list):
            if _type.__str__ is list.__str__ and _type.__repr__ is list.__repr__:
                tostr.handlers[_type] = tostr.handlers[list]
        elif isinstance(value, tuple):
            if _type.__str__ is tuple.__str__ and _type.__repr__ is tuple.__repr__:
                tostr.handlers[_type] = tostr.handlers[tuple]
        elif isinstance(value, dict):
            if _type.__str__ is dict.__str__ and _type.__repr__ is dict.__repr__:
                tostr.handlers[_type] = tostr.handlers[dict]
        elif isinstance(value, str):
            tostr.handlers[_type] = tostr.handlers[str]

    return tostr.handlers[_type](value, quote_str)


tostr.handlers = {
    list: lambda value, quote_str: (
        "[%s]" % (', '.join(tostr(v, True) for v in value))
    ),
    dict: lambda value, quote_str: (
        "{%s}"
        % (
            ', '.join(
                '%s: %s' % (tostr(k, True), tostr(v, True)) for k, v in value.items()
            )
        )
    ),
    tuple: lambda value, quote_str: (
        "(%s,)" % (tostr(value[0], True),)
        if len(value) == 1
        else "(%s)" % (', '.join(tostr(v, True) for v in value))
    ),
    str: lambda value, quote_str: (repr(value) if quote_str else value),
    None: lambda value, quote_str: str(value),
}


def tabular_writer(ostream, prefix, data, header, row_generator):
    """Output data in tabular form

    Parameters
    ----------
    ostream: io.TextIOBase
        the stream to write to
    prefix: str
        prefix each generated line with this string
    data: iterable
        an iterable object that returns (key, value) pairs
        (e.g., from iteritems()) defining each row in the table
    header: List[str]
        list of column headers
    row_generator: function
        a function that accepts the `key` and `value` from `data` and
        returns either a tuple defining the entries for a single row, or
        a generator that returns a sequence of table rows to be output
        for the specified `key`

    """

    prefix = tostr(prefix)

    _rows = {}
    # NB: _width is a list because we will change these values
    if header:
        header = (u"Key",) + tuple(tostr(x) for x in header)
        _width = [len(x) for x in header]
    else:
        _width = None
    _minWidth = 0

    for _key, _val in data:
        try:
            _rowSet = row_generator(_key, _val)
            if isinstance(_rowSet, types.GeneratorType):
                _rowSet = list(_rowSet)
            else:
                _rowSet = [_rowSet]
        except ValueError:
            # A ValueError can be raised when row_generator is called
            # (if it is a function), or when it is exhausted generating
            # the list (if it is a generator)
            _minWidth = 4  # Ensure columns are wide enough to output "None"
            _rows[_key] = None
            continue

        _rows[_key] = [
            ((tostr("" if i else _key),) if header else ())
            + tuple(tostr(x) for x in _r)
            for i, _r in enumerate(_rowSet)
        ]

        if not _rows[_key]:
            _minWidth = 4
        elif not _width:
            _width = [0] * len(_rows[_key][0])
        for _row in _rows[_key]:
            for col, x in enumerate(_row):
                _width[col] = max(_width[col], len(x), col and _minWidth)

    # NB: left-justify header entries
    if header:
        # Note: do not right-pad the last header with unnecessary spaces
        tmp = _width[-1]
        _width[-1] = 0
        ostream.write(
            prefix
            + " : ".join("%%-%ds" % _width[i] % x for i, x in enumerate(header))
            + "\n"
        )
        _width[-1] = tmp

    # If there is no data, we are done...
    if not _rows:
        return

    # right-justify data, except for the last column if there are spaces
    # in the data (probably an expression or vector)
    _width = ["%" + str(i) + "s" for i in _width]

    if any(' ' in r[-1] for x in _rows.values() if x is not None for r in x):
        _width[-1] = '%s'
    for _key in sorted_robust(_rows):
        _rowSet = _rows[_key]
        if not _rowSet:
            _rowSet = [[_key] + [None] * (len(_width) - 1)]
        for _data in _rowSet:
            ostream.write(
                prefix + " : ".join(_width[i] % x for i, x in enumerate(_data)) + "\n"
            )


class StreamIndenter(object):
    """
    Mock-up of a file-like object that wraps another file-like object
    and indents all data using the specified string before passing it to
    the underlying file.  Since this presents a full file interface,
    StreamIndenter objects may be arbitrarily nested.
    """

    def __init__(self, ostream, indent=' ' * 4):
        self.os = ostream
        self.indent = indent
        self.stripped_indent = indent.rstrip()
        self.newline = True

    def __getattr__(self, name):
        return getattr(self.os, name)

    def write(self, data):
        if not len(data):
            return
        lines = data.split('\n')
        if self.newline:
            if lines[0]:
                self.os.write(self.indent + lines[0])
            else:
                self.os.write(self.stripped_indent)
        else:
            self.os.write(lines[0])
        if len(lines) < 2:
            self.newline = False
            return
        for line in lines[1:-1]:
            if line:
                self.os.write("\n" + self.indent + line)
            else:
                self.os.write("\n" + self.stripped_indent)
        if lines[-1]:
            self.os.write("\n" + self.indent + lines[-1])
            self.newline = False
        else:
            self.os.write("\n")
            self.newline = True

    def writelines(self, sequence):
        for x in sequence:
            self.write(x)


_indentation_re = re.compile(r'\s*')
_bullet_re = re.compile(
    r'([-+*] +)'  # bulleted lists
    r'|(\(?[0-9]+[\)\.] +)'  # enumerated lists (arabic numerals)
    r'|(\(?[ivxlcdm]+[\)\.] +)'  # enumerated lists (roman numerals)
    r'|(\(?[IVXLCDM]+[\)\.] +)'  # enumerated lists (roman numerals)
    r'|(\(?[a-zA-Z][\)\.] +)'  # enumerated lists (letters)
    r'|(\(?\#[\)\.] +)'  # auto enumerated lists
    r'|([a-zA-Z0-9_ ]+ +: +)'  # definitions
    r'|(:[a-zA-Z0-9_ ]+: +)'  # field name
    r'|(?:\[\s*[A-Za-z0-9\.]+\s*\] +)'  # [PASS]|[FAIL]|[ OK ]
)
_verbatim_line_start = re.compile(
    r'(\| )' r'|(\+((-{3,})|(={3,}))\+)'  # line blocks  # grid table
)
_verbatim_line = re.compile(
    r'(={3,}[ =]+)'  # simple tables, ======== sections
    # sections
    + ''.join(r'|(\%s{3,})' % c for c in r'!"#$%&\'()*+,-./:;<>?@[\\]^_`{|}~')
)


def wrap_reStructuredText(docstr, wrapper):
    """A text wrapper that honors paragraphs and basic reStructuredText markup

    This wraps `textwrap.fill()` to first separate the incoming text by
    paragraphs before using ``wrapper`` to wrap each one.  It includes a
    basic (partial) parser for reStructuredText format to attempt to
    avoid wrapping structural elements like section headings, bullet /
    enumerated lists, and tables.

    Parameters
    ----------
    docstr : str
        The incoming string to parse and wrap

    wrapper : `textwrap.TextWrap`
        The configured `TextWrap` object to use for wrapping paragraphs.
        While the object will be reconfigured within this function, it
        will be restored to its original state upon exit.

    """
    # As textwrap only works on single paragraphs, we need to break
    # up the incoming message into paragraphs before we pass it to
    # textwrap.
    paragraphs = [(None, None, None)]
    literal_block = False
    verbatim = False
    for line in docstr.rstrip().splitlines():
        leading = _indentation_re.match(line).group()
        content = line.strip()
        if not content:
            if literal_block:
                if literal_block[0] == 2:
                    literal_block = False
            elif paragraphs[-1][2] and ''.join(paragraphs[-1][2]).endswith('::'):
                literal_block = (0, paragraphs[-1][1])
            paragraphs.append((None, None, None))
            continue
        if literal_block:
            if literal_block[0] == 0:
                if len(literal_block[1]) < len(leading):
                    # indented literal block
                    literal_block = 1, leading
                    paragraphs.append((None, None, line))
                    continue
                elif (
                    len(literal_block[1]) == len(leading)
                    and content[0] in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
                ):
                    # quoted literal block
                    literal_block = 2, leading
                    paragraphs.append((None, None, line))
                    continue
                else:
                    # invalid literal block
                    literal_block = False
            elif leading.startswith(literal_block[1]):
                paragraphs.append((None, None, line))
                continue
            else:
                # fall back on normal line processing
                literal_block = False
        if content == '```':
            # Not part of ReST, but we have supported this in Pyomo for a long time
            verbatim ^= True
        elif verbatim:
            paragraphs.append((None, None, line))
        elif _verbatim_line_start.match(content):
            # This catches lines that start with patterns that indicate
            # that the line should not be wrapped (line blocks, grid
            # tables)
            paragraphs.append((None, None, line))
        elif _verbatim_line.match(content):
            # This catches whole line patterns that should not be
            # wrapped with previous/subsequent lines (e.g., simple table
            # headers, section headers)
            paragraphs.append((None, None, line))
        else:
            matchBullet = _bullet_re.match(content)
            if matchBullet:
                # Handle things that look like bullet lists specially
                hang = matchBullet.group()
                paragraphs.append((leading, leading + ' ' * len(hang), [content]))
            elif paragraphs[-1][1] == leading:
                # Continuing a text block
                paragraphs[-1][2].append(content)
            else:
                # Beginning a new text block
                paragraphs.append((leading, leading, [content]))

    while paragraphs and paragraphs[0][2] is None:
        paragraphs.pop(0)

    wrapper_init = wrapper.initial_indent, wrapper.subsequent_indent
    try:
        for i, (indent, subseq, par) in enumerate(paragraphs):
            base_indent = wrapper_init[1] if i else wrapper_init[0]

            if indent is None:
                if par is None:
                    paragraphs[i] = ''
                else:
                    paragraphs[i] = base_indent + par
                continue

            wrapper.initial_indent = base_indent + indent
            wrapper.subsequent_indent = base_indent + subseq
            paragraphs[i] = wrapper.fill(' '.join(par))
    finally:
        # Avoid side-effects and restore the initial wrapper state
        wrapper.initial_indent, wrapper.subsequent_indent = wrapper_init

    return '\n'.join(paragraphs)
