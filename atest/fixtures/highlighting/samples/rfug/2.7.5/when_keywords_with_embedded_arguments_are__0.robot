*** Test Cases ***
Example
    I execute "ls"
    I execute "ls" with "-lh"

*** Keywords ***
I execute "${cmd}"
    Run Process    ${cmd}    shell=True

I execute "${cmd}" with "${opts}"
    Run Process    ${cmd} ${opts}    shell=True
