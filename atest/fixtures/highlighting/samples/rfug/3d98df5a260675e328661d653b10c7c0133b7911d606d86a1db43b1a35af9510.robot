*** Test Cases ***
Only upper limit
    [Documentation]    Loops over values from 0 to 9
    FOR    ${index}    IN RANGE    10
        Log    ${index}
    END

Start and end
    [Documentation]    Loops over values from 1 to 10
    FOR    ${index}    IN RANGE    1    11
        Log    ${index}
    END

Also step given
    [Documentation]    Loops over values 5, 15, and 25
    FOR    ${index}    IN RANGE    5    26    10
        Log    ${index}
    END

Negative step
    [Documentation]    Loops over values 13, 3, and -7
    FOR    ${index}    IN RANGE    13    -13    -10
        Log    ${index}
    END

Arithmetic
    [Documentation]    Arithmetic with variable
    FOR    ${index}    IN RANGE    ${var} + 1
        Log    ${index}
    END

Float parameters
    [Documentation]    Loops over values 3.14, 4.34, and 5.54
    FOR    ${index}    IN RANGE    3.14    6.09    1.2
        Log    ${index}
    END
