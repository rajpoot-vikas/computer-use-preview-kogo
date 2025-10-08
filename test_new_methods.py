"""
Test script to demonstrate the new PlaywrightComputer methods:
- get_data_from_last_page()
- save_last_page_as_pdf()
"""
import os
from computers import PlaywrightComputer
import json
import dotenv
dotenv.load_dotenv()

PLAYWRIGHT_SCREEN_SIZE = (1200, 800)

def test_extraction_and_pdf():
    """Test data extraction and PDF saving functionality."""
    
    # Create browser instance
    with PlaywrightComputer(
        screen_size=PLAYWRIGHT_SCREEN_SIZE,
        initial_url="https://myplace.cuyahogacounty.gov/",
        highlight_mouse=False,
    ) as browser:
        
        print("\n" + "="*60)
        print("Testing PlaywrightComputer Methods")
        print("="*60)
        
        # Wait for page to load
        browser.wait_5_seconds()
        
        import time
        time.sleep(15)
        
        
        # Test 1: Extract all content (no fields specified)
        print("\n📋 Test 1: Extract page content without specific fields")
        data = browser.get_data_from_last_page(
            extraction_goal="Extract general page information"
        )
        print(f"Result keys: {list(data.keys())}")
        print(f"Content length: {len(data.get('content', ''))}")
        
        # Test 2: Extract structured data with specific fields
        print("\n📋 Test 2: Extract structured data with specific fields")
        fields_to_extract = [
            "page_title",
            "search_options",
            "county_name",
            "available_search_types"
        ]
        
        structured_data = browser.get_data_from_last_page(
            extraction_goal="Extract search page information and available options",
            fields=fields_to_extract
        )
        print("Extracted structured data:")
        print(json.dumps(structured_data, indent=2))
        
        # Test 3: Save page as PDF
        print("\n📋 Test 3: Save current page as PDF")
        pdf_result = browser.save_last_page_as_pdf(
            file_path="./data/pdfs/test_page.pdf",
            return_base64=False
        )
        print("PDF save result:")
        print(json.dumps(pdf_result, indent=2))
        
        # Test 4: Save PDF with base64 encoding
        print("\n📋 Test 4: Save PDF with base64 encoding")
        pdf_with_base64 = browser.save_last_page_as_pdf(
            file_path="./data/pdfs/test_page_base64.pdf",
            return_base64=True
        )
        print(f"PDF saved with base64: {pdf_with_base64.get('success')}")
        print(f"Base64 length: {len(pdf_with_base64.get('base64', ''))}")
        
        print("\n" + "="*60)
        print("All tests completed!")
        print("="*60)


if __name__ == "__main__":
    # Check if GEMINI_API_KEY is set
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Warning: GEMINI_API_KEY not set. Structured extraction will fallback to raw content.")
        print("   Set it with: export GEMINI_API_KEY='your-api-key'\n")
    
    test_extraction_and_pdf()
