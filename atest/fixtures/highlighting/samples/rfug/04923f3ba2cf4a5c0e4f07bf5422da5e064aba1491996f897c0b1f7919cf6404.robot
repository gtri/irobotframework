*** Test Cases ***
Start index
    Keyword    ${LIST}[1:]

End index
    Keyword    ${LIST}[:4]

Start and end
    Keyword    ${LIST}[2:-1]

Step
    Keyword    ${LIST}[::2]
    Keyword    ${LIST}[2:-1:2]
