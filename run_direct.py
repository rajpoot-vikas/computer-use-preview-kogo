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
import dotenv
dotenv.load_dotenv()

PLAYWRIGHT_SCREEN_SIZE = (1200, 800)


# Configuration variables - modify these as needed
# QUERY = "Search for Python tutorials on Google"
QUERY = """
        Goal : "This workflow navigates to a real property tax data page, searches using a parcel number, views parcel details.",
        Steps : 
            1. "Input the parcel number into the search field. 'parcel number' == 13-06-400-002 ",
            2. "Click the search button to execute the parcel ID search.",
            3. "Then successfully navigate to the next page",
"""

ENV = "playwright"  # Options: "playwright" or "browserbase"
INITIAL_URL = "https://beacon.schneidercorp.com/Application.aspx?App=MenardCountyIL&PageType=Search"
HIGHLIGHT_MOUSE = False
MODEL = "gemini-2.5-computer-use-preview-10-2025"


def main() -> int:
    """
    Run the browser agent with predefined configuration variables.
    Modify the variables at the top of this file to change behavior.
    """
    print(f"Running browser agent with query: {QUERY}")
    print(f"Environment: {ENV}")
    print(f"Initial URL: {INITIAL_URL}")
    print(f"Model: {MODEL}")
    print("-" * 50)

    if ENV == "playwright":
        env = PlaywrightComputer(
            screen_size=PLAYWRIGHT_SCREEN_SIZE,
            initial_url=INITIAL_URL,
            highlight_mouse=HIGHLIGHT_MOUSE,
        )
    elif ENV == "browserbase":
        env = BrowserbaseComputer(
            screen_size=PLAYWRIGHT_SCREEN_SIZE,
            initial_url=INITIAL_URL
        )
    else:
        raise ValueError(f"Unknown environment: {ENV}")

    with env as browser_computer:
        agent = BrowserAgent(
            browser_computer=browser_computer,
            query=QUERY,
            model_name=MODEL,
        )
        agent.agent_loop()
    return 0


if __name__ == "__main__":
    main()