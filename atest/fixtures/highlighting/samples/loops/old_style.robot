*** Keywords ***
This is a ${woo} keyword
    Log  and it's normal ${var}

Old Syntax
    Log    Outside loop
    :FOR    ${i}  ${animal}    IN ENUMERATE   cat    dog
    \    Log    ${animal}
    \    Log    2nd keyword   a ${x.y}[0][${1}] b=${c${d}}  another
    \    Log    something
    \    ${x} =  Log  ${animal}
    Log    Outside loop

This is a keyword
    Log  and it's ${var} normal

*** Variables ***
${pop}  Fooo
