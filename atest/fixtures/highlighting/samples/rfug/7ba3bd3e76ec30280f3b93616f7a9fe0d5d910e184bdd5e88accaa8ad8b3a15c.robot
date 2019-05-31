*** Test Cases ***
Continue Example
    ${text} =    Set Variable    ${EMPTY}
    FOR    ${var}    IN    one    two    three
        Continue For Loop If    '${var}' == 'two'
        ${text} =    Set Variable    ${text}${var}
    END
    Should Be Equal    ${text}    onethree
