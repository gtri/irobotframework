# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

""" The irobotframework public API
"""

from ._version import __version__  # noqa

from .magic.robot import register_robot_cell_magic, unregister_robot_cell_magic
from .completer import (
    register_robot_completion_finder,
    unregister_robot_completion_finder,
)


__all__ = [
    "load_ipython_extension",
    "register_robot_cell_magic",
    "unregister_robot_cell_magic",
    "register_robot_completion_finder",
    "unregister_robot_completion_finder",
]


def load_ipython_extension(ipython):
    """ load and register the %%robot magic
    """
    from .magic.ipython import RobotMagic

    ipython.register_magics(RobotMagic)
