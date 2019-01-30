*** Keywords ***
One line documentation
    [Documentation]    One line documentation.
    No Operation

Multiline documentation
    [Documentation]    The first line creates the short doc.
    ...
    ...                This is the body of the documentation.
    ...                It is not shown in Libdoc outputs but only
    ...                the short doc is shown in logs.
    No Operation

Short documentation in multiple lines
    [Documentation]    If the short doc gets longer, it can span
    ...                multiple physical lines.
    ...
    ...                The body is separated from the short doc with
    ...                an empty line.
    No Operation
