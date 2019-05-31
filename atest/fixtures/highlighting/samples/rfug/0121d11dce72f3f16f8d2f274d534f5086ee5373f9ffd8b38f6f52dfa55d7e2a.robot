*** Test Cases ***
Free Named Arguments
    Run Program    arg1    arg2    cwd=/home/user
    Run Program    argument    shell=True    env=${ENVIRON}

*** Keywords ***
Run Program
    [Arguments]    @{args}    &{config}
    Run Process    program.py    @{args}    &{config}
