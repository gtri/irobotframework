*** Settings ***
Documentation      This is documentation for this test suite.\nThis kind of documentation can often be get quite long...
Default Tags       default tag 1    default tag 2    default tag 3    default tag 4    default tag 5

*** Variable ***
@{LIST}            this     list     is      quite    long     and    items in it could also be long

*** Test Cases ***
Example
    [Tags]    you    probably    do    not    have    this    many    tags    in    real   life
    Do X    first argument    second argument    third argument    fourth argument    fifth argument    sixth argument
    ${var} =    Get X    first argument passed to this keyword is pretty long   second argument passed to this keyword is long too
