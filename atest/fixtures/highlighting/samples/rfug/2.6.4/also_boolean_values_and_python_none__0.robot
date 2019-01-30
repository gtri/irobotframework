*** Test Cases ***
Boolean
    Set Status    ${true}               # Set Status gets Boolean true as an argument
    Create Y    something   ${false}    # Create Y gets a string and Boolean false

None
    Do XYZ    ${None}                   # Do XYZ gets Python None as an argument

Null
    ${ret} =    Get Value    arg        # Checking that Get Value returns Java null
    Should Be Equal    ${ret}    ${null}
