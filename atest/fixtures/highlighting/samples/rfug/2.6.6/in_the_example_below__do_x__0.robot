*** Variables ***
${JOHN HOME}    /home/john
${JANE HOME}    /home/jane

*** Test Cases ***
Example
    ${name} =    Get Name
    Do X    ${${name} HOME}
