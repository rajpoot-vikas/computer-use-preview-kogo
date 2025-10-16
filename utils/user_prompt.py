OHC_PROMPT = """   
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
   
"""


# OHC_PROMPT = """
#    Follow these steps to generate a report for a given part number.

#    **Part Number**: {part_number}

#    **Instructions**:

#    1.  **Login**:
#       *   Username: `crd8u01`
#       *   Password: `aircraft1!$!`

#    2.  **Set Condition Codes**:
#       *   Ensure the following condition code checkboxes are all checked: `NE`, `NS`, `OH`, `SV`, `AR`.
#       *   If any are unchecked, check them.

#    3.  **Search for Part Number**:
#       *   Locate the input field for `Item 01`.
#       *   Enter the part number `{part_number}` into this field and initiate the search.

#    4.  **Navigate to Pricing**:
#       *   Click on the "Parts Stats & Pricing" tab.

#    5.  **Select Part**:
#       *   In the table, find the row that exactly matches the part number `{part_number}`.
#       *   Click exactly on the square checkbox `[]`

#    6.  **Create Report**:
#       *   Click the "Create Report" button to proceed to the next page.
   # step 7. Logout By click the button on the top right.

# """



# # 7.  **Logout**:
# #    *   Click the logout button located at the top right of the page.

# # new =  """# Item *	Part Number, Keyword or NSN * 

# #    """


