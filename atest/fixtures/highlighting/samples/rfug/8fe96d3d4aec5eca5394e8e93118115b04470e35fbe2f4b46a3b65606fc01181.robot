*** Test Cases ***
Three loop variables
    FOR    ${index}    ${english}    ${finnish}    IN
    ...     1           cat           kissa
    ...     2           dog           koira
    ...     3           horse         hevonen
        Add to dictionary    ${english}    ${finnish}    ${index}
    END
    FOR    ${name}    ${id}    IN    @{EMPLOYERS}
        Create    ${name}    ${id}
    END
