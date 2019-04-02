*** Keywords ***
With Teardown
    Do Something
    [Teardown]    Log    keyword teardown

Using variables
    [Documentation]    Teardown given as variable
    Do Something
    [Teardown]    ${TEARDOWN}
