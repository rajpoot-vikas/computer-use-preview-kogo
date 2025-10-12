# County Tax Website Data Dictionary
# Each entry contains one agency with parcel1 and parcel2

county_data_10_web = {
    1: {
        "agency_number": "210290000",
        "agency_name": "Bullitt County",
        "website": "http://ptax1.csiky.com/bullitt_current/",
        "parcel1": "069-000-00-036",
        "parcel2": "077-000-00-051C",
        "description": "unable bring the data",
        "payment_type": "Annual",
        "duration": "3.45 sec"
    },
    2: {
        "agency_number": "250131007",
        "agency_name": "Springfield City (Hampden)",
        "website": "https://mss.springfield-ma.gov/css/citizens/default.aspx",
        "parcel1": "111100208",
        "parcel2": "111100208",
        "parcel3": "111500006",
        "description": "Need to bring the data based installment number",
        "payment_type": "Semi Annual",
        "duration": "1.30 sec", 
        "Reason" : "working..."
    },
    3: {
        "agency_number": "180350000",
        "agency_name": "Delaware County",
        "website": "https://enoticesonline.com/dlw",
        "parcel1": "18-06-25-100-016.000-008",
        "parcel2": "18-07-33-426-010.000-003",
        "description": "Need to bring the data based installment number",
        "payment_type": "Semi Annual",
        "duration": "1.40 sec",
        "Reason" : "working... (after lots of prompt improvement.)"
        
    },
    4: {
        "agency_number": "211790000",
        "agency_name": "Nelson County",
        "website": "https://nelsonsheriff.com/wordpress/",
        "parcel1": "70000-00-063.21",
        "parcel2": "03000-00-014",
        "description": "Agent was not able click (Workflow execution failed: Deterministic step 2 (click) failed)",
        "payment_type": "Discount annual",
        "duration": "4:30 sec", 
        "reason": "not able to navigate after multiple prompt changes. "
    },
    5: {
        "agency_number": "340133003",
        "agency_name": "BloomfieldTownshipEssex_NJ",
        "website": "https://wipp.edmundsassoc.com/Wipp/?wippid=0702",
        "parcel1": "970-1-C9905",
        "parcel2": "970-1-C9904",
        "description": "Workflow execution failed: Invalid workflow inputs: 3 validation - Multiple boxes",
        "payment_type": "Quaterly",
        "duration": ".30sec", 
        "reason": "not working Multi box inputs"
    },
    6: {
        "agency_number": "180970000",
        "agency_name": "Marion County",
        "website": "https://www.indy.gov/workflow/property-taxes",
        "parcel1": "4038626",
        "parcel2": "4038627",
        "description": "Data is not getting",
        "payment_type": "Annual",
        "duration": "1.40 sec",
        "reason": "partially working, able to navigate till details page, but data filtering not happening"
    },
    7: {
        "agency_number": "212170000",
        "agency_name": "Taylor County",
        "website": "https://taylorcountyky.gov/sheriffs-department",
        "parcel1": "08-041",
        "parcel2": "13-010",
        "description": "Workflow execution failed: Deterministic step 1 (navigation) failed even after fallback",
        "payment_type": "Discount annual",
        "duration": "4:30 sec", 
        "reason": "Working fine"
    },
    8: {
        "agency_number": "181110000",
        "agency_name": "Newton County",
        "website": "https://payments.municipay.com/in_newton/search",
        "parcel1": "56-12-17-333-021.000-007",
        "parcel2": "56-12-18-441-040.000-007",
        "description": "GateWay Timeout",
        "payment_type": "",
        "duration": "5.14 sec", 
        "reason" : "request blocked"
    },
    9: {
        "agency_number": "290470000",
        "agency_name": "Clay County",
        "website": "https://collector.claycountymo.gov/ascend/(1bk4iq45uk42tx455knlsiql)/parcelinfo.aspx",
        "parcel1": "1918000200700",
        "parcel2": "1918000301100",
        "description": "Able to get the data",
        "payment_type": "Non Escrow",
        "duration": "1.52 sec", 
        "reason": "website not loading"
        
    },
    10: {
        "agency_number": "10740000",
        "agency_name": "Jefferson County Birmingham",
        "website": "https://eringcapture.jccal.org/propsearch",
        "parcel1": "09 00 27 3 000 098.001",
        "parcel2": "09 00 27 3 000 102.000",
        "description": "Able to get the data (parcel number missing)",
        "payment_type": "Annual",
        "duration": "2.10 sec", 
        "reason": " accesss denied "
    },
}



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
    }, 
}




new_county_data_next60_days = {

    2: {
        "website": "https://billpay.forte.net/howardcointreasurer/",
        "parcel": "34-03-24-276-001 000-002",
    },
    # 3: {
    #     "website": "https://www.indy.gov/agency/marion-county-treasurers-office",
    #     "parcel": "4038626",
    # },
    4: {
        "website": "https://richmondcountyga.governmentwindow.com/tax.html",
        "parcel": "012-0-019-22-0",
    },
    5: {
        "website": "https://enoticesonline.com/dlw",
        "parcel": "18-07-33-426-010.000-003",
    },
    6: {
        "website": "http://www.treasurer.maricopa.gov/",
        "parcel": "11139292 1",
    },
    7: {
        "website": "https://www.invoicecloud.com/portal/(S(g2irjykixzx5u33xd4qeyojo))/2/Site2.aspx?G=f92bbd52-0986-4971-8f81-6e44801f28d6",
        "parcel": "4038626",
        
    }
}


# Additional County Data - Mixed Status
county_data_mixed_status = {
    # Working entries
    1: {
        "agency_number": "171570000",
        "agency_name": "Randolph County IL",
        # "website": "https://randolphcountyil.gov/",
        "website": "https://www.govtechtaxpro.com/parceldetail.php",
        "parcel1": "18-104-014-00",
        "parcel2": "06-059-007-00",
        "status": "working fine",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    2: {
        "agency_number": "130590000",
        "agency_name": "Athens Clarke County",
        "website": "https://athensclarkecounty.governmentwindow.com/tax.html",
        "parcel1": "181 010C",
        "parcel2": "233A3 A045",
        "status": "caption not working",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    3: {
        "agency_number": "180890000",
        "agency_name": "Lake County IN",
        "website": "https://in-lake.publicaccessnow.com/PropertyTax/TaxSearch.aspx",
        "parcel1": "45-08-36-254-003.000-018",
        "parcel2": "",
        "status": "working",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    4: {
        "agency_number": "10890000",
        "agency_name": "Madison County AL",
        # "website": "http://madisoncountyal.gov",
        "website": "https://madisonproperty.countygovservices.com/Property/Property/Search",
        "parcel1": "14-09-32-2-000-046.000",
        "parcel2": "",
        "status": "working",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    5: {
        "agency_number": "60730000",
        "agency_name": "San Diego County",
        "website": "https://wps.sdttc.com/WebPayments/CoSDTreasurer2/search",
        "parcel1": "211-130-04-00",
        "parcel2": "",
        "status": "working",
        "reason": "",
        "state": None,
        "county": None,
        "year": 2025
    },
    
    # Partially working entries
    6: {
        "agency_number": "130510000",
        "agency_name": "Chatham County",
        "website": "https://www.chathamtax.org/PT/Search/Disclaimer.aspx?FromUrl=../search/commonsearch.aspx?mode=realprop",
        "parcel1": "20647 03004A",
        "parcel2": "",
        "status": "working",
        "reason": "",
        "state": None,
        "county": None,
        "year": 2025
        
    },
    20: {
        "agency_number": "180350000",
        "agency_name": "Delaware County IN",
        "website": "https://enoticesonline.com/dlw",
        "parcel1": "18-07-33-426-010.000-003",
        "parcel2": "",
        "status": "working",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    7: {
        "agency_number": "130890000",
        "agency_name": "DeKalb County GA",
        "website": "https://propertyappraisal.dekalbcountyga.gov/search/commonsearch.aspx?mode=realprop",
        "parcel1": "18 046 02 058",
        "parcel2": "",
        "status": "not working",
        "reason": "",
        "state": None,
        "county": None,
        "year": 2025
    },
    
    # Website blocked entries
    8: {
        "agency_number": "100030000",
        "agency_name": "New Castle DE",
        "website": "https://www.newcastlede.gov/232/Taxes",
        "parcel1": "901700035",
        "parcel2": "",
        "status": "website blocked",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    9: {
        "agency_number": "131210000",
        "agency_name": "Fulton County",
        "website": "https://www.fultoncountytaxes.org/",
        "parcel1": "14 -0045-0003-097-1",
        "parcel2": "",
        "status": "website blocked",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    10: {
        "agency_number": "170550000",
        "agency_name": "Franklin County IL",
        "website": "https://franklincountyil.gov/treasurers-office/",
        "parcel1": "12-19-409-005",
        "parcel2": "",
        "status": "website blocked",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    11: {
        "agency_number": "170770000",
        "agency_name": "Jackson County IL",
        "website": "https://jacksoncounty-il.gov/government/departments-i-z/treasurer",
        "parcel1": "15-20-277-023",
        "parcel2": "",
        "status": "website blocked",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    12: {
        "agency_number": "171490000",
        "agency_name": "Pike County IL",
        "website": "https://pikeil.devnetwedge.com/",
        "parcel1": "54-059-02B",
        "parcel2": "",
        "status": "website blocked",
        "reason": "your connection not private",
        "state": None,
        "county": None,
        "year": None
    },
    13: {
        "agency_number": "181270000",
        "agency_name": "Porter County IN",
        "website": "https://lowtaxinfo.com/portercounty/",
        "parcel1": "64-06-25-251-001.000-006",
        "parcel2": "",
        "status": "website blocked",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    
    # Other issues
    14: {
        "agency_number": "181110000",
        "agency_name": "Newton County IN",
        "website": "http://www.newtoncounty.in.gov/",
        "parcel1": "56-16-21-114-037.001-011",
        "parcel2": "",
        "status": "link not found",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    15: {
        "agency_number": "40150000",
        "agency_name": "Mohave County",
        "website": "https://www.mohave.gov/ContentPage.aspx?id=132",
        "parcel1": "R0184626",
        "parcel2": "",
        "status": "access is denied",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    16: {
        "agency_number": "40190000",
        "agency_name": "Pima County",
        "website": "https://www.to.pima.gov/home/#contactInfo",
        "parcel1": "223-02-036A",
        "parcel2": "",
        "status": "website blocked",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    
    # CAPTION entries (appears to be duplicate/special cases)
    17: {
        "agency_number": "180670000",
        "agency_name": "Howard County IN",
        "website": "https://billpay.forte.net/howardcointreasurer/",
        "parcel1": "34-03-24-276-001 000-002",
        "parcel2": "34-05-33-302-010.000-011",
        "status": "CAPTION",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    18: {
        "agency_number": "180970000",
        "agency_name": "Marion County IN",
        "website": "https://www.indy.gov/agency/marion-county-treasurers-office",
        "parcel1": "4038626",
        "parcel2": "",
        "status": "CAPTION",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    19: {
        "agency_number": "132450000",
        "agency_name": "Richmond County GA",
        "website": "https://richmondcountyga.governmentwindow.com/tax.html",
        "parcel1": "012-0-019-22-0",
        "parcel2": "",
        "status": "CAPTION",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
    
    # Not working entries

    21: {
        "agency_number": "40130000",
        "agency_name": "Maricopa County",
        "website": "http://www.treasurer.maricopa.gov/",
        "parcel1": "11139292 1",
        "parcel2": "",
        "status": "not working",
        "reason": "",
        "state": None,
        "county": None,
        "year": None
    },
}

# # Example usage:
# if __name__ == "__main__":
#     # Print all entries
#     for key, value in county_data.items():
#         print(f"\nEntry {key}:")
#         print(f"  Agency: {value['agency_name']}")
#         print(f"  Website: {value['website']}")
#         print(f"  Parcel 1: {value['parcel1']}")
#         print(f"  Parcel 2: {value['parcel2']}")
#         print(f"  Description: {value['description']}")
    
#     # Filter working entries
#     working_entries = {k: v for k, v in county_data.items() if "Able to get the data" in v['description']}
#     print(f"\n\nTotal agencies: {len(county_data)}")
#     print(f"Working agencies: {len(working_entries)}")
    
#     # Get specific agency
#     clay_county = county_data.get(9)
#     if clay_county:
#         print(f"\nClay County:")
#         print(f"  Parcel 1: {clay_county['parcel1']}")
#         print(f"  Parcel 2: {clay_county['parcel2']}")
