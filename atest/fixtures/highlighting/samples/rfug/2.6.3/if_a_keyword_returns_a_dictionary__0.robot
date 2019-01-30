*** Test Cases ***
Example
    &{dict} =    Create Dictionary    first=1    second=${2}    ${3}=third
    Length Should Be    ${dict}    3
    Do Something    &{dict}
    Log    ${dict.first}
