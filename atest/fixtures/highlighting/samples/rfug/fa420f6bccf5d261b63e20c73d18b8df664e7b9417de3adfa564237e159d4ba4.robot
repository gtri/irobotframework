*** Settings ***
Library    SomeLibrary    localhost        1234    WITH NAME    LocalLib
Library    SomeLibrary    server.domain    8080    WITH NAME    RemoteLib

*** Test Cases ***
My Test
    LocalLib.Some Keyword     some arg       second arg
    RemoteLib.Some Keyword    another arg    whatever
    LocalLib.Another Keyword
