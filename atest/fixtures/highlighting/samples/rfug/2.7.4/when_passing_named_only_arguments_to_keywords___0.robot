*** Test Cases ***
Example
    With Varargs    named=value
    With Varargs    positional    second positional    named=foobar
    Without Varargs    first=1    second=2
    Without Varargs    second=toka    first=eka
    With Positional    foo    named=bar
    With Positional    named=2    positional=1
    With Free Named    positional    named only=value    x=1    y=2
    With Free Named    foo=a    bar=b    named only=c    quux=d
