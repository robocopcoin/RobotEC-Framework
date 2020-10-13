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
   IF  'kuu on taivaalla'
      ${calculator}=  Evaluate  1+${calculator}
      IF  'sininen on taivas'
            ${calculator}=  Evaluate  1+${calculator}
      END
      ${calculator}=  Evaluate  1+${calculator}
   END
   Should be equal  ${calculator}  ${4}

If inside for loop
   FOR  ${var}  IN  1  2  3
       IF  ${var} == 3
          Pass Execution   condition should be met
       END
   END
   Fail  condition not met

For loop inside if
   ${value}   Set Variable   0
   IF  'kaunis maailma'
        FOR  ${var}  IN  1  2  3
            ${value}=   Set Variable  ${var}
        END
   END
   Should be equal  ${value}  3

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