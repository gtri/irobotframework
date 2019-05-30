# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

""" Documentation-related features for irobotframework
"""
import sys

import ipykernel
import IPython
import robot
from robot.libraries import STDLIBS

from ._version import __version__
from .util import url_path_join as ujoin

HAS_NO_DOC = ["Remote"]
PY_DOCS = "https://docs.python.org/%i.%i" % sys.version_info[:2]
IPYTHON_DOCS = "https://ipython.readthedocs.io/"
ROBOT_DOCS = "http://robotframework.org/robotframework/{}/".format(robot.__version__)


def banner():
    """ Banner for interactive consoles and about
    """
    return " » ".join(
        [
            f"Robot Framework Kernel [{__version__}]",
            f"Robot Framework [{robot.__version__}]",
            f"ipykernel [{ipykernel.__version__}]",
            f"IPython [{IPython.__version__}]",
            f"Python [{sys.version}]",
        ]
    )


def help_links():
    """ Help links to show in frontends
    """
    return [
        {"text": "Python Reference", "url": PY_DOCS},
        {"text": "IPython Reference", "url": IPYTHON_DOCS},
        {
            "text": "Robot Framework: User Guide",
            "url": ujoin(ROBOT_DOCS, "RobotFrameworkUserGuide.html"),
        },
        *[
            {
                "text": f"{lib} — Robot Framework",
                "url": ujoin(ROBOT_DOCS, "libraries", f"{lib}.html"),
            }
            for lib in sorted(STDLIBS)
            if lib not in HAS_NO_DOC
        ],
    ]
