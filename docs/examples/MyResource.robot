*** Keywords ***
Ask the question  
  [Arguments]  ${question}
  ${answer} =  Set Variable If  "how many" in """${question}""".lower()  ${42}  Dunno?
  [Return]  ${answer}