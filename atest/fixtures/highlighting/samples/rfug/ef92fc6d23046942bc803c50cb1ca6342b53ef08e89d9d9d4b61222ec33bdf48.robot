*** Settings ***
Library    SeleniumLibrary
Library    SeLibExtensions

*** Test Cases ***
Example
    Open Browser    http://example      # SeleniumLibrary
    Title Should Start With    Example  # SeLibExtensions
