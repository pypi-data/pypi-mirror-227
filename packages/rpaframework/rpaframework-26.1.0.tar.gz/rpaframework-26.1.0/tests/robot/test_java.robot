*** Settings ***
Library         RPA.JavaAccessBridge
Library         Process

#Suite Setup    Start Demo Application
Task Setup      Task setup actions

#Suite Teardown    Exit Demo Application
Force Tags      windows    skip


*** Variables ***
${RESOURCES}    ${CURDIR}${/}..${/}resources
${TEST_APP}     ${RESOURCES}${/}test-app${/}BasicSwing.jar


*** Tasks ***
Test click element
    Click Element    role:push button and name:Send

Test click push button
    Click Push Button    Send
    Click Push Button    Clear

Test print element tree
    ${tree}=    Print Element Tree

Test typing text
    Type Text    role:text    textarea text
    Type Text    role:text    input field text    index=1    clear=${TRUE}
    ${area_text}=    Get Element Text    role:text    0
    ${input_text}=    Get Element Text    role:text    1
    Should Contain    ${area_text}    textarea text
    Should Be Equal As Strings    input field text    ${input_text}

Test get elements
    ${elements}=    Get Elements    role:text
    ${len}=    Get Length    ${elements}
    Should Be Equal As Integers    ${len}    2
    Log Many    ${elements}[0]
    Log Many    ${elements}[1]
    Highlight Element    ${elements}[0]
    Highlight Element    ${elements}[1]

Test Java Elements
    ${elements}=    Get Elements    role:table > role:text
    Log To Console    ${elements}

Test Closing Java Window
    Select Window    Chat Frame
    Sleep    5
    Close Java Window

Test Listing Java Windows
    @{window_list}=    List Java Windows
    FOR    ${window}    IN    @{window_list}
        IF    "${window.title}" == "my java window title"
            Select Window By PID    ${window.pid}
        END
    END
    IF    len($window_list)==1    Select Window By PID    ${window_list[0].pid}


*** Keywords ***
Start Demo Application
    Start Process    java -jar ${TEST_APP}    shell=${TRUE}    cwd=${CURDIR}

Exit Demo Application
    Select Window    Chat Frame
    Select Menu    FILE    Exit
    Select Window    Exit
    Click Push Button    Exit ok

Clear chat frame
    Click Element    role:push button and name:Clear

Task setup actions
    Select Window    Chat Frame
    Clear chat frame
