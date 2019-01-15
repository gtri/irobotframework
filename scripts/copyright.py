# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import re
import sys

from . import SRC, YEAR, COPYRIGHT_RE, PY_HEADER, WEB_HEADER, SCRIPTS, DOCS


def update_patterns(root, patterns, header, ignores=None) -> int:
    """ Check files for copyright patterns, and apply new ones if necessary

        Probably should run this on a clean commit
    """
    ignores = ignores or []

    errors = 0
    for pattern in patterns:
        for path in root.rglob(pattern):
            rel = path.relative_to(root)
            ignored = False
            for ignore in ignores:
                if ignore in str(path):
                    print(f"skip    {rel} ({ignore})")
                    ignored = True
            if ignored:
                continue

            txt = path.read_text()

            years = re.findall(COPYRIGHT_RE, txt)

            if len(years) == 1:
                print(f"""ok      {rel} {" - ".join(years[0])}""")
                continue

            if not years:
                path.write_text(header + txt)
                print(f"update {rel} {YEAR}")
                continue
            else:
                errors += 1
                print(f"ERROR   {rel} (multiple copyrights found)")
    return errors


def main():
    """ apply several kinds of header updaters
    """
    errors = 0
    errors += update_patterns(SRC, ["*.py"], PY_HEADER)
    errors += update_patterns(SCRIPTS, ["*.py"], PY_HEADER)
    errors += update_patterns(DOCS, ["*.py"], PY_HEADER)
    errors += update_patterns(
        SRC, ["*.ts", "*.css"], WEB_HEADER, ["node_modules", "codemirror", "lib"]
    )
    return errors


if __name__ == "__main__":
    sys.exit(main())
