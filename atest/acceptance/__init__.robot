*** Settings ***
Suite Setup       Start JupyterLab
Suite Teardown    Clean Up JupyterLab
Test Setup        Open JupyterLab with    ${BROWSER}
Test Teardown     Reset Application State and Close
Library           SeleniumLibrary
Resource          ../resources/Browser.robot
Resource          ../resources/Lab.robot
