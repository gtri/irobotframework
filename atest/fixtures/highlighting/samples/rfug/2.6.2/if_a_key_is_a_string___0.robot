*** Test Cases ***
Dictionary variable item
    Login    ${USER}[name]    ${USER}[password]
    Title Should Be    Welcome ${USER}[name]!

Key defined as variable
    Log Many    ${DICT}[${KEY}]    ${DICT}[${42}]

Attribute access
    Login    ${USER.name}    ${USER.password}
    Title Should Be    Welcome ${USER.name}!
