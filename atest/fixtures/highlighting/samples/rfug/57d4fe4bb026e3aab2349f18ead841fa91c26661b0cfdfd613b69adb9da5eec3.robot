*** Keywords ***
Free Named Only
    [Arguments]    &{named}
    Log Many    &{named}

Positional And Free Named
    [Arguments]    ${required}    &{extra}
    Log Many    ${required}    &{extra}

Run Program
    [Arguments]    @{args}    &{config}
    Run Process    program.py    @{args}    &{config}
