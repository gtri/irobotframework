*** Test Cases ***
Coercion
    Double Argument     3.14
    Double Argument     2e16
    Compatible Types    Hello, world!    1234
    Compatible Types    Hi again!    -10    true

No Coercion
    Double Argument    ${3.14}
    Conflicting Types    1       ${2}    # must use variables
    Conflicting Types    ${1}    2
