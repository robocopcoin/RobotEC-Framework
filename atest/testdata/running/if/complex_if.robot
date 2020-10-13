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

Direct Boolean condition
   IF  ${True}
      Pass Execution  From the condition
   END
   Fail  condition not working

Direct Boolean condition false
   IF  ${False}
      Fail  should not execute
   END
