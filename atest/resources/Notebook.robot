*** Settings ***
Documentation     JupyterLab Notebook activities
Library           SeleniumLibrary
Resource          Lab.robot
Resource          CodeMirror.robot


*** Variables ***
${VISIBLE_NOTEBOOK}  .jp-NotebookPanel:not(.p-mod-hidden)
${BUSY_KERNEL}    css:${VISIBLE_NOTEBOOK} .jp-Toolbar-kernelStatus.jp-FilledCircleIcon
${BUSY_PROMPT}    In [*]:


*** Keywords ***
Add a Cell
    [Documentation]   Add a cell (probably code) with the given source
    [Arguments]    ${code}
    Click Element    css:${VISIBLE_NOTEBOOK} .jp-NotebookPanel-toolbar .jp-AddIcon
    Wait Until Page Contains Element  css:${VISIBLE_NOTEBOOK} ${CELL_CSS}
    Click Element    css:${VISIBLE_NOTEBOOK} ${CELL_CSS}
    Set Cell Source    ${code}

Add and Run Cell
    [Arguments]    ${code}
    [Documentation]    Add a code cell to the currently active notebook and run it
    Add a Cell  ${code}
    Execute JupyterLab Command  Run Selected Cells And Don't Advance

Run Cell
    [Documentation]   Run a cell. Turns out "2" is actually the first cell. Make better.
    [Arguments]    ${cell_number}
    Click Element    css:${VISIBLE_NOTEBOOK} .jp-Cell:nth-child(${cell_number})
    Execute JupyterLab Command  Run Selected Cells And Don't Advance

Wait Until Kernel Is Idle
    [Documentation]    Wait for the kernel to be busy, and then stop being busy
    Wait Until Page Does Not Contain Element    ${BUSY_KERNEL}
    Wait Until Page Does Not Contain    ${BUSY_PROMPT}
