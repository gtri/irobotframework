*** Settings ***
Force Tags      req-42
Default Tags    owner-john    smoke

*** Variables ***
${HOST}         10.0.1.42

*** Test Cases ***
No own tags
    [Documentation]    This test has tags owner-john, smoke and req-42.
    No Operation

With own tags
    [Documentation]    This test has tags not_ready, owner-mrx and req-42.
    [Tags]    owner-mrx    not_ready
    No Operation

Own tags with variables
    [Documentation]    This test has tags host-10.0.1.42 and req-42.
    [Tags]    host-${HOST}
    No Operation

Empty own tags
    [Documentation]    This test has only tag req-42.
    [Tags]
    No Operation

Set Tags and Remove Tags Keywords
    [Documentation]    This test has tags mytag and owner-john.
    Set Tags    mytag
    Remove Tags    smoke    req-*
