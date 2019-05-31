*** Settings ***
Documentation     Work with Robot Suite Settings
Default Tags      kernel:robot    browser:${BROWSER}    py:${PY}    table:settings
Resource          ../../resources/Lab.robot
Resource          ../../resources/Browser.robot
Resource          ../../resources/Notebook.robot
Resource          ../../resources/LabRobot.robot
Library           SeleniumLibrary

*** Test Cases ***
Robot Notebook Remembers Settings
    [Documentation]    Will re-running Settings create an error in the logs?
    Set Screenshot Directory    ${OUTPUT_DIR}${/}robot${/}settings${/}cellid
    Capture Page Screenshot    00_before.png
    Launch a new    Robot Framework    Notebook
    Capture Page Screenshot    01_new.png
    Add and Run Cell    ${SETTINGS 1}
    Run Cell    2
    Add and Run Cell    ${TEST CASE 1}
    Capture Page Screenshot    02_running.png
    Capture Successful Robot "Log" Screenshot
    Capture Successful Robot "Report" Screenshot

Robot Notebook completes Settings
    [Documentation]    Will tabbing complete various Suite Settings?
    [Tags]    skip:chrome    skip:windows
    Set Screenshot Directory    ${OUTPUT_DIR}${/}robot${/}settings${/}complete
    Launch a new    Robot Framework    Notebook
    Add a Cell    *** Set
    Go to End of Cell Source
    Trigger Cell Source Completion
    Cell Source Should Eventually Contain    *** Settings ***\n
    Append to Cell Source    Lib
    Trigger Cell Source Completion
    Cell Source Should Eventually Contain    Library\ \
    Append to Cell Source    Operating
    Trigger Cell Source Completion
    Cell Source Should Eventually Contain    OperatingSystem
    Append to Cell Source    \nT
    Trigger Cell Source Completion
    Completions Should Contain    Test Setup \ \    Test Teardown \ \    Test Template \ \    Test Timeout \ \    # important whitespace
