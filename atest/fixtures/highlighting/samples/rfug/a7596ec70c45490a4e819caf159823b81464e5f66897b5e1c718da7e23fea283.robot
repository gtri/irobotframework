*** Test Cases ***
List variable item
    Login    ${USER}[0]    ${USER}[1]
    Title Should Be    Welcome ${USER}[0]!

Negative index
    Log    ${LIST}[-1]

Index defined as variable
    Log    ${LIST}[${INDEX}]
