*** Test Cases ***
Positional
    Various Args    hello    world                # Logs 'arg: hello' and 'vararg: world'.

Named
    Various Args    arg=value                     # Logs 'arg: value'.

Kwargs
    Various Args    a=1    b=2    c=3             # Logs 'kwarg: a 1', 'kwarg: b 2' and 'kwarg: c 3'.
    Various Args    c=3    a=1    b=2             # Same as above. Order does not matter.

Positional and kwargs
    Various Args    1    2    kw=3                # Logs 'arg: 1', 'vararg: 2' and 'kwarg: kw 3'.

Named and kwargs
    Various Args    arg=value      hello=world    # Logs 'arg: value' and 'kwarg: hello world'.
    Various Args    hello=world    arg=value      # Same as above. Order does not matter.
