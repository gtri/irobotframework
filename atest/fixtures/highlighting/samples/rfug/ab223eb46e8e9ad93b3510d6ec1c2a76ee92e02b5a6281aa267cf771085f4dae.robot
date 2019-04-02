*** Test Cases ***                  # args, kwargs
No arguments
    Dynamic                         # [], {}

Positional only
    Dynamic    x                    # [x], {}
    Dynamic    x      y             # [x, y], {}

Free named only
    Dynamic    x=1                  # [], {x: 1}
    Dynamic    x=1    y=2    z=3    # [], {x: 1, y: 2, z: 3}

Free named with positional
    Dynamic    x      y=2           # [x], {y: 2}
    Dynamic    x      y=2    z=3    # [x], {y: 2, z: 3}

Free named with normal named
    Dynamic    a=1    x=1           # [], {a: 1, x: 1}
    Dynamic    b=2    x=1    a=1    # [], {a: 1, b: 2, x: 1}
