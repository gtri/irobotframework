*** Test Cases ***
Template
    [Template]    Some keyword
    @{EMPTY}

Override
    Set Global Variable    @{LIST}    @{EMPTY}
    Set Suite Variable     &{DICT}    &{EMPTY}
