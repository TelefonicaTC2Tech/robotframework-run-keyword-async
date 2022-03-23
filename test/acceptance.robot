*** Settings ***

Library    runKeywordAsync


*** Keywords ***

KW 1
    [Arguments]       ${timeout}=2s
    Sleep             ${timeout}
    Should Be True    ${true}          msg=Keywork 1 failed

KW 2
    [Arguments]       ${timeout}=1s
    Sleep             ${timeout}
    Should Be True    ${false}         msg=Keywork 2 failed

KW 3
    [Arguments]       ${timeout}=1s
    Sleep             ${timeout}
    Should Be True    ${true}          msg=Keywork 3 failed

*** Test Cases ***

Test OK

    ${handle}=    Run Keyword Async    KW 1

    ${handle}=    Run Keyword Async    KW 3

    ${return_value}=    Wait Async All



Test OK Single Process

    ${handle}=    Run Keyword Async    KW 1

    ${return_value}=    Wait Async All    

Test Fail

    ${handle_1}=    Run Keyword Async    KW 2
    ${handle_2}=    Run Keyword Async    KW 1

    ${passed}    Run Keyword And Return Status    Wait Async All    timeout=5

    Should Not Be True    ${passed}


Test OK Custom Pool

    ${handle_1}=    Run Keyword Async With Custom Pool    pool_1    KW 1

    ${handle_2}=    Run Keyword Async With Custom Pool    pool_1    KW 3    

    ${return_value}=    Wait Async All    pool=pool_1    timeout=5

Test Fail Custom Pool

    ${handle_1}=    Run Keyword Async With Custom Pool    pool_2    KW 1

    ${handle_2}=    Run Keyword Async With Custom Pool    pool_2    KW 2    

    ${passed}    Run Keyword And Return Status    Wait Async All    pool=pool_2    timeout=5

    Should Not Be True    ${passed}

Test Wrong Pool

    ${handle_1}=    Run Keyword Async With Custom Pool    pool_3    KW 1    

    ${handle_2}=    Run Keyword Async With Custom Pool    pool_3    KW 2    

    ${passed}    Run Keyword And Return Status    Wait Async All    pool=pool_4    timeout=5    

    Should Not Be True    ${passed}


Test Multiple Pools

    ${handle_2_1}=    Run Keyword Async With Custom Pool    pool_2    KW 1    

    ${handle_2_2}=    Run Keyword Async With Custom Pool    pool_2    KW 3 

    ${handle_1_1}=    Run Keyword Async With Custom Pool    pool_1    KW 1    timeout=10s

    ${handle_1_2}=    Run Keyword Async With Custom Pool    pool_1    KW 3    timeout=8s

    ${handle_2_3}=    Run Keyword Async With Custom Pool    pool_2    KW 1    

    ${handle_2_4}=    Run Keyword Async With Custom Pool    pool_2    KW 3    

    ${return_value}=    Wait Async All    pool=pool_2    timeout=5
    Log To Console  \npool_2 finished

    ${return_value}=    Wait Async All    pool=pool_1    timeout=10    
    Log To Console  \npool_1 finished