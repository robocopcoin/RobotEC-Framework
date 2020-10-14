*** Test Cases ***
Multiple keywords in if
   ${calculator}=  Set Variable  1
   IF  'kuu on taivaalla'
      ${calculator}=  Evaluate  1+${calculator}
      ${calculator}=  Evaluate  1+${calculator}
      ${calculator}=  Evaluate  1+${calculator}
   END
   Should be equal  ${calculator}  ${4}

Nested ifs
   ${calculator}=  Set Variable  1
   IF  'kuu on taivaalla taas'
      ${calculator}=  Evaluate  1+${calculator}
      IF  'sininen on taivas'
            ${calculator}=  Evaluate  3+${calculator}
      ELSE
            ${calculator}=  Evaluate  10+${calculator}
      END
      IF  ${False}
            ${calculator}=  Evaluate  2+${calculator}
      END
      ${calculator}=  Evaluate  1+${calculator}
   END
   Should be equal  ${calculator}  ${6}

If inside for loop
   ${outerval}=  Set Variable  wrong
   FOR  ${var}  IN  1  2  3
       IF  ${var} == 2
          ${outerval}=  Set Variable  ${var}
       END
   END
   Should be equal  ${outerval}  2

For loop inside if
   ${value}   Set Variable   0
   IF  'kaunis maailma'
        FOR  ${var}  IN  1  2  3
            ${value}=   Set Variable  ${var}
        END
   ELSE IF  'ei tanne'
        ${value}=  Set Variable  123
   END
   Should be equal  ${value}  3

For loop inside for loop
   ${checker}  Set Variable  wrong
   FOR  ${first}  IN  1  2  3
      FOR  ${second}  IN  4  5  6
          ${checker}  Set Variable  ${first} - ${second}
      END
   END
   Should be equal  ${checker}  3 - 6

Direct Boolean condition
   [Documentation]  PASS From the condition
   IF  ${True}
      Pass Execution  From the condition
   END
   Fail  condition not working

Direct Boolean condition false
   IF  ${False}
      Fail  should not execute
   END