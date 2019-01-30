*** Test Cases ***
Named-only Arguments
    Run Program    arg1    arg2              # 'shell' is False (default)
    Run Program    argument    shell=True    # 'shell' is True

*** Keywords ***
Run Program
    [Arguments]    @{args}    ${shell}=False
    Run Process    program.py    @{args}    shell=${shell}
