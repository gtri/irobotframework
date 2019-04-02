*** Variables ***
@{NUMBERS}      ${1}    ${2}    ${5}
@{NAMES}        one     two     five

*** Test Cases ***
Iterate over two lists manually
    ${length}=    Get Length    ${NUMBERS}
    FOR    ${idx}    IN RANGE    ${length}
        Number Should Be Named    ${NUMBERS}[${idx}]    ${NAMES}[${idx}]
    END

For-in-zip
    FOR    ${number}    ${name}    IN ZIP    ${NUMBERS}    ${NAMES}
        Number Should Be Named    ${number}    ${name}
    END
