*** Test Cases ***
Example
    I execute "ls"
    I execute "ls" with "-lh"
    I type 1 + 2
    I type 53 - 11
    Today is 2011-06-27

*** Keywords ***
I execute "${cmd:[^"]+}"
    Run Process    ${cmd}    shell=True

I execute "${cmd}" with "${opts}"
    Run Process    ${cmd} ${opts}    shell=True

I type ${a:\d+} ${operator:[+-]} ${b:\d+}
    Calculate    ${a}    ${operator}    ${b}

Today is ${date:\d{4\}-\d{2\}-\d{2\}}
    Log    ${date}
