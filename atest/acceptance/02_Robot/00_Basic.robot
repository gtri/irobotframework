*** Settings ***
Documentation     Try out the Robot kernel
Default Tags      kernel:robot    browser:${BROWSER}
Resource          ../../resources/Lab.robot
Resource          ../../resources/Browser.robot
Resource          ../../resources/Notebook.robot
Resource          ../../resources/LabRobot.robot
Library           SeleniumLibrary

*** Test Cases ***
Robot Test Case Notebook
    [Documentation]    Can we make a simple Robot Test notebook?
    Set Screenshot Directory    ${OUTPUT_DIR}/${BROWSER}/robot/base
    Capture Page Screenshot    00_before.png
    Launch a new    Robot Framework    Notebook
    Capture Page Screenshot    01_new.png
    Add and Run Cell    ${TEST CASE 1}
    Capture Page Screenshot    02_running.png
    Capture Successful Robot "Log" Screenshot
    Capture Successful Robot "Report" Screenshot

Robot Task Notebook
    [Documentation]    Can we make a simple Robot Process Automation notebook?
    Set Screenshot Directory    ${OUTPUT_DIR}/${BROWSER}/robot/rpa
    Capture Page Screenshot    00_before.png
    Launch a new    Robot Framework    Notebook
    Capture Page Screenshot    01_new.png
    Add and Run Cell    ${TASK 1}
    Capture Page Screenshot    02_running.png
    Capture Successful Robot "Log" Screenshot
    Capture Successful Robot "Report" Screenshot
