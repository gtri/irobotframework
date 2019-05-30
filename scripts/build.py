# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import shutil
import sys
import tarfile
import tempfile
from pathlib import Path

from . import DIST, PACKAGE, ROOT, run


def sdist(sdist_args):
    """ Build the source distribution
    """
    rc = run(["python", "setup.py", "clean"])
    if rc != 0:
        return rc
    return run(["python", "setup.py", "sdist", "--dist-dir", DIST / "pip"] + sdist_args)


def wheel(wheel_args):
    """ Build the wheel
    """
    rc = run(["python", "setup.py", "clean"])
    if rc != 0:
        return rc
    return run(
        ["python", "setup.py", "bdist_wheel", "--dist-dir", DIST / "pip"] + wheel_args
    )


def lerna(lerna_args):
    """ Build the lerna packages
    """
    return run(["jlpm", "build"] + lerna_args)


def npm(npm_args):
    """ pack up the extensions
    """
    src_dirs = sum([list(ROOT.glob(ws)) for ws in PACKAGE["workspaces"]], [])
    out_dir = DIST / "npm"

    rc = run(["jlpm", "npm:pack"])

    if rc != 0:
        return rc

    out_dir.exists() and shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for src_dir in src_dirs:
        for tgz in src_dir.glob("*.tgz"):
            tgz.rename(out_dir / tgz.name)

    return 0


def jupyterlab(extra_args):
    """ build a jupyterlab
    """
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)

        lab_dir = tdp / "lab"
        ext_dir = lab_dir / "extensions"
        ext_dir.mkdir(parents=True)
        ext = list((DIST / "npm").glob("*.tgz"))[0]
        shutil.copy(ext, ext_dir)

        rc = run(["jupyter", "lab", "build", "--app-dir", lab_dir])
        if rc != 0:
            return rc

        lab_out = DIST / "lab"
        lab_out.exists() and shutil.rmtree(lab_out)
        lab_out.mkdir()

        with tarfile.open(lab_out / "lab.tar.gz", "w:gz") as tarball:
            for path in ["static", "themes", "schemas", "extensions"]:
                tarball.add(lab_dir / path, arcname=path)

        with tarfile.open(lab_out / "lab.tar.gz", "r") as tarball:
            tarball.extractall(lab_out)


def docs(extra_args):
    """ build the docs
    """
    try:
        import sphinx

        print(sphinx.__version__)
    except Exception as error:
        print(error)
        print("skipping docs build, run in `--env-spec docs`")
        return 0
    return run(["sphinx-build", ROOT / "docs", DIST / "docs"])


BUILDS = [
    [sdist, []],
    [wheel, []],
    [lerna, []],
    [npm, []],
    [jupyterlab, []],
    [docs, []],
]


if __name__ == "__main__":
    rc = 0
    args = list(sys.argv[1:])
    if not args:
        DIST.exists() and shutil.rmtree(DIST)

        for test, extra_args in BUILDS:
            rc = test(extra_args) or rc
            if "-x" in args:
                if rc != 0:
                    break
    elif args[0] in ["sdist", "s"]:
        rc = sdist(args[1:])
    elif args[0] in ["wheel", "w"]:
        rc = wheel(args[1:])
    elif args[0] in ["npm", "n"]:
        rc = npm(args[1:])
    elif args[0] in ["lerna", "l"]:
        rc = lerna(args[1:])
    elif args[0] in ["jupyterlab", "j"]:
        rc = jupyterlab(args[1:])
    elif args[0] in ["docs", "d"]:
        rc = docs(args[1:])

    sys.exit(rc)
