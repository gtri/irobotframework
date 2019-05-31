*** Test Cases ***
One Return Value
    ${ret} =    Return One Value    argument
    Some Keyword    ${ret}

Multiple Values
    ${a}    ${b}    ${c} =    Return Three Values
    @{list} =    Return Three Values
    ${scalar}    @{rest} =    Return Three Values

*** Keywords ***
Return One Value
    [Arguments]    ${arg}
    Do Something    ${arg}
    ${value} =    Get Some Value
    [Return]    ${value}

Return Three Values
    [Return]    foo    bar    zap
