*** Settings ***
Suite Setup       Run Tests    ${EMPTY}    running/if/complex_if.robot
Resource          atest_resource.robot

*** Test Cases ***
Multiple keywords in if
   Check Test Case    ${TESTNAME}

Nested ifs
   Check Test Case    ${TESTNAME}

If inside for loop
   Check Test Case    ${TESTNAME}

For loop inside if
   Check Test Case    ${TESTNAME}

Direct Boolean condition
   Check Test Case    ${TESTNAME}

Direct Boolean condition false
   Check Test Case    ${TESTNAME}