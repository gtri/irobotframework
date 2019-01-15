# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

# Derived from robotkernel
# Copyright (c) 2018, Asko Soukka
# Distributed under the terms of the BSD-3-Clause License


""" A collection of things for dealing with formats and data URIs
"""
from base64 import b64encode
from traceback import format_exc
from typing import Tuple

from IPython.utils.tokenutil import line_at_cursor


def javascript_uri(html):
    """ Because data-uri for text/html is not supported by IE
    """
    if isinstance(html, str):
        html = html.encode("utf-8")
    return (
        "javascript:(function(){{"
        "var w=window.open();"
        "w.document.open();"
        "w.document.write(window.atob('{}'));"
        "w.document.close();"
        '}})();" '.format(b64encode(html).decode("utf-8"))
    )


def data_uri(mimetype, data):
    """ Base64 encode some stuff
    """
    return "data:{};base64,{}".format(mimetype, b64encode(data).decode("utf-8"))


def format_error(error):
    """ Wrap up an exception with kernel message spec fields
    """
    return {
        "ename": error.__class__.__name__,
        "evalue": str(error),
        "traceback": list(format_exc().splitlines()),
    }


# From https://github.com/jupyter/notebook/blob/master/notebook/utils.py
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
def url_path_join(*pieces):  # pragma: no cover
    """Join components of url into a relative url
    Use to prevent double slash when joining subpath. This will leave the
    initial and final / in place
    """
    initial = pieces[0].startswith("/")
    final = pieces[-1].endswith("/")
    stripped = [s.strip("/") for s in pieces]
    result = "/".join(s for s in stripped if s)
    if initial:
        result = "/" + result
    if final:
        result = result + "/"
    if result == "//":
        result = "/"
    return result


def find_line(code: str, cursor_pos: int) -> Tuple[str, int, int]:
    """ What is the full line, line_cursor and offset at the cursor position
        in a multi-line string?
    """
    if cursor_pos is None:
        cursor_pos = len(code)
    line, offset = line_at_cursor(code, cursor_pos)
    line_cursor = cursor_pos - offset
    return line, line_cursor, offset
