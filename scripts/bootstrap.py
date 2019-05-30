# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import sys

from . import DIST, ROOT, run

RES = ROOT / "src" / "irobotframework" / "resources"
PIP = DIST / "pip"

PIP_ARGS = "pip install --ignore-installed --no-deps --no-cache-dir"

COMMANDS = dict(
    js="jlpm bootstrap",
    lint="python -m scripts.test lint",
    build="python -m scripts.build",
    sdist=lambda: f"{PIP_ARGS} {sdist()}",
    wheel=lambda: f"{PIP_ARGS} {wheel()}",
    dev=f"{PIP_ARGS} -e .",
    kernel=f"jupyter kernelspec install --name robotframework --sys-prefix {RES}",
    test="python -m scripts.test",
)


def sdist():
    return list(PIP.glob("*.tar.gz"))[0].resolve()


def wheel():
    return list(PIP.glob("*.whl"))[0].resolve()


def bootstrap(steps):
    rc = 1

    for name, cmd in COMMANDS.items():
        if steps and name not in steps:
            continue
        if not isinstance(cmd, str):
            cmd = cmd()
        rc = run(cmd.split(" "))
        if rc != 0:
            break

    return rc


if __name__ == "__main__":
    sys.exit(bootstrap(sys.argv[1:]))
