# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import re
import sys
import subprocess

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


def build_tree():
    ug = html.parse(str(UG_DOC))

    els = [el for el in ug.xpath("//*[@class='highlight']") if is_robot_src(el)]

    tree = {}

    for el in els:
        pel = el.xpath("preceding::*[self::p]")[-1]
        h3 = el.xpath("preceding::*[self::h3]")[-1]
        slug = re.sub(
            r"[^a-z0-9]", "_", "_".join(pel.text_content().lower().split(" ")[0:6])
        )
        tree.setdefault(h3.text_content().split("\xa0")[0], {}).setdefault(
            slug, []
        ).append(el.text_content())

    return tree


def write_fixtures(tree):
    robot_lines = []

    for section, slugs in tree.items():
        section_dir = FIXTURES / "highlighting" / "samples" / "rfug" / section
        section_dir.mkdir(exist_ok=True, parents=True)
        for slug, contents in slugs.items():
            for i, content in enumerate(contents):
                out_file = section_dir / f"{slug}__{i}.robot"
                out_file.write_text(content)
                robot_lines += [
                    str(out_file.relative_to(section_dir.parent.parent))
                    .replace(".robot", "")
                    .replace("/", "${/}")
                ]

    return robot_lines


def rfug_fixtures():
    if not ROBOT.exists():
        subprocess.check_call(["git", "submodule", "update", "--init"], cwd=str(ROOT))
    subprocess.check_call(["python", "ug2html.py", "create"], cwd=str(UG))

    tree = build_tree()
    lines = write_fixtures(tree)
    print("\n".join(lines))

    return 0


if __name__ == "__main__":
    sys.exit(rfug_fixtures())
