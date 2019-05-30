# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

import os
import shutil
import sys
from pathlib import Path
from subprocess import check_call
from tempfile import TemporaryDirectory

from . import DIST, PLATFORM, PY, TEST_DIR, TEST_OUT, run

BROWSER = os.environ.get("BROWSER", "headlessfirefox")

XUNIT = TEST_OUT / "xunit"
COV = TEST_OUT / "cov"
PY_SRC = ["src", "setup.py", "scripts", "docs"]
RF_SRC = [os.path.join("atest", "resources"), os.path.join("atest", "acceptance")]


def lint(targets=[]):
    if PLATFORM == "windows":
        return 0

    if not targets or "copyright" in targets:
        check_call([sys.executable, "-m", "scripts.copyright"])

    if not targets or "py" in targets:
        check_call(["isort", "-rc"] + PY_SRC)
        check_call(["black"] + PY_SRC)
        check_call(["flake8"] + PY_SRC)

    if not targets or "robot" in targets:
        for src in RF_SRC:
            check_call(["python", "-m", "robot.tidy", "-r", src])
            check_call(
                [
                    "rflint",
                    "--configure",
                    "TooManyTestSteps:200",
                    "--configure",
                    "TooFewKeywordSteps:0",
                    "--configure",
                    "LineTooLong:200",
                    src,
                ]
            )

    if not targets or "ipynb" in targets:
        from nbformat import NO_CONVERT, read, write

        for nbp in (Path(__file__).parent.parent / "docs").rglob("*.ipynb"):
            nbf = read(str(nbp), NO_CONVERT)
            changed = False
            for cell in nbf.cells:
                if cell.cell_type == "code":
                    if cell.outputs:
                        cell.outputs = []
                        changed = True
                    if cell.execution_count:
                        cell.execution_count = None
                        changed = True
            if changed:
                print(f"Overwriting {nbp}")
                write(nbf, str(nbp))

    if not targets or "js" in targets:
        check_call(["jlpm"])
        check_call(["jlpm", "lint"])

    return 0


def unit(pytest_args):
    attempts = 3 if PY == "37" and PLATFORM == "windows" else 1
    for i in range(attempts):
        rc = run(
            [
                "pytest",
                "--cov-report",
                f"xml:{COV / PLATFORM}.{PY}.py.xml",
                "--cov-report",
                f"html:{COV / PLATFORM}.{PY}",
                "--junitxml",
                f"{XUNIT / PLATFORM}.{PY}.py.xml",
            ]
            + list(pytest_args)
        )
        if rc == 0:
            break
    return rc


def acceptance(robot_args):
    import chromedriver_binary  # noqa

    global BROWSER
    env = dict(**os.environ)

    with TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "home").mkdir()
        shutil.copytree(DIST / "lab", tdp / "lab")

        if "--browser" in robot_args:
            browser_index = robot_args.index("--browser")
            BROWSER = robot_args[browser_index + 1]
            robot_args.remove("--browser")
            robot_args.remove(BROWSER)
            os.environ["BROWSER"] = BROWSER

        env.update(
            PATH=os.pathsep.join(
                [os.path.dirname(chromedriver_binary.__file__), os.environ["PATH"]]
            ),
            JUPYTERLAB_DIR=str(tdp / "lab"),
            JUPYTERLAB_SETTINGS_DIR=str(tdp / "lab" / "settings"),
            JUPYTERLAB_WORKSPACES_DIR=str(tdp / "lab" / "workspaces"),
            HOME=str(tdp / "home"),
        )

        robot_out = TEST_OUT / "robot"
        out_dir = robot_out / PLATFORM / BROWSER / PY
        out_dir.mkdir(parents=True, exist_ok=True)

        args = (
            [
                sys.executable,
                "-m",
                "robot",
                "--name",
                f"{BROWSER} on {PLATFORM} on {PY}",
                "--outputdir",
                out_dir,
                "--output",
                f"{robot_out / PLATFORM}.{BROWSER}.{PY}.xml",
                "--log",
                f"{robot_out / PLATFORM}.{BROWSER}.{PY}.log.html",
                "--report",
                f"{robot_out / PLATFORM}.{BROWSER}.{PY}.report.html",
                "--xunit",
                f"""{XUNIT / PLATFORM}.{BROWSER}.{PY}.robot.xml""",
                "--variable",
                f"OS:{PLATFORM}",
                "--variable",
                f"BROWSER:{BROWSER}",
                "--variable",
                f"PY:{PY}",
                "--exclude",
                f"""skip:{BROWSER.replace("headless", "")}""",
                "--exclude",
                f"""skip:{PLATFORM}""",
            ]
            + list(robot_args)
            + [str(TEST_DIR)]
        )
        return run(args, env=env)


def combine(rebot_args):
    args = (
        [
            "python",
            "-m",
            "robot.rebot",
            "--name",
            "IRobotFramework",
            "--outputdir",
            str(TEST_OUT / "robot"),
            "--output",
            "index.xml",
        ]
        + rebot_args
        + list(map(str, (TEST_OUT / "robot").glob("*.xml")))
    )

    return run(args)


TESTS = [
    [lint, []],
    [unit, []],
    [acceptance, ["--browser", "headlessfirefox"]],
    [acceptance, ["--browser", "headlesschrome"]],
    [combine, []],
]

if __name__ == "__main__":
    rc = 0
    args = list(sys.argv[1:])
    if not args:
        TEST_OUT.exists() and shutil.rmtree(TEST_OUT)

        for test, extra_args in TESTS:
            rc = test(extra_args) or rc
            if "-x" in args:
                if rc != 0:
                    break
    elif args[0] in ["lint", "l"]:
        rc = lint(args[1:])
    elif args[0] in ["unit", "u"]:
        rc = unit(args[1:])
    elif args[0] in ["acceptance", "a"]:
        rc = acceptance(args[1:])
    elif args[0] in ["combine", "c"]:
        rc = combine(args[1:])

    sys.exit(rc)
