Goal : "This workflow navigates to a real property tax data page, searches using a parcel number, views parcel details.",
Steps : 
1. "Navigate to the real property search page.",
2. "Open the Parcel search tab.",
3. "Enter the parcel number to search for property details.",
4. "Submit the search for the parcel details.",
5. "View property details from search results.",
6. "Access the Tax Detail section of the property.",



python run_direct.py | tee run_direct.log 

python run_direct.py 2>&1 | tee ./data/logs/run_direct.log 

https://www.actdatascout.com/RealProperty/Arkansas/Izard






1. "Select the tax year from the dropdown.",
2. "Select 'Parcel Number' as the search type.",
3. "Input the parcel number to search for.",
4. "Click the search button to start the search.",
5. "The search results are dynamic and can change. Use an agent to ensure it clicks the correct 'View Details/Pay' button.",


1. "Input the parcel number to search. 'parcel number' == 0174040050 ",
2. "Submit the parcel number search.",
3. "The search may return multiple results, requiring click of the correct one. and reach final page",




"Workflow to search and retrieve property tax details using a parcel number in Menard County, IL. The workflow navigates to the search page, inputs the parcel number, performs the search, and extracts tax details.",
"Navigate to Menard County property search page.",

1. "Input the parcel number into the search field.",
2. "Click the search button to execute the parcel ID search.",
3. "Navigate to the property tax details page.",


Here is an improved and more robust prompt for automating the workflow of searching for real property tax data by parcel number on the Beacon Menard County, IL website. This version ensures that edge cases—such as popups, loaders, agreements, modal dialogs, or navigation issues—are handled gracefully:

***



**Robust Automation Workflow: Real Property Tax Search by Parcel Number**

**Objective:**  
Automate the process of searching for parcel information using a parcel number on tax website with resilience to page variations, pop-ups, agreements, and modal dialogs.

**Steps:**

1. **Page Preparation**
   - Wait for the main search interface to fully load.  
   - Detect and handle any overlays, modals, or pop-up agreements (such as disclaimers, terms of service, or consent dialogs) by interacting with 'Agree', 'Accept', or similarly labeled buttons, ensuring the search input is accessible.

2. **Searching by Parcel Number**
   - Locate the search field designated for parcel numbers.  
   - Enter the provided parcel number: **13-06-400-002**.  
   - If multiple search fields are present, ensure the correct one is selected (e.g., labeled as "Parcel Number", "Parcel ID", or similar).

3. **Trigger Search Action**
   - Identify and click the appropriate search or submit button, which may be labeled "Search," "Go," or contain a similar action term.  
   - Wait for the search results section to load fully (use explicit waits for content, results, or the "loading" indicator to disappear).
   - Handle edge case: If button click fails, try pressing 'Enter' key in search field as alternative


4. **Handle Unexpected Dialogs and Popups**
   - Monitor for any unexpected pop-ups, error messages, or information dialogs throughout the process.
   - If such elements appear (e.g., session warnings, information/disclaimer popups, or modal overlays), interact with them to dismiss, continue, or agree, as appropriate.

4a. **Disambiguate Multiple Results**
    - If the search yields multiple results, scan the results list for the entry matching the exact parcel number **13-06-400-002**.
    - Programmatically identify and click the corresponding "View Details," "Select," or equivalent action button/link for that specific parcel.
    - Ensure navigation proceeds only after confirming the correct parcel has been selected and the details page is loading.

5. **Access Parcel Details**
   - Once the results are visible, find and click the link or button to view the details for parcel number **13-06-400-002**.
   - If multiple results appear, match the exact parcel number before proceeding.

6. **Navigation & Finalization**
   - Confirm successful navigation by waiting for the parcel details page or section to load.
   - Verify that the detailed parcel information for **13-06-400-002** is visible and accessible, indicating the workflow’s success.

**General Robustness Considerations:**
- Use flexible selectors and timeout/retry logic to account for variable load times and layout changes.
- Include error handling for missing fields, timeouts, or site maintenance notifications.
- Log each step and any exceptional events (e.g., repeated modals, search failures, multiple matches).

