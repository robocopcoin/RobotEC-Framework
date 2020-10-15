*** Settings ***
Suite Setup       Run Tests    --dryrun    cli/dryrun/if.robot
Test Teardown     Last keyword should have been validated
Resource          dryrun_resource.robot

*** Test Cases ***
IF will not recurse in dry run
    Check Test Case    ${TESTNAME}

ELSE IF will not recurse in dry run
    Check Test Case    ${TESTNAME}

ELSE will not recurse in dry run
    Check Test Case    ${TESTNAME}

Dryrun fail inside of IF
    Check Test Case    ${TESTNAME}

Dryrun fail inside of ELSE IF
    Check Test Case    ${TESTNAME}

Dryrun fail inside of ELSE
    Check Test Case    ${TESTNAME}