

USER_FLEXIBLE_PROMPT = """
**Objective:**
Flexibly navigate diverse tax websites to find and view parcel details for {parcel_number}, and then locate the tax/payment information. This may require a sequence of actions for a single logical step.

**Core Principles:**
- **Adaptability:** Assume websites vary. Adapt to different layouts, labels, and multi-step workflows.
- **Resilience:** Handle common web obstacles like pop-ups, varied navigation, and search result formats.

**Workflow Steps:**

1.  **Navigate to Search Portal (If Necessary):**
   - **Goal:** Reach the property search form from the landing page.
   - **Condition:** Perform this step only if the initial page does not contain a search form.
   - **Actions:**
      - Scan the page for navigation elements like menus, buttons, or links with keywords such as "Search," "Property," "Tax," "Parcel," or "Assessments."
      - This may be a multi-step process. you may need to click on buttons multiple time. 
      - Continue clicking through relevant links until you arrive at a page containing the search form (i.e., a page with input fields for parcel number, address, etc.).
   - **Note:** If the initial page is already the search portal, skip this step and proceed to Step 2, and also don't do more then 5 action/steps to complete this step.
   
2.  **Prepare the Search Form:**
   - **Goal:** Make the search form accessible and ready for input.
   - **Actions:** Wait for the page to load. Dismiss any initial overlays, disclaimers, or cookie banners by clicking "Accept," "Agree," "OK," or a close icon ('X'). This might be a multi-step process if there are several modals.

3.  **Configure Search Criteria:**
   - **Goal:** Correctly set all required fields before searching.
   - **Actions:**
    - **Search Type:** If a choice is offered (e.g., "By Parcel," "By Owner"), select the option for "Parcel Number," "Account ID," or a similar identifier.
    - **Year Selection:** If a tax year selector is present, set it to `{search_year}`.
    - **Parcel Input:** Locate the input field (e.g., "Parcel Number," "Account Number," "Property ID", "MAP NUMBER"). Enter `{parcel_number}`.
    - **Self-Correction:** If any selection (like year or search type) clears other fields, re-enter the necessary information. Ensure all required fields are correctly populated before proceeding.

4.  **Execute Search:**
   - **Goal:** Trigger the search and wait for results.
   - **Actions:** Click the "Search" or "Submit" button. If that fails or is not available, press the 'Enter' key in the parcel number input field as an alternative. Wait for the results to load.

5.  **Process Search Outcome:**
   - **Goal:** Navigate from the search outcome to the specific parcel's tax information.
   - **Scenario A: List of Results:** If the search displays a list of results, scan for an exact match of `{parcel_number}`. Click the corresponding link or button (e.g., "View Details," "Select," or the parcel number itself) to open the details page.
   - **Scenario B: Direct to Details:** If the search leads directly to a parcel details page, this step is complete.
   - **Scenario C: No Results:** If no results are found, the task is complete with a "not found" status.

6.  **Locate Tax Information:**
   - **Goal:** From the parcel details page, find the section or page with tax payment information.
   - **Actions:** First, check if tax information (like "Amount Due", "Total Tax", "Taxes Payable") is already visible on the current page. If it is, this step is complete. If not, look for and click on links, tabs, or buttons labeled "Taxes", "Tax Bill", "Payments", "Amount Due", "Payable", "Billing", or similar terms to navigate to the tax information page. This may require navigating through one or more pages.

7.  **Confirm and Finalize:**
   - **Goal:** Verify that the page containing tax due information is displayed.
   - **Actions:** Wait for the tax/payment page to load. Once a page containing terms like "Amount Due", "Total Tax", "Taxes Payable", or similar financial details for the correct parcel is visible, the task is successfully completed. Do not perform any further actions.

"""




USER_FLEXIBLE_STATE_COUNTY_PROMPT = """
**Objective:**
Flexibly navigate diverse tax websites to find and view parcel details for {parcel_number} for a given {state} and {county}, and then locate the tax/payment information. This may require a sequence of actions for a single logical step.

**Core Principles:**
- **Adaptability:** Assume websites vary. Adapt to different layouts, labels, and multi-step workflows.
- **Resilience:** Handle common web obstacles like pop-ups, varied navigation, and search result formats.
- **Site Constraint**: Remain on the provided website domain. Do not navigate to external sites like Google to find information.
- **Failure Condition**: If tax information cannot be located after following all relevant steps, conclude the task with a "not found" status.
- **State-Change Verification**: After performing an action (like a click), verify that the page state has changed. If it hasn't, retry the action once.



**Workflow Steps:**

1.  **Navigate to Search Portal (If Necessary):**
   - **Goal:** Reach the property search form from the landing page.
   - **Condition:** Perform this step only if the initial page does not contain a search form.
   - **Actions:**
      - Scan the page for navigation elements like menus, buttons, or links with keywords such as "Search," "Property," "Tax," "Parcel," or "Assessments."
      - This may be a multi-step process. you may need to click on buttons multiple time. 
      - Continue clicking through relevant links until you arrive at a page containing the search form (i.e., a page with input fields for parcel number, address, etc.).
   - **Note:** If the initial page is already the search portal, skip this step and proceed to Step 2, and also don't do more then 5 action/steps to complete this step.
   
2.  **Prepare the Search Form:**
   - **Goal:** Make the search form accessible and ready for input.
   - **Actions:** Wait for the page to load. Dismiss any initial overlays, disclaimers, or cookie banners by clicking "Accept," "Agree," "OK," or a close icon ('X'). This might be a multi-step process if there are several modals.

3.  **Configure Search Criteria:**
   - **Goal:** Correctly set all required fields before searching.
   - **Actions:**
    - **State Selection:** If a state selector is present and `{state}` is not 'None', select `{state}`.
    - **County Selection:** If a county selector is present and `{county}` is not 'None', select `{county}`.
    - **Search Type:** If a choice is offered (e.g., "By Parcel," "By Owner"), select the option for "Parcel Number," "Account ID," or a similar identifier.
    - **Year Selection:** If a tax year selector is present, set it to `{search_year}`.
    - **Parcel Input:** Locate the input field (e.g., "Parcel Number," "Account Number," "Property ID", "MAP NUMBER"). Enter `{parcel_number}`.
    - **Self-Correction:** If any selection (like year or search type) clears other fields, re-enter the necessary information. Ensure all required fields are correctly populated before proceeding.

4.  **Execute Search:**
   - **Goal:** Trigger the search and wait for results.
   - **Actions:** Click the "Search" or "Submit" button. If that fails or is not available, press the 'Enter' key in the parcel number input field as an alternative. Wait for the results to load.

5.  **Process Search Outcome:**
   - **Goal:** Navigate from the search outcome to the specific parcel's tax information.
   - **Scenario A: List of Results:** If the search displays a list of results, scan for an exact match of `{parcel_number}`. Click the corresponding link or button (e.g., "View Details," "Select," or the parcel number itself) to open the details page.
   - **Scenario B: Direct to Details:** If the search leads directly to a parcel details page, this step is complete.
   - **Scenario C: No Results:** If no results are found, the task is complete with a "not found" status.

6.  **Locate Tax Information:**
   - **Goal:** From the parcel details page, find the section or page with tax payment information.
   - **Actions:** First, check if tax information (like "Amount Due", "Total Tax", "Taxes Payable") is already visible on the current page. If it is, this step is complete. If not, look for and click on links, tabs, or buttons labeled "Taxes", "Tax Bill", "Payments", "Amount Due", "Payable", "Billing", or similar terms to navigate to the tax information page. This may require navigating through one or more pages.

7.  **Confirm and Finalize:**
   - **Goal:** Verify that the page containing tax due information is displayed.
   - **Actions:** Wait for the tax/payment page to load. Once a page containing terms like "Amount Due", "Total Tax", "Taxes Payable", or similar financial details for the correct parcel is visible, the task is successfully completed. Do not perform any further actions.

"""
