*** Settings ***
Documentation     Some quick tests to see if we broke the build somehow.
Suite Setup       Set Screenshot Directory    ${OUTPUT_DIR}${/}smoke
Resource          ../resources/Lab.robot
Resource          ../resources/Browser.robot

*** Test Cases ***
JupyterLab Loads
    [Documentation]    Does a JupyterLab open?
    Page Should Contain    Robot Framework
    Capture Page Screenshot    00_smoke.png
