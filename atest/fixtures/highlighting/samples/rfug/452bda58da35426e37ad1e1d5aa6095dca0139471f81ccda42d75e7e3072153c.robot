*** Test Cases ***
Template and for
    [Template]    Example keyword
    FOR    ${item}    IN    @{ITEMS}
        ${item}    2nd arg
    END
    FOR    ${index}    IN RANGE    42
        1st arg    ${index}
    END
