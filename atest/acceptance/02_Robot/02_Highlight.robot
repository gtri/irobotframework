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
    # BEGIN RFUG
    # END RFUG

*** Keywords ***
Robot Syntax Highlighting Should Yield Tokens
    [Arguments]    ${example}
    Run Keyword And Ignore Error    Click Element    css:.jp-Dialog-button.jp-mod-accept
    ${robot} =    Get File    ..${/}fixtures${/}highlighting${/}samples${/}${example}.robot
    Add a Cell    ${robot}
    ${observed} =    Get Cell Source Tokens
    ${cake} =    Evaluate    "\\n".join([" ".join(obs) for obs in ${observed}])
    Create File    ${OUTPUT DIR}${/}${BROWSER}${/}tokens${/}${example}.tokens    ${cake}
    ${raw} =    Get File    ..${/}fixtures${/}highlighting${/}tokens${/}${example}.tokens
    ${expected} =    Evaluate    [line.strip().split(" ") for line in """${raw}""".strip().split("\\n")]
    Should Be Equal    ${observed}    ${expected}

Make a Highlighting Notebook
    [Documentation]    Make a notebook for testing syntax highlighting
    Open JupyterLab with    ${BROWSER}
    Set Screenshot Directory    ${OUTPUT_DIR}${/}${BROWSER}${/}robot${/}highlighting
    Launch a new    Robot Framework    Notebook
