OHC_PROMPT = """

step 1 :
   
step 1. Login using the given creds : 
   Id : crd8u01
   password : aircraft1!$!
   
2. Ensure all the condition codes are checked :  
   - Condition Codes *: NE, NS, OH, SV, AR
   - if any of it unchecked please check it. 

step 3. search using the Part Number :  {part_number}
      Only use the Input box corresponding to the Item 01.

step 4. navigate to the : Parts Stats & Pricing tab. 

step 5. click on check box (click exactly on the square box []) which is exact match to the Part No. {part_number}

step 6. click on the Create Report Button and navigate to next page. 
step 7. Logout By click the button on the top right.
"""


# new =  """# Item *	Part Number, Keyword or NSN * 

#    """