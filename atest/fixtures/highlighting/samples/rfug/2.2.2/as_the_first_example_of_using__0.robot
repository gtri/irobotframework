*** Test Cases ***
Free Named Arguments
    Run Process    program.py    arg1    arg2    cwd=/home/user
    Run Process    program.py    argument    shell=True    env=${ENVIRON}
