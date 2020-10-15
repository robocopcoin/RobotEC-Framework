*** Settings ***
Resource        resource.robot

*** Test Cases ***
IF is not executed in dry run
    Recursive if  call again
    This is validated

ELSE IF is not executed in dry run
    Recursive else if  call again
    This is validated

ELSE is not executed in dry run
    Recursive else  call again
    This is validated

Dryrun fail inside of IF
    [Documentation]    FAIL    Keyword 'resource.Anarchy in the UK' expected 3 arguments, got 2.
    IF  'something' == 'thing'
       Anarchy in the UK    1    2
    END
    This is validated

Dryrun fail inside of ELSE IF
    [Documentation]    FAIL    Keyword 'resource.Anarchy in the UK' expected 3 arguments, got 1.
    IF  'total' == 'empty'
       Log  this is fine
    ELSE IF  'something' == 'thing'
       Anarchy in the UK    1
    ELSE
       Log  fine and dandy
    END
    This is validated

Dryrun fail inside of ELSE
    [Documentation]    FAIL    Keyword 'resource.Anarchy in the UK' expected 3 arguments, got 0.
    IF  'total' == 'empty'
       Log  this is fine
    ELSE
       Anarchy in the UK
    END
    This is validated

*** Keywords ***
Recursive if
    [Arguments]  ${arg}
    IF  '${arg}' == 'call again'
      Recursive if  call no more
    ELSE IF  '${arg}' == 'call sometimes'
      Log  no more calls
    ELSE
      Log  no more calls
    END

Recursive else if
    [Arguments]  ${arg}
    IF  '${arg}' == 'call no more'
      Log  no more calls
    ELSE IF  '${arg}' == 'call again'
      Recursive else if  call no more
    ELSE
      Log  no more calls
    END

Recursive else
    [Arguments]  ${arg}
    IF  '${arg}' == 'call no more'
      Log  no more calls
    ELSE IF  '${arg}' == 'call sometimes'
      Log  no more calls
    ELSE
      Recursive else  call no more
    END