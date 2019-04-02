*** Settings ***
Documentation    Resource file for demo purposes.
...              This resource is only used in an example and it doesn't do anything useful.

*** Keywords ***
My Keyword
    [Documentation]   Does nothing
    No Operation

Your Keyword
    [Arguments]  ${arg}
    [Documentation]   Takes one argument and *does nothing* with it.
    ...
    ...    Examples:
    ...    | Your Keyword | xxx |
    ...    | Your Keyword | yyy |
    No Operation
