*** Settings ***
Documentation     Run JupyterLab commands
Resource          Selectors.robot
Resource          Sidebar.robot


*** Keywords ***
Execute JupyterLab Command
    [Arguments]    ${command}  ${accept}=${True}  ${close}=${True}
    [Documentation]    Use the JupyterLab Command Palette to run a command
    Maybe accept a JupyterLab prompt
    Maybe Open JupyterLab Sidebar  command-palette
    Input Text    ${CMD_PAL_INPUT}    ${command}
    Wait Until Page Contains Element    ${CMD_PAL_ITEM}
    Click Element    ${CMD_PAL_ITEM}
    Run Keyword If  ${accept}  Maybe Accept a JupyterLab Prompt
    Run Keyword If  ${close}  Maybe Close JupyterLab Sidebar

Reset JupyterLab and Close
    [Documentation]    Try to clean up after doing some things to the JupyterLab state
    Execute JupyterLab Command    Reset Application State
    Close Browser
