# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

""" Completion implementations
"""

# pylint: disable=W0613,C0330,R0913,W0703,R0914

import re
from typing import List, Tuple

from IPython.core.completerlib import get_root_modules
from robot.libraries import STDLIBS
from robot.parsing.datarow import DataRow
from robot.parsing.robotreader import RobotReader

from .completer import Completer

TABLE_NAMES = ["Keywords", "Settings", "Tasks", "Test Cases", "Variables"]


TABLE_NAMES = ["Keywords", "Settings", "Tasks", "Test Cases", "Variables"]
RE_TABLE_NAME = (
    r"^\*+ *(?P<name>settings?|(user )?keywords?|test cases?|variables?|tasks?) *\*+$"
)
RE_SEP = r"\|| {2,}|\t"
DEFAULT_SEP = "    "

SUITE_SETTINGS = [
    "Default Tags",
    "Documentation",
    "Force Tags",
    "Library",
    "Metadata",
    "Resource",
    "Suite Setup",
    "Suite Teardown",
    "Task Setup",
    "Task Teardown",
    "Task Template",
    "Task Timeout",
    "Test Setup",
    "Test Teardown",
    "Test Template",
    "Test Timeout",
    "Variables",
]

CASE_SETTINGS = ["Documentation", "Setup", "Tags", "Teardown", "Template", "Timeout"]

KEYWORD_SETTINGS = [
    "Documentation",
    "Tags",
    "Teardown",
    "Timeout",
    "Arguments",
    "Return",
]

# lowercase line-starting tokens that trigger keyword completion
RE_PRE_KEYWORD_SUITE = r"^((suite|test|task) (setup|teardown)|(test|task) template)$"
RE_PRE_KEYWORD_BRACKET = r"^\[ *(setup|teardown|template) *\]$"


def get_default_completion_finders():
    """ The default ordering of completers, roughly from cheapest to most dear
    """
    return [
        complete_cell_magics,
        complete_tables,
        complete_libraries,
        complete_settings,
        complete_variables,
        complete_keywords,
    ]


def complete_cell_magics(
    completer: Completer,
    line: str,
    code: str,
    cursor_pos: int,
    line_cursor: int,
    offset: int,
    history: List[str],
):
    """ Complete with all defined magics
    """
    if not offset and line.startswith("%"):
        matches = (
            [
                f"%%{name}"
                for name in completer.parent.robot_magics["cell"]
                if name.startswith(line.replace("%", "").strip())
            ],
        )
        return (
            [
                {"start": offset, "end": offset + len(line), "type": "magic", "text": m}
                for m in matches
            ],
        )


def complete_tables(
    completer: Completer,
    line: str,
    code: str,
    cursor_pos: int,
    line_cursor: int,
    offset: int,
    history: List[str],
) -> Tuple[List[str], List[dict]]:
    """ Complete table names
    """

    matches = []

    if line.startswith("*"):
        no_star = line.replace("*", "").lower().strip()
        for name in TABLE_NAMES:
            if not no_star or name.lower().startswith(no_star):
                matches.append(f"*** {name} ***\n")
    elif line.startswith("| *"):
        no_star = line.replace("*", "").replace("|", "").lower().strip()
        for name in TABLE_NAMES:
            if not no_star or name.lower().startswith(no_star):
                matches.append(f"| *** {name} *** |\n")

    return (
        matches,
        [
            {"start": offset, "end": offset + len(line), "type": "table", "text": m}
            for m in matches
        ],
    )


def complete_settings(
    completer: Completer,
    line: str,
    code: str,
    cursor_pos: int,
    line_cursor: int,
    offset: int,
    history: List[str],
) -> Tuple[List[str], List[dict]]:
    """ Complete settings
    """
    matches = []

    row = DataRow(RobotReader.split_row(line[:line_cursor]))
    tokens = row.data

    current_table = find_current_table(code, cursor_pos)

    if current_table is None:
        return matches, []

    bracket = False
    settings = None
    if "etting" in current_table:
        settings = SUITE_SETTINGS
    elif "test case" in current_table or "task" in current_table:
        settings, bracket = CASE_SETTINGS, True
    elif "keyword" in current_table:
        settings, bracket = KEYWORD_SETTINGS, True

    if not settings:
        return matches, []

    matches = complete_table_settings(completer, settings, tokens[-1], bracket)

    post = ""

    if bracket and not line.strip()[-1] == "]":
        post = "]"
        post += " | " if line.startswith("|") else "  "
    elif not bracket:
        post += " | " if line.startswith("|") else "  "

    matches = [
        f"{line[:line_cursor - (len(tokens[-1]))]}{match}{post}" for match in matches
    ]

    return (
        matches,
        [
            {
                "start": cursor_pos,
                "end": offset + len(line),
                "type": "setting",
                "text": m,
            }
            for m in matches
        ],
    )


def complete_variables(
    completer: Completer,
    line: str,
    code: str,
    cursor_pos: int,
    line_cursor: int,
    offset: int,
    history: List[str],
) -> Tuple[List[str], List[dict]]:
    """ Complete variable references

        These aren't particularly clever in terms of scope.
    """
    matches = []

    if not re.findall(r"[\$&@%]", line):
        return matches, []

    try:
        frag = re.findall(r".*([\$%&@]\{[^{}]*$)", line[:line_cursor])[0]
        frag_type = frag[0]
        frag_start = frag[2:]
    except Exception:
        return matches, []

    try:
        if line[line_cursor] == "}":
            trail = ""
    except Exception:
        trail = "}"

    for var in find_all_variable_names(code, history, frag_type):
        if frag_start.lower() in var.lower():
            matches += [line.split(frag)[0] + frag_type + "{" + var + trail]

    return (
        matches,
        [
            {
                "start": cursor_pos,
                "end": offset + len(line),
                "type": "variable",
                "text": m,
            }
            for m in matches
        ],
    )


def complete_libraries(
    completer: Completer,
    line: str,
    code: str,
    cursor_pos: int,
    line_cursor: int,
    offset: int,
    history: List[str],
) -> Tuple[List[str], List[dict]]:
    """ Complete library names

        This could do better with sub-modules.
    """
    matches = []

    row = DataRow(RobotReader.split_row(line))
    tokens = row.data

    if not re.findall(r"\* *settings", code.lower(), flags=re.I):
        return matches, []

    if not tokens or tokens[0].lower() != "library":
        return matches, []

    for lib in list(STDLIBS) + list(get_root_modules()):
        if tokens[1].lower() in lib.lower():
            pre = line.split(tokens[1])[0]
            if line.startswith("|"):
                matches += [f"""{pre}{lib} | """]
            else:
                matches += [f"""{pre}{lib}  """]

    return (
        matches,
        [
            {
                "start": cursor_pos,
                "end": offset + len(line),
                "type": "library",
                "text": m,
            }
            for m in matches
        ],
    )


def complete_keywords(
    completer: Completer,
    line: str,
    code: str,
    cursor_pos: int,
    line_cursor: int,
    offset: int,
    history: List[str],
) -> Tuple[List[str], List[dict]]:
    """ Complete keywords from all imported libraries
    """
    matches = []

    row = DataRow(RobotReader.split_row(line))
    tokens = row.data

    if len(tokens) < 2:
        return matches, []

    if len(tokens) == 2 and not tokens[0].strip():
        kw_token = tokens[1]
    elif re.match(RE_PRE_KEYWORD_SUITE, tokens[0], flags=re.I) is not None:
        kw_token = tokens[1]
    elif re.match(RE_PRE_KEYWORD_BRACKET, tokens[1], flags=re.I) is not None:
        kw_token = tokens[2]
    else:
        return matches, []

    bdd = None
    orig_kw_token = kw_token
    bdd_token = re.match(r"^(given|when|then|and|but)?\b *(.*)", kw_token, flags=re.I)

    if bdd_token is not None:
        bdd, kw_token = bdd_token.groups()

    for doc in completer.docs(history).values():
        for keyword in getattr(doc, "keywords", []):
            if kw_token.lower() in keyword.name.lower():
                suggest_token = f"{bdd} {keyword.name}" if bdd else keyword.name
                pre = line.split(orig_kw_token)[0]
                if line.strip()[0] == "|":
                    matches.append(f"""{pre}{suggest_token} | """)
                else:
                    matches.append(f"""{pre}{suggest_token}  """)
    return (
        matches,
        [
            {
                "start": cursor_pos,
                "end": offset + len(line),
                "type": "keyword",
                "text": m,
            }
            for m in matches
        ],
    )


# Utility functions
def complete_table_settings(
    completer: Completer, settings: List[str], token: str, bracket: bool = False
) -> List[str]:
    """ Find settings that might be in a table
    """
    matches = []
    for setting in settings:
        if bracket:
            setting = f"[{setting}"
        if setting.lower().startswith(token.lower()):
            matches += [setting]
    return matches


def find_current_table(code: str, cursor_pos: int) -> str:
    """ Given some code, what is the current table we are in?
    """
    bits = re.split(r"^(\| )?(\*+ *[^*]+? *\*+)", code[:cursor_pos], flags=re.I | re.M)
    for bit in bits[::-1]:
        if bit is None:
            continue
        match = re.match(RE_TABLE_NAME, bit, flags=re.I)
        if match is not None:
            return match.groupdict()["name"].lower()
    return None


def find_all_variable_names(code: str, history: str, frag_type: str):
    """ Find all the variable names in the code and history

        frag_type is one of the Robot variable types
    """
    if frag_type == "%":
        pattern = r"""%\{[^\$%&@}]+}"""
    else:
        pattern = r"""[\$&@]\{[^\$%&@}]+}"""

    return [var[2:-1] for var in re.findall(pattern, "\n".join(history + [code]))]
