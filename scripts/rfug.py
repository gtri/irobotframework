# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import re
import sys
import subprocess
from hashlib import sha256

from lxml import html

from . import ROOT, VENDOR, FIXTURES


ROBOT = VENDOR / "robotframework"
UG = ROBOT / "doc" / "userguide"
UG_DOC = UG / "RobotFrameworkUserGuide.html"


def is_robot_src(el):
    txt = el.text_content()
    if ".. code::" in txt:
        return False
    return re.findall(
        r"\*\s*(setting|test case|task|keyword|variable)s?",
        el.text_content(),
        flags=re.I,
    )


def build_hashes():
    ug = html.parse(str(UG_DOC))

    return {
        sha256(el.text_content().encode("utf-8")).hexdigest(): el.text_content()
        for el in
        [el for el in ug.xpath("//*[@class='highlight']") if is_robot_src(el)]
    }


def write_fixtures(hashes):
    robot_lines = []

    for sha, txt in sorted(hashes.items()):
        out_file = FIXTURES / "highlighting" / "samples" / "rfug" / f"{sha}.robot"
        out_file.write_text(txt)
        robot_lines += [
            str(out_file.relative_to(out_file.parent.parent))
            .replace(".robot", "")
            .replace("/", "${/}")
        ]

    return robot_lines


def rfug_fixtures():
    if not ROBOT.exists():
        subprocess.check_call(["git", "submodule", "update", "--init"], cwd=str(ROOT))
    subprocess.check_call(["python", "ug2html.py", "create"], cwd=str(UG))

    hashes = build_hashes()
    lines = write_fixtures(hashes)
    print("\n".join(lines))

    return 0


if __name__ == "__main__":
    sys.exit(rfug_fixtures())
