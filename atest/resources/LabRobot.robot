*** Settings ***
Documentation  Robotic things to do in JupyterLab
Library  SeleniumLibrary

*** Variables ***
${TEST CASE 1}    | *Test Case* |\n| A Test\n| | Log | Hello
${MAGIC TEST CASE 1}    %%robot\n${TEST CASE 1}
${SETTINGS 1}     | *Setting* |\n| Documentation | This is Docs
${TASK 1}    | *Tasks* |\n| A Test\n| | Log | Hello

*** Keywords ***
Load IPython Robot extension
    [Documentation]   Reload the the IPython robot extension
    Add and Run Cell    %reload_ext irobotframework

Capture ${criteria} Robot "${document}" Screenshot
    [Documentation]   Verify that documents are clickable and contain expected content
    ${xpath} =  Set Variable  //a[text() = '${document}']
    ${title} =  Set Variable  Untitled Test Suite ${document}
    Wait Until Page Contains Element    ${xpath}  timeout=20s
    Click Element    ${xpath}
    Sleep    1s
    Select Window   NEW
    Wait Until Page Contains Element    //h1[text() = '${title}']
    Run Keyword If    'fail' not in '${criteria.lower()}'   Page Should Not Contain Element   //h2[text() = 'Test Execution Errors']
    Run Keyword If    'fail' in '${criteria.lower()}'   Page Should Contain Element   //h2[text() = 'Test Execution Errors']
    [Teardown]  Close ${document} Popup and restore main

Close ${document} Popup and restore main
    [Documentation]  Take a picture of a robot popup and close it
    Capture Page Screenshot    ${document.lower()}.png
    Execute Javascript    window.close()
    Select Window  MAIN
