
*** Settings ***
Documentation     JupyterLab Notebook activities
Library           SeleniumLibrary
Library           Collections
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
    ${result} =   Evaluate Cell CodeMirror    setValue(${code.split("\n")}.join("\\n"))
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

Cell Source Should Eventually Contain
    [Documentation]   Whether source of a cell contains given text (eventually)
    [Arguments]  ${text}
    Wait Until Keyword Succeeds   5x  1s  Cell Source Should Contain  ${text}

Cell Source Tokens Should Equal
    [Documentation]   Whether a cell is highlighted as expected
    [Arguments]  ${expected_tokens}
    ${observed_tokens} =  Get Cell Source Tokens
    Should Be Equal As Numbers    ${observed_tokens.__len__()}    ${expected_tokens.__len__()}
    FOR  ${i}  ${el}  IN ENUMERATE  @{observed_tokens}
      Element Should Only Have Classes  ${el}  ${expected_tokens[${i}]}
    END

Get Cell Source Tokens
    [Documentation]   Extract the current cell tokens
    ${tokens} =  Create List
    ${els} =  Get WebElements    css:${VISIBLE_NOTEBOOK} ${CELL_CSS} .CodeMirror-lines span[class^='cm-']
    FOR  ${el}  IN  @{els}
      ${raw_classes} =   Call Method    ${el}   get_attribute   class
      ${observed} =  Set Variable  ${raw_classes.replace("cm-", "").split(" ")}
      ${sorted} =  Evaluate  sorted(${observed})
      Run Keyword If  "tab-wrap-hack" not in ${sorted}   Append To List    ${tokens}  ${sorted}
    END
    [Return]  ${tokens}

Trigger Cell Source Completion
    [Documentation]   Initiate Tab Complete
    Press Key  css:body  \\9
    Wait Until Kernel Is Idle

Completions Should Contain
    [Documentation]   Does the completer show the expected completions?
    [Arguments]  @{completions}
    :FOR   ${c}   IN  @{completions}
    \   Wait Until Page Contains Element    ${COMPLETE_CSS}\[data-value="${c}"]
