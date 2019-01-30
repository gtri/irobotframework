| *** Test Cases *** |                 |                 |                      |
| Escaping Pipe      | ${file count} = | Execute Command | ls -1 *.txt \| wc -l |
|                    | Should Be Equal | ${file count}   | 42                   |
