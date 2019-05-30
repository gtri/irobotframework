# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

""" Pure python tests of completion behavior
"""
import jupyter_kernel_test

from irobotframework.completion_finders import TABLE_NAMES

from . import RobotBase
from .utils import taskify


def cs(text, matches):
    return dict(text=text, matches=matches)


class Tables(RobotBase, jupyter_kernel_test.KernelTests):
    completion_samples = [
        cs("*", {f"*** {t} ***\n" for t in TABLE_NAMES}),
        cs("| *", {f"| *** {t} *** |\n" for t in TABLE_NAMES}),
    ]


KW_SPACE = """
*** Test Cases ***
One does not simply...
    Log M"""

KW_PIPE = """
| *Test Cases* |
| One does not simply...
| | Log M"""

KW_SUITE_SPACE = """
*** Settings ***
Suite Setup  Log M"""

KW_SUITE_PIPE = """
| *Settings * |
| Suite Setup | Log M"""

KW_BRACK_SPACE = """
*** Test Cases ***
One does not simply...
    [Setup]  Log M"""

KW_BRACK_PIPE = """
| *Test Case *|
| One does not simply...
| | [Setup] | Log M"""

LIB_SPACE = """
*** Settings ***
Library  OperatingSyste"""

LIB_PIPE = """
| *Settings* |
| Library | OperatingSyste"""


class Keywords(RobotBase, jupyter_kernel_test.KernelTests):
    completion_samples = [
        cs(KW_SPACE, {"    Log Many  "}),
        cs(taskify(KW_SPACE), {"    Log Many  "}),
        cs(KW_PIPE, {"| | Log Many | "}),
        cs(taskify(KW_PIPE), {"| | Log Many | "}),
        cs(KW_SUITE_SPACE, {"Suite Setup  Log Many  "}),
        cs(KW_SUITE_PIPE, {"| Suite Setup | Log Many | "}),
        cs(KW_BRACK_SPACE, {"    [Setup]  Log Many  "}),
        cs(taskify(KW_BRACK_SPACE), {"    [Setup]  Log Many  "}),
        cs(KW_BRACK_PIPE, {"| | [Setup] | Log Many | "}),
        cs(taskify(KW_BRACK_PIPE), {"| | [Setup] | Log Many | "}),
    ]


class Libraries(RobotBase, jupyter_kernel_test.KernelTests):
    completion_samples = [
        cs(LIB_SPACE, {"Library  OperatingSystem  "}),
        cs(LIB_PIPE, {"| Library | OperatingSystem | "}),
    ]


_SOME_VARS = """
*** Variables ***
${xy}  1
&{xyy}  1
@{xyyy}  1
%{xyyyy}  1
%{xyyyyy}  1
"""

_VAR_PRE = """
*** Test Cases ***
One does not simply...
    Log  """

VAR = _SOME_VARS + _VAR_PRE + "${X"
ENV_VAR = _SOME_VARS + _VAR_PRE + "%{X"


class Variables(RobotBase, jupyter_kernel_test.KernelTests):
    completion_samples = [
        cs(ENV_VAR, {"    Log  %{" + x + "}" for x in ["xyyyy", "xyyyyy"]}),
        cs(taskify(ENV_VAR), {"    Log  %{" + x + "}" for x in ["xyyyy", "xyyyyy"]}),
        cs(VAR, {"    Log  ${" + x + "}" for x in ["xy", "xyy", "xyyy"]}),
        cs(taskify(VAR), {"    Log  ${" + x + "}" for x in ["xy", "xyy", "xyyy"]}),
    ]


SET_SUITE_SPACE = """
*** Settings ***
Test"""

EX_SET_SUITE_SPACE = {
    "Test Setup  ",
    "Test Teardown  ",
    "Test Timeout  ",
    "Test Template  ",
}

SET_SUITE_PIPE = """
| *Settings* |
| Test"""

EX_SET_SUITE_PIPE = {
    "| Test Setup | ",
    "| Test Teardown | ",
    "| Test Timeout | ",
    "| Test Template | ",
}


class SuiteSettings(RobotBase, jupyter_kernel_test.KernelTests):
    completion_samples = [
        cs(SET_SUITE_SPACE, EX_SET_SUITE_SPACE),
        cs(taskify(SET_SUITE_SPACE), set(map(taskify, EX_SET_SUITE_SPACE))),
        cs(SET_SUITE_PIPE, EX_SET_SUITE_PIPE),
        cs(taskify(SET_SUITE_PIPE), set(map(taskify, EX_SET_SUITE_PIPE))),
    ]


SET_KW_SPACE = """
*** Keywords ***
A Keyword
    [A"""

EX_SET_KW_SPACE = {"    [Arguments]  "}

SET_KW_PIPE = """
| *Keyword* |
| A Keyword |
| | [A"""

EX_SET_KW_PIPE = {"| | [Arguments] | "}


class KeywordSettings(RobotBase, jupyter_kernel_test.KernelTests):
    completion_samples = [
        cs(SET_KW_SPACE, EX_SET_KW_SPACE),
        cs(SET_KW_PIPE, EX_SET_KW_PIPE),
    ]


SET_CASE_SPACE = """
*** Test Cases ***
A Test Cas
    [S"""

EX_SET_CASE_SPACE = {"    [Setup]  "}

SET_CASE_PIPE = """
| *Test Case* |
| A Test Case |
| | [S"""

EX_SET_CASE_PIPE = {"| | [Setup] | "}


class CaseSettings(RobotBase, jupyter_kernel_test.KernelTests):
    completion_samples = [
        cs(SET_CASE_SPACE, EX_SET_CASE_SPACE),
        cs(SET_CASE_PIPE, EX_SET_CASE_PIPE),
        cs(taskify(SET_CASE_PIPE), EX_SET_CASE_PIPE),
    ]


class MixedSettings(RobotBase, jupyter_kernel_test.KernelTests):
    completion_samples = [
        cs(f"{SET_SUITE_PIPE}\n\n{SET_KW_SPACE}", EX_SET_KW_SPACE),
        cs(f"{SET_KW_PIPE}\n\n{SET_SUITE_PIPE}", EX_SET_SUITE_PIPE),
        cs(f"{SET_KW_PIPE}\n\n{SET_CASE_PIPE}", EX_SET_CASE_PIPE),
        cs(f"{SET_SUITE_PIPE}\n\n{SET_CASE_SPACE}", EX_SET_CASE_SPACE),
    ]
