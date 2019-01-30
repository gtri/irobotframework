*** Test Cases ***
Environment variables
    Log    Current user: %{USER}
    Run    %{JAVA_HOME}${/}javac
