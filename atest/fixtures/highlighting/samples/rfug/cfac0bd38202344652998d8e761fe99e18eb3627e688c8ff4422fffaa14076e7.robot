*** Keywords ***
With Varargs
    [Arguments]    @{varargs}    ${named}
    Log Many    @{varargs}    ${named}

Without Varargs
    [Arguments]    @{}    ${first}    ${second}
    Log Many    ${first}    ${second}
