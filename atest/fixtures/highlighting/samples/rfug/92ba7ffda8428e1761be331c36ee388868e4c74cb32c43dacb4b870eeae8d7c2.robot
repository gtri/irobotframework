*** Settings ***
Library    Remote    http://127.0.0.1:8270       WITH NAME    Example1
Library    Remote    http://example.com:8080/    WITH NAME    Example2
Library    Remote    http://10.0.0.2/example    1 minute    WITH NAME    Example3
