*** Settings ***
Suite Setup       Run Tests    --dryrun    cli/dryrun/if.robot
Test Teardown     Last keyword should have been validated
Resource          dryrun_resource.robot

*** Test Cases ***
IF is not executed in dry run
    Check Test Case    ${TESTNAME}

ELSE IF is not executed in dry run
    Check Test Case    ${TESTNAME}

ELSE is not executed in dry run
    Check Test Case    ${TESTNAME}