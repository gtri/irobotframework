*** Settings ***
Documentation     Try out the python magics
Suite Setup       Set Screenshot Directory    ${OUTPUT_DIR}${/}python
Default Tags      kernel:python    browser:${BROWSER}    py:${PY}
Resource          ../resources/Lab.robot
Resource          ../resources/Browser.robot
Resource          ../resources/Notebook.robot
Resource          ../resources/LabRobot.robot

*** Test Cases ***
Python Notebook
    [Documentation]    Can we make a simple Python notebook?
    Capture Page Screenshot    00_before.png
    Launch a new    Python 3    Notebook
    Capture Page Screenshot    01_new.png
    Load IPython Robot extension
    Add and Run Cell    ${MAGIC TEST CASE 1}
    Capture Page Screenshot    02_running.png
    Capture Successful Robot "Log" Screenshot
    Capture Successful Robot "Report" Screenshot
