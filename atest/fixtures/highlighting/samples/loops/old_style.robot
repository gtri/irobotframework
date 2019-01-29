*** Keywords ***
This is a ${woo} keyword
    Log  and it's normal ${var}

Old Syntax
    Log    Outside loop
:FOR    ${animal}    IN    cat    dog
    \    Log    ${animal}
    \    Log    2nd keyword   sds  ${asdasda}
    \    ${x} =  Log  ${animal}
    Log    Outside loop
    Log    outside

This is a keyword
    Log  and it's ${var} normal

*** Variables ***
${pop}  Fooo
