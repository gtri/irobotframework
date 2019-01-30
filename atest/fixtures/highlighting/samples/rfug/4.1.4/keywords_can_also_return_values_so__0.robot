*** Test Cases ***
Returning multiple values
    ${var1}    ${var2} =    Return Two Values
    Should Be Equal    ${var1}    first value
    Should Be Equal    ${var2}    second value
    @{list} =    Return Two Values
    Should Be Equal    @{list}[0]    first value
    Should Be Equal    @{list}[1]    second value
    ${s1}    ${s2}    @{li} =    Return Multiple Values
    Should Be Equal    ${s1} ${s2}    a list
    Should Be Equal    @{li}[0] @{li}[1]    of strings
