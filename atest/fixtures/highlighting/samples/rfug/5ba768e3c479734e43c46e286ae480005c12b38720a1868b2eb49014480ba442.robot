*** Keywords ***
Handle Table
    [Arguments]    @{table}
    FOR    ${row}    IN    @{table}
        Handle Row    @{row}
    END

Handle Row
    [Arguments]    @{row}
    FOR    ${cell}    IN    @{row}
        Handle Cell    ${cell}
    END
