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
