*** Test Cases ***
Example
    :FOR    ${animal}    IN    cat    dog
    \    Log    ${animal}
    \    Log    2nd keyword
    Log    Outside loop
