*** Settings ***
Test Timeout    2 minutes

*** Test Cases ***
Default Timeout
    [Documentation]    Timeout from the Setting table is used
    Some Keyword    argument

Override
    [Documentation]    Override default, use 10 seconds timeout
    [Timeout]    10
    Some Keyword    argument

Custom Message
    [Documentation]    Override default and use custom message
    [Timeout]    1min 10s    This is my custom error
    Some Keyword    argument

Variables
    [Documentation]    It is possible to use variables too
    [Timeout]    ${TIMEOUT}
    Some Keyword    argument

No Timeout
    [Documentation]    Empty timeout means no timeout even when Test Timeout has been used
    [Timeout]
    Some Keyword    argument

No Timeout 2
    [Documentation]    Disabling timeout with NONE works too and is more explicit.
    [Timeout]    NONE
    Some Keyword    argument
