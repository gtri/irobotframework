*** Settings ***
Documentation     Highlight Robot Syntax
Suite Setup       Make a Highlighting Notebook
Default Tags      kernel:robot    browser:${BROWSER}    feature:highlighting
Resource          ../../resources/Lab.robot
Resource          ../../resources/Browser.robot
Resource          ../../resources/Notebook.robot
Resource          ../../resources/LabRobot.robot
Resource          ../../resources/CodeMirror.robot
Resource          ../../resources/Elements.robot
Library           SeleniumLibrary
Library           OperatingSystem

*** Test Cases ***
Robot Syntax is Beautiful
    [Documentation]    Does CodeMirror syntax highlighting work as expected?
    [Template]    Robot Syntax Highlighting Should Yield Tokens
    basic${/}00_test_case

*** Keywords ***
Robot Syntax Highlighting Should Yield Tokens
    [Arguments]    ${example}
    ${robot} =    Get File    ../fixtures/highlighting/${example}.robot
    ${tokens} =    Get File    ../fixtures/highlighting/${example}.tokens
    ${tokens} =    Evaluate    [["cm-{}".format(t) for t in line.strip().split(" ")] for line in """${tokens}""".strip().split("\\n")]
    Add a Cell    ${robot}
    Cell Source Tokens Should Equal    ${tokens}

Make a Highlighting Notebook
    [Documentation]    Make a notebook for testing syntax highlighting
    Open JupyterLab with    ${BROWSER}
    Set Screenshot Directory    ${OUTPUT_DIR}/${BROWSER}/robot/highlighting
    Launch a new    Robot Framework    Notebook
