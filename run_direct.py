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
from utils.user_prompt import OHC_PROMPT
import dotenv
import sys
dotenv.load_dotenv()

from utils.county_data_dict import county_data_10_web, new_county_data_next60_days, new_data_o13

PLAYWRIGHT_SCREEN_SIZE = (1366, 1400)


ENV = "playwright" 
HIGHLIGHT_MOUSE = True
MODEL = "gemini-2.5-computer-use-preview-10-2025"

def run(initial_url: str, part_no: str, ) -> int:
    """
    Run the browser agent with predefined configuration variables.
    Modify the variables at the top of this file to change behavior.
    """
    query = OHC_PROMPT.format(
        part_number=part_no, 
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
            record_video=True,
            parcel_number=part_no
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
    
    initial_url = "https://static.ilsmart.com/pages/ilslogin.htm"
    # part_no = "521100"
    part_no = "4383121"
 
    run(initial_url, part_no)

    print("#"*100) 


