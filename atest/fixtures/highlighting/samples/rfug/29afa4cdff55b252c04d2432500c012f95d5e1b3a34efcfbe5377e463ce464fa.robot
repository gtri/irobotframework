| *** Test Cases ***
| Recommended solution
| | FOR  | ${animal}    | IN          | cat | dog |
| |      | Log          | ${animal}   |
| |      | Log          | 2nd keyword |
| | END  |              |
| | Log  | Outside loop |
|
| Compatible with RF 3.0.x
| | :FOR | ${animal}    | IN          | cat | dog |
| | \    | Log          | ${animal}   |
| | \    | Log          | 2nd keyword |
| | Log  | Outside loop |
