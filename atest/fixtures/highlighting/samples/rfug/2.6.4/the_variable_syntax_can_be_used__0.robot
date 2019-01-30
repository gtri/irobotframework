*** Test Cases ***
Example 1A
    Connect    example.com    80       # Connect gets two strings as arguments

Example 1B
    Connect    example.com    ${80}    # Connect gets a string and an integer

Example 2
    Do X    ${3.14}    ${-1e-4}        # Do X gets floating point numbers 3.14 and -0.0001
