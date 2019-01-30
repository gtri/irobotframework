*** Test Cases ***                                  # args, kwargs
Named-only only
    Dynamic    named=value                          # [], {named: value}
    Dynamic    named=value    named2=2              # [], {named: value, named2: 2}

Named-only with positional and varargs
    Dynamic    argument       named=xxx             # [argument], {named: xxx}
    Dynamic    a1             a2         named=3    # [a1, a2], {named: 3}

Named-only with normal named
    Dynamic    named=foo      positional=bar        # [], {positional: bar, named: foo}

Named-only with free named
    Dynamic    named=value    foo=bar               # [], {named: value, foo=bar}
    Dynamic    named2=2       third=3    named=1    # [], {named: 1, named2: 2, third: 3}
