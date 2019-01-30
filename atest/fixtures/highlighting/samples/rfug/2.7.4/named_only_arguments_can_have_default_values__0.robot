*** Keywords ***
With Default
    [Arguments]    @{}    ${named}=default
    Log Many    ${named}

With And Without Defaults
    [Arguments]    @{}    ${optional}=default    ${mandatory}    ${mandatory 2}    ${optional 2}=default 2    ${mandatory 3}
    Log Many    ${optional}    ${mandatory}    ${mandatory 2}    ${optional 2}    ${mandatory 3}
