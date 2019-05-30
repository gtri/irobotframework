# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import json
import sys

from . import HISTORY, PACKAGES, ROOT, VERSIONS


def release_check(version):
    """ Is the current version ready to be tagged?
    """
    print(f"\n*** READY TO RELEASE {version}? ***\n")

    version_comp = f"""__version__ = "{version}" """.strip()
    history_comp = f"""## {version}"""

    outdated = []

    for package in PACKAGES:
        print(f"- {package.relative_to(ROOT)}...")
        if json.loads(package.read_text(encoding="utf-8"))["version"] != version:
            print(f"""  - NOPE""")
            outdated += [package]

    for py_version in VERSIONS:
        print(f"- {py_version.relative_to(ROOT)}...")
        if version_comp not in py_version.read_text(encoding="utf-8"):
            print(f"""  - NOPE""")
            outdated += [py_version]

    print(f"- {HISTORY.relative_to(ROOT)}...")
    if history_comp not in HISTORY.read_text(encoding="utf-8"):
        print(f"""  - NOPE""")
        outdated += [HISTORY]

    if outdated:
        print(f"""\n*** NO, THERE ARE {len(outdated)} OUTDATED FILES ***""")
        for out in outdated:
            print(f"""  - {out.relative_to(ROOT)}""")
    else:
        print(f"""\n*** YES, RELEASE THE {version} ***\n""")

    return len(outdated)


if __name__ == "__main__":
    sys.exit(release_check(sys.argv[1]))
