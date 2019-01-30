*** Settings ***
Library         ExampleLibrary      @{LIB ARGS}    # This works
Library         ${LIBRARY}          @{LIB ARGS}    # This works
Library         @{LIBRARY AND ARGS}                # This does not work
Suite Setup     Some Keyword        @{KW ARGS}     # This works
Suite Setup     ${KEYWORD}          @{KW ARGS}     # This works
Suite Setup     @{KEYWORD AND ARGS}                # This does not work
Default Tags    @{TAGS}                            # This works
