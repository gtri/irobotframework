# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import re
from typing import Callable, Text

from ipykernel.ipkernel import IPythonKernel
from IPython import get_ipython
from tornado.concurrent import Future

from .. import patches
from ..irobot import StringTidy

__all__ = ["register_robot_cell_magic", "default_robot_cell_magics"]


# pattern for matching the `%%python module` magic
PY_MAGIC_RE = re.compile(
    r"^%%python\s*module\s*(?P<name>[a-zA-Z_][a-zA-Z_\d]*)\s*\n(?P<body>.*)$", re.S
)
# pattern for matching the `%%tidy` magic
TIDY_MAGIC_RE = re.compile(r"^%%tidy\s*\n(?P<body>.*)$", re.S)
# pattern for cleaning weird test/tasks
TIDY_WEIRD = re.compile(r"^\|?\s*\*+\s*(test case|task)s?\s*\*+\|?", re.I | re.M)


def default_robot_cell_magics():
    """ The default cell magics
    """
    return {
        "python module": dict(pattern=PY_MAGIC_RE, func=cell_magic_python_module),
        "tidy": dict(pattern=TIDY_MAGIC_RE, func=cell_magic_tidy),
    }


def register_robot_cell_magic(name: Text, pattern: Text, func: Callable):
    """ Add a robot cell magic. the func is a callable with a notional arg spec
        of:

            def magic_function(code,
                               silent=silent,
                               store_history=store_history,
                               user_expressions=user_expressions,
                               allow_stdin=allow_stdin,)

       it may return:
       - an execute_response dict
       - a string of the robot code to be executed
    """
    kernel = get_ipython().kernel
    kernel.robot_magics["cell"][name] = {"pattern": pattern, "func": func}


def unregister_robot_cell_magic(name: Text):
    """ Remove a robot cell magic
    """
    kernel = get_ipython().kernel
    kernel.robot_magics["cell"].pop(name, None)


def cell_magic_python_module(code, **kwargs):
    """ the %%python module cell magic
    """
    kernel = get_ipython().kernel
    match = re.match(PY_MAGIC_RE, code.strip())
    groups = match.groupdict()

    with patches.ScopedCodeRunner(kernel.shell, groups["name"]):
        result = IPythonKernel.do_execute(kernel, groups["body"], **kwargs)

        if isinstance(result, Future):
            result = result.result()

        return result


def cell_magic_tidy(code, **kwargs):
    """ Use robot's tidy to normalize cell content
    """
    match = re.match(TIDY_MAGIC_RE, code.strip())
    groups = match.groupdict()
    tidied = StringTidy().file(groups["body"])

    # seems to always inject an empty test case table
    if re.match(TIDY_WEIRD, groups["body"]) is None:
        tidied = re.sub(TIDY_WEIRD, "", tidied).strip()

    return dict(
        status="ok", payload=[dict(source="set_next_input", text=tidied, replace=True)]
    )
