*** Test Cases ***
String
    ${string} =    Set Variable    abc
    Log    ${string.upper()}      # Logs 'ABC'
    Log    ${string * 2}          # Logs 'abcabc'

Number
    ${number} =    Set Variable    ${-2}
    Log    ${number * 10}         # Logs -20
    Log    ${number.__abs__()}    # Logs 2
