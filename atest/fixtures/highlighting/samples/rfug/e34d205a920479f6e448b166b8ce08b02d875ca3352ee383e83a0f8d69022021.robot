*** Keywords ***
Timed Keyword
    [Documentation]    Set only the timeout value and not the custom message.
    [Timeout]    1 minute 42 seconds
    Do Something
    Do Something Else

Wrapper With Timeout
    [Arguments]    @{args}
    [Documentation]    This keyword is a wrapper that adds a timeout to another keyword.
    [Timeout]    2 minutes    Original Keyword didn't finish in 2 minutes
    Original Keyword    @{args}

Wrapper With Customizable Timeout
    [Arguments]    ${timeout}    @{args}
    [Documentation]    Same as the above but timeout given as an argument.
    [Timeout]    ${timeout}
    Original Keyword    @{args}
