*** Settings ***
Documentation     Base JupyterLab activities (should be split into server/ui)
Library           Process
Library           BuiltIn
Library           SeleniumLibrary
Library           OperatingSystem
Resource          Selectors.robot
Resource          Commands.robot

*** Variables ***
${TOKEN}          hopelesslyinsecure
${LAB_CMD}        jupyter-lab --no-browser --NotebookApp.token=${TOKEN} --port 18888 --debug --ip=0.0.0.0
${LAB_URL}        http://localhost:18888/lab?token=${TOKEN}

*** Keywords ***
Wait for Splash Screen
    [Documentation]    Wait for the JupyterLab splash animation to run its course
    Wait Until Page Contains Element    ${SPLASH_ID}
    Wait Until Page Does Not Contain Element    ${SPLASH_ID}
    Sleep    0.1s

Launch a new
    [Arguments]    ${kernel}    ${category}
    [Documentation]    Use the JupyterLab launcher to launch Notebook or Console
    Click Element    css:${CARD_CSS}\[title='${kernel}'][data-category='${category}']
    Wait Until Page Does Not Contain Element    ${SPINNER}
    Wait Until Page Contains Element    css:${CELL_CSS}
    Sleep    1s

Start JupyterLab
    [Documentation]    Start a Jupyter Notebook Server with JupyterLab
    ${notebooks} =  Set Variable  ${OUTPUT_DIR}${/}${BROWSER}${/}_notebooks
    ${log} =  Set Variable  ${OUTPUT_DIR}${/}${BROWSER}${/}_lab.log
    ${cmd} =  Set Variable  ${LAB_CMD} --notebook-dir=${notebooks}
    Create Directory      ${notebooks}
    Start Process    ${cmd}    shell=true    stderr=STDOUT    stdout=${log}

Click JupyterLab Menu
    [Arguments]    ${menu_label}
    [Documentation]    Click a top-level JupyterLab Menu bar, e.g. File, Help, etc.
    Wait Until Page Contains Element    ${TOP}${BAR_ITEM}\[text() = '${menu_label}']
    Mouse Over    ${TOP}${BAR_ITEM}\[text() = '${menu_label}']
    Click Element    ${TOP}${BAR_ITEM}\[text() = '${menu_label}']

Click JupyterLab Menu Item
    [Arguments]    ${item_label}
    [Documentation]    Click a top-level JupyterLab Menu Item (not File, Help, etc.)
    ${item} =    Set Variable    //div[@class='p-Menu-itemLabel']
    Wait Until Page Contains Element    ${item}\[text() = '${item_label}']
    Mouse Over    ${item}\[text() = '${item_label}']
    Click Element    ${item}\[text() = '${item_label}']

Open JupyterLab with
    [Arguments]    ${browser}
    [Documentation]    Start the given browser and wait for the animation
    Open Browser    ${LAB_URL}    ${browser}
    Wait for Splash Screen
    Sleep  0.1s

Reset Application State and Close
    [Documentation]    Try to clean up after doing some things to the JupyterLab state
    Run Keyword And Ignore Error    Click Element  ${SAVE}
    Execute JupyterLab Command    Reset Application State
    Close All Browsers

Clean Up JupyterLab
    [Documentation]    Close all the browsers and stop all processes
    Close All Browsers
    Terminate All Processes    kill=True

Maybe Accept a JupyterLab Prompt
    [Documentation]  Accept the JupyterLab prompt, if visible
    ${accept} =  Get WebElements  css:${JLAB CSS ACCEPT}
    Run Keyword If  ${accept}   Click Element    ${accept[0]}
