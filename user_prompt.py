USER_MAIN_PROMPT = """**Objective:**  
Automate the process of searching for parcel information using a parcel number on tax website with resilience to page variations, pop-ups, agreements, and modal dialogs.

**Steps:**

1. **Page Preparation**
   - Wait for the main search interface to fully load.  
   - Detect and handle any overlays, modals, or pop-up agreements (such as disclaimers, terms of service, or consent dialogs) by interacting with 'Agree', 'Accept', or similarly labeled buttons, ensuring the search input is accessible.

2. **Select Year (if required) and Enter Parcel Number**
   - Check if a 'Year', 'Tax Year', 'Tax Roll', or similar selector (dropdown, radio buttons, tabs) is present and required to enable the search.
   - If present, select the year : {search_year} first. Prefer the latest or default year when no explicit instruction is given.
   - After selecting the year, wait for the form to refresh or inputs to become enabled.
   - Locate the search field designated for parcel numbers.
   - Enter the provided parcel number: {parcel_number}.
   - If multiple search fields are present, ensure the correct one is selected (e.g., labeled as "Parcel Number", "Parcel ID", or similar).
   - Edge case: If selecting the year clears or resets the parcel field, re-enter {parcel_number}.

3. **Trigger Search Action**
   - Identify and click the appropriate search or submit button, which may be labeled "Search," "Go," or contain a similar action term.
   - If the button is disabled, verify that both the year (when required) and parcel number are set, then retry.
   - Wait for the search results section to load fully (use explicit waits for content, results, or the "loading" indicator to disappear).
   - Handle edge case: If button click fails, try pressing 'Enter' key in search field as alternative

4. **Handle Unexpected Dialogs and Popups**
   - Monitor for any unexpected pop-ups, error messages, or information dialogs throughout the process.
   - If such elements appear (e.g., session warnings, information/disclaimer popups, or modal overlays), interact with them to dismiss, continue, or agree, as appropriate.

4a. **Disambiguate Multiple Results**
    - If the search yields multiple results, scan the results list for the entry matching the exact parcel number {parcel_number}.
    - Programmatically identify and click the corresponding "View Details," "Select," or equivalent action button/link for that specific parcel.
    - Ensure navigation proceeds only after confirming the correct parcel has been selected and the details page is loading.

5. **Access Parcel Details**
   - Once the results are visible, find and click the link or button to view the details for parcel number {parcel_number}.
   - If multiple results appear, match the exact parcel number before proceeding.

6. **Navigation & Finalization**
   - Confirm successful navigation by waiting for the parcel details page or section to load.
   - Verify that the detailed parcel information for {parcel_number} is visible and accessible, indicating the workflow’s success.

**General Robustness Considerations:**
- Use flexible selectors and timeout/retry logic to account for variable load times and layout changes.
- Include error handling for missing fields, timeouts, or site maintenance notifications.
- Prefer the latest available year when a year must be selected and no explicit year is provided.
- Re-validate that both year (if required) and parcel inputs are set before attempting search.
- Log each step and any exceptional events (e.g., repeated modals, search failures, multiple matches).
"""

USER_MINIMAL_PROMPT = """
Objective:
Retrieve parcel details for {parcel_number} using the fewest possible interactions.

Principles:
- Do only what is strictly necessary to complete the search.
- Prefer defaults; change settings only if required to enable search.
- Minimize clicks/keystrokes and page traversals.
- Dismiss blocking elements only when they prevent interaction.

Steps:
1. Wait until the search interface is usable (inputs enabled, not covered by overlays).
2. If search requires a year selection to enable input or search, set it to {search_year}; otherwise leave the default.
3. If a search type selector is present (e.g., Parcel/Parcel ID, Property ID, Account/Account ID, Account Number, ID, Owner), choose the option that corresponds to parcel/account identification (typically labeled as "Parcel", "Parcel ID", "Account", "Account ID", "Account Number", "ID", or similar).
4. Enter {parcel_number} in the parcel/account input field. The field may be labeled as "Parcel Number",  "Property ID", "Parcel ID", "Account Number", "Account ID", "ID", or similar variations. If year selection clears it, re-enter once.
5. Trigger the search using the primary search button; if not clickable, press Enter in the input.
6. If multiple results appear, choose the exact match for {parcel_number} (which may be displayed as parcel number, account number, account ID, or ID) with a single click.
7. Open the parcel details if needed and stop once the details page/section is visible.

Minimal robustness:
- Use generic, resilient selectors; retry each critical action once.
- If a modal/overlay blocks interaction, click a single Agree/Accept/Close action to proceed.
- Use short explicit waits for visibility/enablement;
- Do not open new tabs or navigate elsewhere unless the site forces it.
- Log only brief outcomes of each step.
"""

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
