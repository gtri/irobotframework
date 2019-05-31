*** Settings ***
Documentation   Keywords for checking things about WebElements
Library   SeleniumLibrary

*** Keywords ***
Element Should Only Have Classes
    [Documentation]  Does the given element only have the given CSS classes?
    [Arguments]  ${el}  ${expected_classes}
    ${raw_classes} =   Call Method    ${el}   get_attribute   class
    ${observed} =  Set Variable  ${raw_classes.split(" ")}
    ${difference} =  Evaluate  set(${expected_classes}).symmetric_difference(set(${observed}))
    Should Be Empty    ${difference}
