*** Settings ***
Resource          Lab.robot
Resource          Browser.robot
Resource          Notebook.robot
Resource          LabRobot.robot
Resource          CodeMirror.robot
Resource          Elements.robot
Library           SeleniumLibrary
Library           OperatingSystem

*** Keywords ***
Robot Syntax Highlighting Should Yield Tokens
    [Documentation]  Makes sure some notebook highlighting tokens are correct
    [Arguments]    ${example}
    Run Keyword And Ignore Error    Click Element    css:.jp-Dialog-button.jp-mod-accept
    ${robot} =    Get File    ..${/}fixtures${/}highlighting${/}samples${/}${example}.robot
    Add a Cell    ${robot}
    Run Keyword And Ignore Error    Click Element    ${SAVE}
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
