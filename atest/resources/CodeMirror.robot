
*** Settings ***
Documentation     JupyterLab Notebook activities
Library           SeleniumLibrary
Resource          Lab.robot

*** Variables ***
${COMPLETE_CSS}   css:.jp-Completer-item


*** Keywords ***
Evaluate Cell CodeMirror
    [Documentation]   Run a method against CodeMirror in the current cell
    [Arguments]  ${code}
    ${result} =  Execute JavaScript    return document.querySelector("${VISIBLE_NOTEBOOK} ${CELL_CSS}").CodeMirror.${code}
    [Return]  ${result}

Set Cell Source
    [Documentation]   Set the source of a cell
    [Arguments]   ${code}
    ${result} =   Evaluate Cell CodeMirror    setValue(`${code}`)
    [Return]   ${result}

Append to Cell Source
    [Documentation]   Set the source of a cell
    [Arguments]   ${source}
    ${old source} =   Get Cell Source
    ${result} =   Evaluate Cell CodeMirror    setValue(`${old source}${source}`)
    Go to End of Cell Source
    [Return]   ${result}

Get Cell Source
    [Documentation]   Get the source of a cell
    ${result} =  Evaluate Cell CodeMirror  getValue()
    [Return]   ${result}

Go to End of Cell Source
    [Documentation]   Position the caret at the end of the cell
    Evaluate Cell CodeMirror    execCommand('goDocEnd')

Cell Source Should Equal
    [Documentation]   Compare the exact source of a cell to a given text
    [Arguments]  ${text}
    ${result} =  Get Cell Source
    Should Be Equal  ${result}  ${text}

Cell Source Should Contain
    [Documentation]   Whether source of a cell contains given text
    [Arguments]  ${text}
    ${result} =  Get Cell Source
    Should Contain    ${result}  ${text}

Trigger Cell Source Completion
    [Documentation]   Initiate Tab Complete
    Press Key  css:body  \\9

Completions Should Contain
    [Documentation]   Does the completer show the expected completions?
    [Arguments]  @{completions}
    :FOR   ${c}   IN  @{completions}
    \   Wait Until Page Contains Element    ${COMPLETE_CSS}\[data-value="${c}"]
