*** Keywords ***
True examples
    Should Be Equal    ${x}    ${y}    Custom error    values=True         # Strings are generally true.
    Should Be Equal    ${x}    ${y}    Custom error    values=yes          # Same as the above.
    Should Be Equal    ${x}    ${y}    Custom error    values=${TRUE}      # Python `True` is true.
    Should Be Equal    ${x}    ${y}    Custom error    values=${42}        # Numbers other than 0 are true.

False examples
    Should Be Equal    ${x}    ${y}    Custom error    values=False        # String `false` is false.
    Should Be Equal    ${x}    ${y}    Custom error    values=no           # Also string `no` is false.
    Should Be Equal    ${x}    ${y}    Custom error    values=${EMPTY}     # Empty string is false.
    Should Be Equal    ${x}    ${y}    Custom error    values=${FALSE}     # Python `False` is false.
    Should Be Equal    ${x}    ${y}    Custom error    values=no values    # Special false string with this keyword.
