# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from agent import BrowserAgent
from computers import BrowserbaseComputer, PlaywrightComputer
from user_prompt import USER_FLEXIBLE_STATE_COUNTY_PROMPT
import dotenv
import sys
dotenv.load_dotenv()

from county_data_dict import county_data_10_web, new_county_data_next60_days, county_data_mixed_status

PLAYWRIGHT_SCREEN_SIZE = (1366, 1400)


ENV = "playwright"  # Options: "playwright" or "browserbase"
HIGHLIGHT_MOUSE = False
MODEL = "gemini-2.5-computer-use-preview-10-2025"





# index = 11

def run(initial_url: str, parcel_number: str, search_year: str, state: str, county: str) -> int:
    """
    Run the browser agent with predefined configuration variables.
    Modify the variables at the top of this file to change behavior.
    """
    query = USER_FLEXIBLE_STATE_COUNTY_PROMPT.format(
        parcel_number=parcel_number, 
        search_year=search_year,
        state=state,
        county=county
    )
    
    # print(f"Running browser agent with query: {query}") 
    # print(f"Environment: {ENV}")
    print("-" * 50)
    print(f"Initial URL: {initial_url}")
    print("-" * 50)
    # print(f"Model: {MODEL}")
    # print("-" * 50)

    if ENV == "playwright":
        env = PlaywrightComputer(
            screen_size=PLAYWRIGHT_SCREEN_SIZE,
            initial_url=initial_url,
            highlight_mouse=HIGHLIGHT_MOUSE,
        )
    elif ENV == "browserbase":
        env = BrowserbaseComputer(
            screen_size=PLAYWRIGHT_SCREEN_SIZE,
            initial_url=initial_url
        )
    else:
        raise ValueError(f"Unknown environment: {ENV}")

    with env as browser_computer:
        agent = BrowserAgent(
            browser_computer=browser_computer,
            query=query,
            model_name=MODEL,
        )
        agent.agent_loop()
    return 0


if __name__ == "__main__":
    # Get index from command line argument, default to 1
    # global index
    # for index in range(25, 26):
    print("\n\n\n\n") 
    print("#"*100) 
    print("#"*100) 
    index = 20
    print(f" \033[92m STARTING OF NEW RECORDING INDEX {index} \033[0m") 

    initial_url = county_data_mixed_status[index]["website"] 
    parcel_number = county_data_mixed_status[index]["parcel1"] 
    search_year = county_data_mixed_status[index]["year"] 
    state = county_data_mixed_status[index]["state"]  # Or get from your data source
    county = county_data_mixed_status[index]["county"]  # Or get from your data source
    
    run(initial_url, parcel_number, search_year, state, county)

    print("#"*100) 
    print("#"*100) 

 
