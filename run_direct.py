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
from user_prompt import USER_FLEXIBLE_PROMPT
import dotenv
import sys
dotenv.load_dotenv()

PLAYWRIGHT_SCREEN_SIZE = (1200, 800)

ENV = "playwright"  # Options: "playwright" or "browserbase"
HIGHLIGHT_MOUSE = False
MODEL = "gemini-2.5-computer-use-preview-10-2025"


data_web = {
    1: {
        "website": "https://ca-solano.publicaccessnow.com/TaxCollector/TaxSearch.aspx",
        "parcel": "0174-040-050"
    },
    2: {
        "website": "https://beacon.schneidercorp.com/Application.aspx?App=MenardCountyIL&PageType=Search",
        "parcel": "13-06-400-002"
    },
    3: {
        "website": "https://www.to.pima.gov/propertyInquiry/",
        "parcel": "136074070"
    },
    4: {
        "website": "https://county-taxes.net/fl-lee/property-tax",
        "parcel": "094725E33703B0000"
    },
    5: {
        "website": "https://www.sbcountyatc.gov/tax-services/property-tax",
        "parcel": "0229-121-50-0000"
    },
    6: {
        "website": "https://qpublic.schneidercorp.com/Application.aspx?App=HonoluluCountyHI&PageType=Search",
        "parcel": "110050460000"
    },
    7: {
        "website": "https://www.ncpub.org/_Web/datalets/datalet.aspx?mode=profile_nh&sIndex=1&idx=1&LMparent=20",
        "parcel": "M7 2 17A 0204",
        "fun" : "not working"
    },
    8: {
        "website": "https://propertytax.alamedacountyca.gov/",
        "parcel": "55-1872-11", 
        "fun" : "not working"
    },
    9: {
        "website": "https://county-taxes.net/ca-sanfrancisco/property-tax",
        "parcel": "0339 019"
    },
    10: {
        "website": "https://common3.mptsweb.com/mbc/sonoma/tax/search",
        "parcel": "125-700-005-000"
    },
    11: {
        "website": "https://nv-washoe.publicaccessnow.com/Treasurer/TaxSearch.aspx",
        "parcel": "2128102"
    },
    12: {
        "website": "https://www.cobbtaxpayments.org/#/WildfireSearch",
        "parcel": "16008900320"
    },
    13: {
        "website": "https://actweb.acttax.com/act_webdev/galveston/index.jsp",
        "parcel": "613635"
    },
    14: {
        "website": "https://actweb.acttax.com/kaufman/kaufman/index.jsp",
        "parcel": "43888",
        "fun" : "not working",
        "reason" : "not able the select the search type parcel id."
    },
    15: {
        "website": "https://tax.wilcotx.gov/",
        "parcel": "R612317"
    },
    16: {
        "website": "https://property.guadalupetx.gov/",
        "parcel": "05193-450-0220"
    },
    17: {
        "website": "https://propertytax.alamedacountyca.gov/",
        "parcel": "55-1872-11"
    },
    18: {
        "website": "https://treapropsearch.franklincountyohio.gov/Default.aspx",
        "parcel": "010-106301-00"
    },
    19: {
        "website": "https://trweb.co.clark.nv.us/",
        "parcel": "176-34-612-004"
    },
    20: {
        "website": "https://auditor.lakecountyohio.gov/search/commonsearch.aspx?mode=realprop",
        "parcel": "19A092R000810"
    },
    21: {
        "website": "https://propertysearch.bcohio.gov/search/commonsearch.aspx?mode=parid",
        "parcel": "A0700006000109"
    },
    22: {
        "website": "https://auditor.greenecountyohio.gov/Search/Number",
        "parcel": "A02000100110011400"
    },
    23: {
        "website": "https://www.hctax.net/Property/PropertyTax",
        "parcel": "420860000066",
        "fun" : "not working"
        
    },
    24: {
        "website": "https://www.invoicecloud.com/portal/(S(ch0oks30dlfo3man4fu2n5fo))/2/customerlocator.aspx?iti=8&bg=df4c9b56-182b-4199-b0db-f20392ea18e0&vsii=1",
        "parcel": "T17905",
        "fun" : "not working: not moving forward after the "
        
    },
    25: {
        "website": "https://ipn.paymentus.com/rotp/HNPN",
        "parcel": "0602724240008"
    }
}

data_web_1 = {
    26: {
        "website": "https://enoticesonline.com/dlw",
        "parcel": "18-06-25-100-016.000-008", 
        "description": "working fine" 
    },
    27: {
        "website": "http://ptax1.csiky.com/bullitt_current/",
        "parcel": "069-000-00-036",
        "reason" : "scroll is not done"
    },
    28: {
        "website": "https://nelsonsheriff.com/wordpress/",
        "parcel": "70000-00-063.15",
        "description": "working fine" 
    },
    29: {
        "website": "https://wipp.edmundsassoc.com/Wipp/?wippid=0702",
        "parcel": "970-1-C9905", 
        "reason" : "multiple inputs: Block, Lot, Qual"
    },
    30: {
        "website": "https://www.indy.gov/workflow/property-taxes",
        "parcel": "4038626",
        "reason" : "Partially Not working."
    },
    31: {
        # "website": "https://taylorcountyky.gov/sheriffs-department",
        "website": "https://view.properlytaxes.com/taxbillsearch/site/47",
        "parcel": "08-041", 
        "reason": "not working..."
    },
    32: {
        "website": "https://payments.municipay.com/in_newton/search",
        "parcel": "56-12-17-333-021.000-007", 
        "reason": "request blocked"
    },
    33: {
        "website": "https://collector.claycountymo.gov/ascend/(1bk4iq45uk42tx455knlsiql)/parcelinfo.aspx",
        "parcel": "1918000200700",
        "reason": "error log"
    },
    34: {
        "website": "https://eringcapture.jccal.org/propsearch",
        "parcel": "09 00 27 3 000 098.001", 
        "reason": "access is denied"
    }
}



# index = 11

def run(initial_url: str, parcel_number: str, search_year: str) -> int:
    """
    Run the browser agent with predefined configuration variables.
    Modify the variables at the top of this file to change behavior.
    """
    query = USER_FLEXIBLE_PROMPT.format(parcel_number=parcel_number, search_year=search_year)
    
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
    index = 34
    print(f" \033[92m STARTING OF NEW RECORDING INDEX {index} \033[0m")

    initial_url = data_web_1[index]["website"] 
    parcel_number = data_web_1[index]["parcel"] 
    search_year = "2024"
    
    run(initial_url, parcel_number, search_year)


