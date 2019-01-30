*** Test Cases ***
Returning one value
    ${string} =    Return String
    Should Be Equal    ${string}    Hello, world!
    ${object} =    Return Object    Robot
    Should Be Equal    ${object.name}    Robot
