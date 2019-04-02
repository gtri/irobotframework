*** Test Cases ***
Exit Example
    ${text} =    Set Variable    ${EMPTY}
    FOR    ${var}    IN    one    two
        Run Keyword If    '${var}' == 'two'    Exit For Loop
        ${text} =    Set Variable    ${text}${var}
    END
    Should Be Equal    ${text}    one
