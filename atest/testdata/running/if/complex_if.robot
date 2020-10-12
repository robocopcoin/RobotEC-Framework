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

