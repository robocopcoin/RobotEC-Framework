*** Settings ***
Suite Setup       Run Tests    ${EMPTY}    running/if/complex_if.robot
Resource          atest_resource.robot

*** Test Cases ***
Multiple keywords in if
   Check Test Case    ${TESTNAME}

Nested ifs
   Check Test Case    ${TESTNAME}

