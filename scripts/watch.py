# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import sys

from . import DIST, ROOT, run


def docs(extra_args):
    return run(["sphinx-autobuild", "-b", "html", ROOT / "docs", DIST / "docs"])


WATCHES = [[docs, []]]


if __name__ == "__main__":
    rc = 0
    args = list(sys.argv[1:])
    if not args:
        for watch, extra_args in WATCHES:
            rc = watch(extra_args) or rc
            if "-x" in args:
                if rc != 0:
                    break
    elif args[0] in ["docs", "d"]:
        rc = docs(args[1:])

    sys.exit(rc)
