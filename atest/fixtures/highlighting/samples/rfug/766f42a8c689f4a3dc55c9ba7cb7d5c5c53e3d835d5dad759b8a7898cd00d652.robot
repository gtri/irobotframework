*** Test Cases ***
Using backslash
    Do Something    first arg    \
Using ${EMPTY}
    Do Something    first arg    ${EMPTY}
Non-trailing empty
    Do Something    ${EMPTY}     second arg    # Escaping needed in space separated format
