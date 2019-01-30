*** Keywords ***
With Positional
    [Arguments]    ${positional}    @{}    ${named}
    Log Many    ${positional}    ${named}

With Free Named
    [Arguments]    @{varargs}    ${named only}    &{free named}
    Log Many    @{varargs}    ${named only}    &{free named}
