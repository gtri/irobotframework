*** Test Case ***
For-in-enumerate with two values per iteration
    FOR    ${index}    ${en}    ${fi}    IN ENUMERATE
    ...    cat      kissa
    ...    dog      koira
    ...    horse    hevonen
        Log    "${en}" in English is "${fi}" in Finnish (index: ${index})
    END
