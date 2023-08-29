from __future__ import print_function
from __future__ import unicode_literals
from collections import namedtuple
import sys
import re
import math


if sys.version_info >= (3, 3): from collections.abc import Iterable
else: from collections import Iterable

if sys.version_info[0] < 3:
    from itertools import izip_longest
    from functools import partial

    _none_type,_bool_type,_int_type,_long_type,_float_type,_text_type,_binary_type = type(None),bool,int,long,float,unicode,str

    def _is_file(f): return hasattr(f, "read")


else:
    from itertools import zip_longest as izip_longest
    from functools import reduce, partial

    _none_type,_bool_type,_int_type,_long_type,_float_type,_text_type,_binary_type,basestring = type(None),bool,int,int,float,str,bytes,str


    import io

    def _is_file(f): return isinstance(f, io.IOBase)


try: import wcwidth
except ImportError: wcwidth = None

try: from html import escape as htmlescape
except ImportError: from cgi import escape as htmlescape


__all__ = ["tabulate", "tabulate_formats", "simple_separated_format"]



MIN_PADDING = 2
PRESERVE_WHITESPACE = False
_DEFAULT_FLOAT_FMT,_DEFAULT_MISSINGVAL = "g",""
_DEFAULT_ALIGN = "default"
WIDE_CHARS_MODE = wcwidth is not None
Line = namedtuple("Line", ["begin", "hline", "sep", "end"])
DataRow = namedtuple("DataRow", ["begin", "sep", "end"])

TableFormat = namedtuple(
    "TableFormat",
    [
        "lineabove",
        "linebelowheader",
        "linebetweenrows",
        "linebelow",
        "headerrow",
        "datarow",
        "padding",
        "with_header_hide",
    ],
)


def _pipe_segment_with_colons(align, col_width):
    w = col_width
    if align in ["right", "decimal"]: return ("-" * (w - 1)) + ":"
    elif align == "center": return ":" + ("-" * (w - 2)) + ":"
    elif align == "left": return ":" + ("-" * (w - 1))
    else: return "-" * w


def _pipe_line_with_colons(col_widths, col_aligns):
    if not col_aligns: col_aligns = [""] * len(col_widths)
    segments = [_pipe_segment_with_colons(a, w) for a, w in zip(col_aligns, col_widths)]
    return "|" + "|".join(segments) + "|"


def _mediawiki_row_with_attrs(separator, cell_values, col_widths, col_aligns):
    alignment = {
        "left": "",
        "right": 'align="right"| ',
        "center": 'align="center"| ',
        "decimal": 'align="right"| ',
    }


    values_with_attrs = [" " + alignment.get(a, "") + c + " " for c, a in zip(cell_values, col_aligns)]
    col_sep = separator * 2
    return (separator + col_sep.join(values_with_attrs)).rstrip()


def _textile_row_with_attrs(cell_values, col_widths, col_aligns):
    cell_values[0] += " "
    alignment = {"left": "<.", "right": ">.", "center": "=.", "decimal": ">."}
    values = (alignment.get(a, "") + v for a, v in zip(col_aligns, cell_values))
    return "|" + "|".join(values) + "|"


def _html_begin_table_without_header(col_widths_ignore, col_aligns_ignore):
    return "<table>\n<tbody>"


def _html_row_with_attrs(cell_tag, unsafe, cell_values, col_widths, col_aligns):
    alignment = {
        "left": "",
        "right": ' style="text-align: right;"',
        "center": ' style="text-align: center;"',
        "decimal": ' style="text-align: right;"',
    }
    if unsafe:
        values_with_attrs = [
            "<{0}{1}>{2}</{0}>".format(cell_tag, alignment.get(a, ""), c)
            for c, a in zip(cell_values, col_aligns)
        ]
    else:
        values_with_attrs = [
            "<{0}{1}>{2}</{0}>".format(cell_tag, alignment.get(a, ""), htmlescape(c))
            for c, a in zip(cell_values, col_aligns)
        ]
    row_html = "<tr>{}</tr>".format("".join(values_with_attrs).rstrip())
    if cell_tag == "th": row_html = "<table>\n<thead>\n{}\n</thead>\n<tbody>".format(row_html)
    return row_html


def _moin_row_with_attrs(cell_tag, cell_values, col_widths, col_aligns, header=""):
    alignment = {
        "left": "",
        "right": '<style="text-align: right;">',
        "center": '<style="text-align: center;">',
        "decimal": '<style="text-align: right;">',
    }
    values_with_attrs = [
        "{0}{1} {2} ".format(cell_tag, alignment.get(a, ""), header + c + header)
        for c, a in zip(cell_values, col_aligns)
    ]
    return "".join(values_with_attrs) + "||"


def _latex_line_begin_tabular(col_widths, col_aligns, book_tabs=False, long_table=False):
    alignment = {"left": "l", "right": "r", "center": "c", "decimal": "r"}
    tabular_columns_fmt = "".join([alignment.get(a, "l") for a in col_aligns])
    return "\n".join(
        [
            ("\\begin{tabular}{" if not long_table else "\\begin{long_table}{")
            + tabular_columns_fmt
            + "}",
            "\\toprule" if book_tabs else "\\hline",
        ]
    )


LATEX_ESCAPE_RULES = {
    r"&": r"\&",
    r"%": r"\%",
    r"$": r"\$",
    r"#": r"\#",
    r"_": r"\_",
    r"^": r"\^{}",
    r"{": r"\{",
    r"}": r"\}",
    r"~": r"\textasciitilde{}",
    "\\": r"\textbackslash{}",
    r"<": r"\ensuremath{<}",
    r">": r"\ensuremath{>}",
}


def _latex_row(cell_values, col_widths, col_aligns, esc_rules=LATEX_ESCAPE_RULES):
    def escape_char(c): return esc_rules.get(c, c)

    escaped_values = ["".join(map(escape_char, cell)) for cell in cell_values]
    row_fmt = DataRow("", "&", "\\\\")
    return _build_simple_row(escaped_values, row_fmt)


def _rst_escape_first_column(rows, headers):
    def escape_empty(val):
        if isinstance(val, (_text_type, _binary_type)) and not val.strip(): return ".."
        else: return val

    new_headers = list(headers)
    new_rows = []
    if headers: new_headers[0] = escape_empty(headers[0])
    for row in rows:
        new_row = list(row)
        if new_row: new_row[0] = escape_empty(row[0])
        new_rows.append(new_row)
    return new_rows, new_headers


_table_formats = {
    "simple": TableFormat(
        lineabove=Line("", "-", "  ", ""),
        linebelowheader=Line("", "-", "  ", ""),
        linebetweenrows=None,
        linebelow=Line("", "-", "  ", ""),
        headerrow=DataRow("", "  ", ""),
        datarow=DataRow("", "  ", ""),
        padding=0,
        with_header_hide=["lineabove", "linebelow"],
    ),
    "plain": TableFormat(
        lineabove=None,
        linebelowheader=None,
        linebetweenrows=None,
        linebelow=None,
        headerrow=DataRow("", "  ", ""),
        datarow=DataRow("", "  ", ""),
        padding=0,
        with_header_hide=None,
    ),
    "grid": TableFormat(
        lineabove=Line("+", "-", "+", "+"),
        linebelowheader=Line("+", "=", "+", "+"),
        linebetweenrows=Line("+", "-", "+", "+"),
        linebelow=Line("+", "-", "+", "+"),
        headerrow=DataRow("|", "|", "|"),
        datarow=DataRow("|", "|", "|"),
        padding=1,
        with_header_hide=None,
    ),
    "fancy_grid": TableFormat(
        lineabove=Line("╒", "═", "╤", "╕"),
        linebelowheader=Line("╞", "═", "╪", "╡"),
        linebetweenrows=Line("├", "─", "┼", "┤"),
        linebelow=Line("╘", "═", "╧", "╛"),
        headerrow=DataRow("│", "│", "│"),
        datarow=DataRow("│", "│", "│"),
        padding=1,
        with_header_hide=None,
    ),
    "fancy_outline": TableFormat(
        lineabove=Line("╒", "═", "╤", "╕"),
        linebelowheader=Line("╞", "═", "╪", "╡"),
        linebetweenrows=None,
        linebelow=Line("╘", "═", "╧", "╛"),
        headerrow=DataRow("│", "│", "│"),
        datarow=DataRow("│", "│", "│"),
        padding=1,
        with_header_hide=None,
    ),
    "github": TableFormat(
        lineabove=Line("|", "-", "|", "|"),
        linebelowheader=Line("|", "-", "|", "|"),
        linebetweenrows=None,
        linebelow=None,
        headerrow=DataRow("|", "|", "|"),
        datarow=DataRow("|", "|", "|"),
        padding=1,
        with_header_hide=["lineabove"],
    ),
    "pipe": TableFormat(
        lineabove=_pipe_line_with_colons,
        linebelowheader=_pipe_line_with_colons,
        linebetweenrows=None,
        linebelow=None,
        headerrow=DataRow("|", "|", "|"),
        datarow=DataRow("|", "|", "|"),
        padding=1,
        with_header_hide=["lineabove"],
    ),
    "orgtbl": TableFormat(
        lineabove=None,
        linebelowheader=Line("|", "-", "+", "|"),
        linebetweenrows=None,
        linebelow=None,
        headerrow=DataRow("|", "|", "|"),
        datarow=DataRow("|", "|", "|"),
        padding=1,
        with_header_hide=None,
    ),
    "jira": TableFormat(
        lineabove=None,
        linebelowheader=None,
        linebetweenrows=None,
        linebelow=None,
        headerrow=DataRow("||", "||", "||"),
        datarow=DataRow("|", "|", "|"),
        padding=1,
        with_header_hide=None,
    ),
    "presto": TableFormat(
        lineabove=None,
        linebelowheader=Line("", "-", "+", ""),
        linebetweenrows=None,
        linebelow=None,
        headerrow=DataRow("", "|", ""),
        datarow=DataRow("", "|", ""),
        padding=1,
        with_header_hide=None,
    ),
    "pretty": TableFormat(
        lineabove=Line("+", "-", "+", "+"),
        linebelowheader=Line("+", "-", "+", "+"),
        linebetweenrows=None,
        linebelow=Line("+", "-", "+", "+"),
        headerrow=DataRow("|", "|", "|"),
        datarow=DataRow("|", "|", "|"),
        padding=1,
        with_header_hide=None,
    ),
    "psql": TableFormat(
        lineabove=Line("+", "-", "+", "+"),
        linebelowheader=Line("|", "-", "+", "|"),
        linebetweenrows=None,
        linebelow=Line("+", "-", "+", "+"),
        headerrow=DataRow("|", "|", "|"),
        datarow=DataRow("|", "|", "|"),
        padding=1,
        with_header_hide=None,
    ),
    "rst": TableFormat(
        lineabove=Line("", "=", "  ", ""),
        linebelowheader=Line("", "=", "  ", ""),
        linebetweenrows=None,
        linebelow=Line("", "=", "  ", ""),
        headerrow=DataRow("", "  ", ""),
        datarow=DataRow("", "  ", ""),
        padding=0,
        with_header_hide=None,
    ),
    "mediawiki": TableFormat(
        lineabove=Line(
            '{| class="wikitable" style="text-align: left;"',
            "",
            "",
            "\n|+ <!-- caption -->\n|-",
        ),
        linebelowheader=Line("|-", "", "", ""),
        linebetweenrows=Line("|-", "", "", ""),
        linebelow=Line("|}", "", "", ""),
        headerrow=partial(_mediawiki_row_with_attrs, "!"),
        datarow=partial(_mediawiki_row_with_attrs, "|"),
        padding=0,
        with_header_hide=None,
    ),
    "moinmoin": TableFormat(
        lineabove=None,
        linebelowheader=None,
        linebetweenrows=None,
        linebelow=None,
        headerrow=partial(_moin_row_with_attrs, "||", header="'''"),
        datarow=partial(_moin_row_with_attrs, "||"),
        padding=1,
        with_header_hide=None,
    ),
    "youtrack": TableFormat(
        lineabove=None,
        linebelowheader=None,
        linebetweenrows=None,
        linebelow=None,
        headerrow=DataRow("|| ", " || ", " || "),
        datarow=DataRow("| ", " | ", " |"),
        padding=1,
        with_header_hide=None,
    ),
    "html": TableFormat(
        lineabove=_html_begin_table_without_header,
        linebelowheader="",
        linebetweenrows=None,
        linebelow=Line("</tbody>\n</table>", "", "", ""),
        headerrow=partial(_html_row_with_attrs, "th", False),
        datarow=partial(_html_row_with_attrs, "td", False),
        padding=0,
        with_header_hide=["lineabove"],
    ),
    "unsafehtml": TableFormat(
        lineabove=_html_begin_table_without_header,
        linebelowheader="",
        linebetweenrows=None,
        linebelow=Line("</tbody>\n</table>", "", "", ""),
        headerrow=partial(_html_row_with_attrs, "th", True),
        datarow=partial(_html_row_with_attrs, "td", True),
        padding=0,
        with_header_hide=["lineabove"],
    ),
    "latex": TableFormat(
        lineabove=_latex_line_begin_tabular,
        linebelowheader=Line("\\hline", "", "", ""),
        linebetweenrows=None,
        linebelow=Line("\\hline\n\\end{tabular}", "", "", ""),
        headerrow=_latex_row,
        datarow=_latex_row,
        padding=1,
        with_header_hide=None,
    ),
    "latex_raw": TableFormat(
        lineabove=_latex_line_begin_tabular,
        linebelowheader=Line("\\hline", "", "", ""),
        linebetweenrows=None,
        linebelow=Line("\\hline\n\\end{tabular}", "", "", ""),
        headerrow=partial(_latex_row, esc_rules={}),
        datarow=partial(_latex_row, esc_rules={}),
        padding=1,
        with_header_hide=None,
    ),
    "latex_book_tabs": TableFormat(
        lineabove=partial(_latex_line_begin_tabular, book_tabs=True),
        linebelowheader=Line("\\midrule", "", "", ""),
        linebetweenrows=None,
        linebelow=Line("\\bottomrule\n\\end{tabular}", "", "", ""),
        headerrow=_latex_row,
        datarow=_latex_row,
        padding=1,
        with_header_hide=None,
    ),
    "latex_long_table": TableFormat(
        lineabove=partial(_latex_line_begin_tabular, long_table=True),
        linebelowheader=Line("\\hline\n\\endhead", "", "", ""),
        linebetweenrows=None,
        linebelow=Line("\\hline\n\\end{long_table}", "", "", ""),
        headerrow=_latex_row,
        datarow=_latex_row,
        padding=1,
        with_header_hide=None,
    ),
    "tsv": TableFormat(
        lineabove=None,
        linebelowheader=None,
        linebetweenrows=None,
        linebelow=None,
        headerrow=DataRow("", "\t", ""),
        datarow=DataRow("", "\t", ""),
        padding=0,
        with_header_hide=None,
    ),
    "textile": TableFormat(
        lineabove=None,
        linebelowheader=None,
        linebetweenrows=None,
        linebelow=None,
        headerrow=DataRow("|_. ", "|_.", "|"),
        datarow=_textile_row_with_attrs,
        padding=1,
        with_header_hide=None,
    ),
}


tabulate_formats = list(sorted(_table_formats.keys()))




multiline_formats = {
    "plain": "plain",
    "simple": "simple",
    "grid": "grid",
    "fancy_grid": "fancy_grid",
    "pipe": "pipe",
    "orgtbl": "orgtbl",
    "jira": "jira",
    "presto": "presto",
    "pretty": "pretty",
    "psql": "psql",
    "rst": "rst",
}

_multiline_codes = re.compile(r"\r|\n|\r\n")
_multiline_codes_bytes = re.compile(b"\r|\n|\r\n")
_invisible_codes = re.compile(r"\x1b\[\d+[;\d]*m|\x1b\[\d*\;\d*\;\d*m|\x1b\]8;;(.*?)\x1b\\")
_invisible_codes_bytes = re.compile(b"\x1b\\[\\d+\\[;\\d]*m|\x1b\\[\\d*;\\d*;\\d*m|\\x1b\\]8;;(.*?)\\x1b\\\\")
_invisible_codes_link = re.compile(r"\x1B]8;[a-zA-Z0-9:]*;[^\x1B]+\x1B\\([^\x1b]+)\x1B]8;;\x1B\\")


def simple_separated_format(separator):

    return TableFormat(
        None,
        None,
        None,
        None,
        headerrow=DataRow("", separator, ""),
        datarow=DataRow("", separator, ""),
        padding=0,
        with_header_hide=None,
    )


def _is_convert_able(conv, string):
    try:
        conv(string)
        return True
    except (ValueError, TypeError): return False


def _is_number(string):

    if not _is_convert_able(float, string): return False
    elif isinstance(string, (_text_type, _binary_type)) and (math.isinf(float(string)) or math.isnan(float(string))): return string.lower() in ["inf", "-inf", "nan"]
    return True


def _is_int(string, inttype=int):

    return (type(string) is inttype or (isinstance(string, _binary_type) or isinstance(string, _text_type)) and _is_convert_able(inttype, string))


def _is_bool(string):

    return type(string) is _bool_type or (isinstance(string, (_binary_type, _text_type)) and string in ("True", "False"))


def _type(string, has_invisible=True, num_parse=True):


    if has_invisible and (isinstance(string, _text_type) or isinstance(string, _binary_type)): string = _strip_invisible(string)

    if string is None: return _none_type
    elif hasattr(string, "isoformat"): return _text_type
    elif _is_bool(string): return _bool_type
    elif _is_int(string) and num_parse: return int
    elif _is_int(string, _long_type) and num_parse: return int
    elif _is_number(string) and num_parse: return float
    elif isinstance(string, _binary_type): return _binary_type
    else: return _text_type


def _after_point(string):

    if _is_number(string):
        if _is_int(string): return -1
        else:
            pos = string.rfind(".")
            pos = string.lower().rfind("e") if pos < 0 else pos
            if pos >= 0: return len(string) - pos - 1
            else: return -1
    else: return -1


def _pad_left(width, s):

    fmt = "{0:>%ds}" % width
    return fmt.format(s)


def _pad_right(width, s):

    fmt = "{0:<%ds}" % width
    return fmt.format(s)


def _pad_both(width, s):

    fmt = "{0:^%ds}" % width
    return fmt.format(s)


def _pad_none(ignore_width, s): return s


def _strip_invisible(s):

    if isinstance(s, _text_type):
        links_removed = re.sub(_invisible_codes_link, "\\1", s)
        return re.sub(_invisible_codes, "", links_removed)
    else: return re.sub(_invisible_codes_bytes, "", s)


def _visible_width(s):


    if wcwidth is not None and WIDE_CHARS_MODE: len_fn = wcwidth.wcswidth
    else: len_fn = len
    if isinstance(s, _text_type) or isinstance(s, _binary_type): return len_fn(_strip_invisible(s))
    else: return len_fn(_text_type(s))


def _is_multiline(s):
    if isinstance(s, _text_type): return bool(re.search(_multiline_codes, s))
    else: return bool(re.search(_multiline_codes_bytes, s))


def _multiline_width(multiline_s, line_width_fn=len):
    return max(map(line_width_fn, re.split("[\r\n]", multiline_s)))


def _choose_width_fn(has_invisible, enable_widechars, is_multiline):
    if has_invisible: line_width_fn = _visible_width
    elif enable_widechars: line_width_fn = wcwidth.wcswidth
    else: line_width_fn = len
    if is_multiline: width_fn = lambda s: _multiline_width(s, line_width_fn)
    else: width_fn = line_width_fn
    return width_fn


def _align_column_choose_pad_fn(strings, alignment, has_invisible):
    if alignment == "right":
        if not PRESERVE_WHITESPACE: strings = [s.strip() for s in strings]
        pad_fn = _pad_left
    elif alignment == "center":
        if not PRESERVE_WHITESPACE: strings = [s.strip() for s in strings]
        pad_fn = _pad_both
    elif alignment == "decimal":
        if has_invisible: decimals = [_after_point(_strip_invisible(s)) for s in strings]
        else: decimals = [_after_point(s) for s in strings]
        max_decimals = max(decimals)
        strings = [s + (max_decimals - decs) * " " for s, decs in zip(strings, decimals)]
        pad_fn = _pad_left
    elif not alignment: pad_fn = _pad_none
    else:
        if not PRESERVE_WHITESPACE: strings = [s.strip() for s in strings]
        pad_fn = _pad_right
    return strings, pad_fn


def _align_column_choose_width_fn(has_invisible, enable_wide_chars, is_multiline):
    if has_invisible: line_width_fn = _visible_width
    elif enable_wide_chars: line_width_fn = wcwidth.wcswidth
    else: line_width_fn = len
    if is_multiline: width_fn = lambda s: _align_column_multiline_width(s, line_width_fn)
    else: width_fn = line_width_fn
    return width_fn


def _align_column_multiline_width(multiline_s, line_width_fn=len):
    return list(map(line_width_fn, re.split("[\r\n]", multiline_s)))


def _flat_list(nested_list):
    ret = []
    for item in nested_list:
        if isinstance(item, list):
            for subitem in item: ret.append(subitem)
        else: ret.append(item)
    return ret


def _align_column(
    strings,
    alignment,
    min_width=0,
    has_invisible=True,
    enable_wide_chars=False,
    is_multiline=False,
):
    strings, pad_fn = _align_column_choose_pad_fn(strings, alignment, has_invisible)
    width_fn = _align_column_choose_width_fn(has_invisible, enable_wide_chars, is_multiline)

    s_widths = list(map(width_fn, strings))
    maxwidth = max(max(_flat_list(s_widths)), min_width)

    if is_multiline:
        if not enable_wide_chars and not has_invisible:
            padded_strings = [
                "\n".join([pad_fn(maxwidth, s) for s in ms.splitlines()])
                for ms in strings
            ]
        else:
            s_lens = [[len(s) for s in re.split("[\r\n]", ms)] for ms in strings]
            visible_widths = [
                [maxwidth - (w - l) for w, l in zip(mw, ml)]
                for mw, ml in zip(s_widths, s_lens)
            ]

            padded_strings = [
                "\n".join([pad_fn(w, s) for s, w in zip((ms.splitlines() or ms), mw)])
                for ms, mw in zip(strings, visible_widths)
            ]
    else:
        if not enable_wide_chars and not has_invisible: padded_strings = [pad_fn(maxwidth, s) for s in strings]
        else:
            s_lens = list(map(len, strings))
            visible_widths = [maxwidth - (w - l) for w, l in zip(s_widths, s_lens)]
            padded_strings = [pad_fn(w, s) for s, w in zip(strings, visible_widths)]
    return padded_strings


def _more_generic(type1, type2):
    types = {
        _none_type: 0,
        _bool_type: 1,
        int: 2,
        float: 3,
        _binary_type: 4,
        _text_type: 5,
    }
    inv_types = {
        5: _text_type,
        4: _binary_type,
        3: float,
        2: int,
        1: _bool_type,
        0: _none_type,
    }
    more_generic = max(types.get(type1, 5), types.get(type2, 5))
    return inv_types[more_generic]


def _column_type(strings, has_invisible=True, num_parse=True):

    types = [_type(s, has_invisible, num_parse) for s in strings]
    return reduce(_more_generic, types, _bool_type)


def _format(val, val_type, float_fmt, missingval="", has_invisible=True):

    if val is None: return missingval

    if val_type in [int, _text_type]: return "{0}".format(val)
    elif val_type is _binary_type:
        try: return _text_type(val, "ascii")
        except TypeError: return _text_type(val)
    elif val_type is float:
        is_a_colored_number = has_invisible and isinstance(
            val, (_text_type, _binary_type)
        )
        if is_a_colored_number:
            raw_val = _strip_invisible(val)
            formatted_val = format(float(raw_val), float_fmt)
            return val.replace(raw_val, formatted_val)
        else: return format(float(val), float_fmt)
    else: return "{0}".format(val)


def _align_header(
    header, alignment, width, visible_width, is_multiline=False, width_fn=None
):
    if is_multiline:
        header_lines = re.split(_multiline_codes, header)
        padded_lines = [
            _align_header(h, alignment, width, width_fn(h)) for h in header_lines
        ]
        return "\n".join(padded_lines)

    nin_visible = len(header) - visible_width
    width += nin_visible
    if alignment == "left": return _pad_right(width, header)
    elif alignment == "center": return _pad_both(width, header)
    elif not alignment: return "{0}".format(header)
    else: return _pad_left(width, header)


def _prepend_row_index(rows, index):

    if index is None or index is False: return rows
    if len(index) != len(rows):
        print("index=", index)
        print("rows=", rows)
        raise ValueError("index must be as long as the number of data rows")
    rows = [[v] + list(row) for v, row in zip(index, rows)]
    return rows


def _bool(val):
    "A wrapper around standard bool() which doesn't throw on NumPy arrays"
    try: return bool(val)
    except ValueError: return False


def _normalize_tabular_data(tabular_data, headers, show_index="default"):

    try:
        bool(headers)
        is_headers2bool_broken = False
    except ValueError:
        is_headers2bool_broken = True
        headers = list(headers)

    index = None
    if hasattr(tabular_data, "keys") and hasattr(tabular_data, "values"):

        if hasattr(tabular_data.values, "__call__"):

            keys = tabular_data.keys()
            rows = list(
                izip_longest(*tabular_data.values())
            )
        elif hasattr(tabular_data, "index"):

            keys = list(tabular_data)
            if (
                show_index in ["default", "always", True]
                and tabular_data.index.name is not None
            ):
                if isinstance(tabular_data.index.name, list): keys[:0] = tabular_data.index.name
                else: keys[:0] = [tabular_data.index.name]
            vals = tabular_data.values

            index = list(tabular_data.index)
            rows = [list(row) for row in vals]
        else: raise ValueError("tabular data doesn't appear to be a dict or a DataFrame")

        if headers == "keys": headers = list(map(_text_type, keys))

    else:
        rows = list(tabular_data)

        if headers == "keys" and not rows:

            headers = []
        elif (
            headers == "keys"
            and hasattr(tabular_data, "dtype")
            and getattr(tabular_data.dtype, "names")
        ):

            headers = tabular_data.dtype.names
        elif (
            headers == "keys"
            and len(rows) > 0
            and isinstance(rows[0], tuple)
            and hasattr(rows[0], "_fields")
        ): headers = list(map(_text_type, rows[0]._fields))

        elif len(rows) > 0 and hasattr(rows[0], "keys") and hasattr(rows[0], "values"):

            uniq_keys = set()
            keys = []
            if headers == "firstrow":
                first_dict = rows[0] if len(rows) > 0 else {}
                keys.extend(first_dict.keys())
                uniq_keys.update(keys)
                rows = rows[1:]
            for row in rows:
                for k in row.keys():

                    if k not in uniq_keys:
                        keys.append(k)
                        uniq_keys.add(k)
            if headers == "keys": headers = keys
            elif isinstance(headers, dict):

                headers = [headers.get(k, k) for k in keys]
                headers = list(map(_text_type, headers))
            elif headers == "firstrow":
                if len(rows) > 0:
                    headers = [first_dict.get(k, k) for k in keys]
                    headers = list(map(_text_type, headers))
                else: headers = []
            elif headers:
                raise ValueError(
                    "headers for a list of dicts is not a dict or a keyword"
                )
            rows = [[row.get(k) for k in keys] for row in rows]

        elif (
            headers == "keys"
            and hasattr(tabular_data, "description")
            and hasattr(tabular_data, "fetchone")
            and hasattr(tabular_data, "rowcount")):


            headers = [column[0] for column in tabular_data.description]

        elif headers == "keys" and len(rows) > 0: headers = list(map(_text_type, range(len(rows[0]))))


    if headers == "firstrow" and len(rows) > 0:
        if index is not None:
            headers = [index[0]] + list(rows[0])
            index = index[1:]
        else: headers = rows[0]
        headers = list(map(_text_type, headers))
        rows = rows[1:]

    headers = list(map(_text_type, headers))
    rows = list(map(list, rows))


    show_index_is_a_str = type(show_index) in [_text_type, _binary_type]
    if show_index == "default" and index is not None: rows = _prepend_row_index(rows, index)
    elif isinstance(show_index, Iterable) and not show_index_is_a_str: rows = _prepend_row_index(rows, list(show_index))
    elif show_index == "always" or (_bool(show_index) and not show_index_is_a_str):
        if index is None: index = list(range(len(rows)))
        rows = _prepend_row_index(rows, index)
    elif show_index == "never" or (not _bool(show_index) and not show_index_is_a_str): pass


    if headers and len(rows) > 0:
        nhs = len(headers)
        n_cols = len(rows[0])
        if nhs < n_cols: headers = [""] * (n_cols - nhs) + headers

    return rows, headers


def tabulate(
    tabular_data,
    headers=(),
    tablefmt="simple",
    float_fmt=_DEFAULT_FLOAT_FMT,
    num_align=_DEFAULT_ALIGN,
    str_align=_DEFAULT_ALIGN,
    missingval=_DEFAULT_MISSINGVAL,
    show_index="default",
    disable_num_parse=False,
    col_align=None,
):

    if tabular_data is None: tabular_data = []
    list_of_lists, headers = _normalize_tabular_data(
        tabular_data, headers, show_index=show_index
    )

    if tablefmt == "rst": list_of_lists, headers = _rst_escape_first_column(list_of_lists, headers)





    min_padding = MIN_PADDING
    if tablefmt == "pretty":
        min_padding = 0
        disable_num_parse = True
        num_align = "center" if num_align == _DEFAULT_ALIGN else num_align
        str_align = "center" if str_align == _DEFAULT_ALIGN else str_align
    else:
        num_align = "decimal" if num_align == _DEFAULT_ALIGN else num_align
        str_align = "left" if str_align == _DEFAULT_ALIGN else str_align



    plain_text = "\t".join(
        ["\t".join(map(_text_type, headers))]
        + ["\t".join(map(_text_type, row)) for row in list_of_lists]
    )

    has_invisible = re.search(_invisible_codes, plain_text)
    if not has_invisible: has_invisible = re.search(_invisible_codes_link, plain_text)
    enable_wide_chars = wcwidth is not None and WIDE_CHARS_MODE
    if (
        not isinstance(tablefmt, TableFormat)
        and tablefmt in multiline_formats
        and _is_multiline(plain_text)
    ):
        tablefmt = multiline_formats.get(tablefmt, tablefmt)
        is_multiline = True
    else: is_multiline = False
    width_fn = _choose_width_fn(has_invisible, enable_wide_chars, is_multiline)


    cols = list(izip_longest(*list_of_lists))
    num_parses = _expand_num_parse(disable_num_parse, len(cols))
    col_types = [_column_type(col, num_parse=np) for col, np in zip(cols, num_parses)]
    if isinstance(float_fmt, basestring):
        float_formats = len(cols) * [
            float_fmt
        ]
    else:
        float_formats = list(float_fmt)
        if len(float_formats) < len(cols): float_formats.extend((len(cols) - len(float_formats)) * [_DEFAULT_FLOAT_FMT])
    if isinstance(missingval, basestring): missing_vals = len(cols) * [missingval]
    else:
        missing_vals = list(missingval)
        if len(missing_vals) < len(cols): missing_vals.extend((len(cols) - len(missing_vals)) * [_DEFAULT_MISSINGVAL])
    cols = [
        [_format(v, ct, fl_fmt, miss_v, has_invisible) for v in c]
        for c, ct, fl_fmt, miss_v in zip(cols, col_types, float_formats, missing_vals)
    ]


    aligns = [num_align if ct in [int, float] else str_align for ct in col_types]
    if col_align is not None:
        assert isinstance(col_align, Iterable)
        for idx, align in enumerate(col_align): aligns[idx] = align
    min_widths = (
        [width_fn(h) + min_padding for h in headers] if headers else [0] * len(cols)
    )
    cols = [
        _align_column(c, a, minw, has_invisible, enable_wide_chars, is_multiline)
        for c, a, minw in zip(cols, aligns, min_widths)
    ]

    if headers:

        t_cols = cols or [[""]] * len(headers)
        t_aligns = aligns or [str_align] * len(headers)
        min_widths = [
            max(minw, max(width_fn(cl) for cl in c))
            for minw, c in zip(min_widths, t_cols)
        ]
        headers = [
            _align_header(h, a, minw, width_fn(h), is_multiline, width_fn)
            for h, a, minw in zip(headers, t_aligns, min_widths)
        ]
        rows = list(zip(*cols))
    else:
        min_widths = [max(width_fn(cl) for cl in c) for c in cols]
        rows = list(zip(*cols))

    if not isinstance(tablefmt, TableFormat): tablefmt = _table_formats.get(tablefmt, _table_formats["simple"])

    return _format_table(tablefmt, headers, rows, min_widths, aligns, is_multiline)


def _expand_num_parse(disable_num_parse, column_count):
    if isinstance(disable_num_parse, Iterable):
        numparses = [True] * column_count
        for index in disable_num_parse:
            numparses[index] = False
        return numparses
    else:
        return [not disable_num_parse] * column_count


def _pad_row(cells, padding):
    if cells:
        pad = " " * padding
        padded_cells = [pad + cell + pad for cell in cells]
        return padded_cells
    else: return cells


def _build_simple_row(padded_cells, row_fmt):
    "Format row according to DataRow format without padding."
    begin, sep, end = row_fmt
    return (begin + sep.join(padded_cells) + end).rstrip()


def _build_row(padded_cells, col_widths, col_aligns, row_fmt):
    "Return a string which represents a row of data cells."
    if not row_fmt: return None
    if hasattr(row_fmt, "__call__"): return row_fmt(padded_cells, col_widths, col_aligns)
    else: return _build_simple_row(padded_cells, row_fmt)


def _append_basic_row(lines, padded_cells, col_widths, col_aligns, row_fmt):
    lines.append(_build_row(padded_cells, col_widths, col_aligns, row_fmt))
    return lines


def _append_multiline_row(
    lines, padded_multiline_cells, padded_widths, col_aligns, row_fmt, pad
):
    col_widths = [w - 2 * pad for w in padded_widths]
    cells_lines = [c.splitlines() for c in padded_multiline_cells]
    nlines = max(map(len, cells_lines))

    cells_lines = [
        (cl + [" " * w] * (nlines - len(cl))) for cl, w in zip(cells_lines, col_widths)
    ]
    lines_cells = [[cl[i] for cl in cells_lines] for i in range(nlines)]
    for ln in lines_cells:
        padded_ln = _pad_row(ln, pad)
        _append_basic_row(lines, padded_ln, col_widths, col_aligns, row_fmt)
    return lines


def _build_line(col_widths, col_aligns, line_fmt):
    "Return a string which represents a horizontal line."
    if not line_fmt: return None
    if hasattr(line_fmt, "__call__"): return line_fmt(col_widths, col_aligns)
    else:
        begin, fill, sep, end = line_fmt
        cells = [fill * w for w in col_widths]
        return _build_simple_row(cells, (begin, sep, end))


def _append_line(lines, col_widths, col_aligns, line_fmt):
    lines.append(_build_line(col_widths, col_aligns, line_fmt))
    return lines


class JupyterHTMLStr(str):

    def _repr_html_(self): return self

    @property
    def str(self): return self


def _format_table(fmt, headers, rows, col_widths, col_aligns, is_multiline):
    lines = []
    hidden = fmt.with_header_hide if (headers and fmt.with_header_hide) else []
    pad = fmt.padding
    headerrow = fmt.headerrow

    padded_widths = [(w + 2 * pad) for w in col_widths]
    if is_multiline:
        pad_row = lambda row, _: row  # noqa do it later, in _append_multiline_row
        append_row = partial(_append_multiline_row, pad=pad)
    else:
        pad_row = _pad_row
        append_row = _append_basic_row

    padded_headers = pad_row(headers, pad)
    padded_rows = [pad_row(row, pad) for row in rows]

    if fmt.lineabove and "lineabove" not in hidden: _append_line(lines, padded_widths, col_aligns, fmt.lineabove)

    if padded_headers:
        append_row(lines, padded_headers, padded_widths, col_aligns, headerrow)
        if fmt.linebelowheader and "linebelowheader" not in hidden: _append_line(lines, padded_widths, col_aligns, fmt.linebelowheader)

    if padded_rows and fmt.linebetweenrows and "linebetweenrows" not in hidden:
        for row in padded_rows[:-1]:
            append_row(lines, row, padded_widths, col_aligns, fmt.datarow)
            _append_line(lines, padded_widths, col_aligns, fmt.linebetweenrows)
        append_row(lines, padded_rows[-1], padded_widths, col_aligns, fmt.datarow)
    else:
        for row in padded_rows: append_row(lines, row, padded_widths, col_aligns, fmt.datarow)

    if fmt.linebelow and "linebelow" not in hidden: _append_line(lines, padded_widths, col_aligns, fmt.linebelow)

    if headers or rows:
        output = "\n".join(lines)
        if fmt.lineabove == _html_begin_table_without_header: return JupyterHTMLStr(output)
        else: return output
    else: return ""


def _main():
    import getopt
    import sys
    import textwrap

    usage = textwrap.dedent(_main.__doc__)
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "h1o:s:F:A:f:",
            ["help", "header", "output", "sep=", "float=", "align=", "format="],
        )
    except getopt.GetoptError as e:
        print(e)
        print(usage)
        sys.exit(2)
    headers = []
    float_fmt = _DEFAULT_FLOAT_FMT
    col_align = None
    tablefmt = "simple"
    sep = r"\s+"
    outfile = "-"
    for opt, value in opts:
        if opt in ["-1", "--header"]: headers = "firstrow"
        elif opt in ["-o", "--output"]: outfile = value
        elif opt in ["-F", "--float"]: float_fmt = value
        elif opt in ["-C", "--colalign"]: col_align = value.split()
        elif opt in ["-f", "--format"]:
            if value not in tabulate_formats:
                print("%s is not a supported table format" % value)
                print(usage)
                sys.exit(3)
            tablefmt = value
        elif opt in ["-s", "--sep"]: sep = value
        elif opt in ["-h", "--help"]:
            print(usage)
            sys.exit(0)
    files = [sys.stdin] if not args else args
    with (sys.stdout if outfile == "-" else open(outfile, "w")) as out:
        for f in files:
            if f == "-": f = sys.stdin
            if _is_file(f):
                _pprint_file(
                    f,
                    headers=headers,
                    tablefmt=tablefmt,
                    sep=sep,
                    float_fmt=float_fmt,
                    file=out,
                    col_align=col_align,
                )
            else:
                with open(f) as fobj:
                    _pprint_file(
                        fobj,
                        headers=headers,
                        tablefmt=tablefmt,
                        sep=sep,
                        float_fmt=float_fmt,
                        file=out,
                        col_align=col_align,
                    )


def _pprint_file(f_object, headers, tablefmt, sep, float_fmt, file, col_align):
    rows = f_object.readlines()
    table = [re.split(sep, r.rstrip()) for r in rows if r.strip()]
    print(
        tabulate(table, headers, tablefmt, float_fmt=float_fmt, col_align=col_align),
        file=file,
    )


if __name__ == "__main__": _main()
