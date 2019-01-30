*** Test Cases ***
Example
    Create Binary File    ${CURDIR}${/}input.data    Some text here${\n}on two lines
    Set Environment Variable    CLASSPATH    ${TEMPDIR}${:}${CURDIR}${/}foo.jar
