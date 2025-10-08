"""
Minimal sample function using Gemini to extract structured JSON data from page content.
"""
import os
import asyncio
import json
from typing import Dict, Any
from google import genai
from google.genai import types
import dotenv 
dotenv.load_dotenv() 

async def extract_structured_data_with_gemini(
    page_content: str,
    extraction_goal: str,
    fields: list[str]
) -> Dict[str, Any]:
    """
    Extract structured data from page content using Gemini API.
    
    Args:
        page_content: The HTML/Markdown content to extract from
        extraction_goal: What to extract from the page
        fields: List of field names to extract (e.g., ['parcel_number', 'owner_name', 'tax_amount'])
    
    Returns:
        Dictionary with extracted data in JSON format
    """
    # Configure Gemini API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    client = genai.Client(api_key=api_key)
    
    # Create prompt for structured extraction
    fields_list = ", ".join(fields)
    prompt = f"""
Your task is to extract specific information from the page content below.

Extraction Goal: {extraction_goal}

Fields to Extract: {fields_list}

Return ONLY a valid JSON object with these exact field names as keys.
If a field is not found, set its value to null.
Do not include any explanation or markdown formatting, just the raw JSON.

Page Content:
{page_content[:10000]}  # Limit content to avoid token limits

JSON Output:
"""
    
    try:
        # Generate content
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        # Parse JSON from response
        json_text = response.text.strip()
        # Remove markdown code blocks if present
        if json_text.startswith("```json"):
            json_text = json_text[7:]
        if json_text.startswith("```"):
            json_text = json_text[3:]
        if json_text.endswith("```"):
            json_text = json_text[:-3]
        
        extracted_data = json.loads(json_text.strip())
        return extracted_data
        
    except json.JSONDecodeError as e:
        print(f"⚠️  Failed to parse JSON: {e}")
        print(f"Raw response: {response.text}")
        # Return raw text as fallback
        return {"raw_content": response.text, "error": "Failed to parse JSON"}
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return {"error": str(e)}


# Example usage with property tax data extraction
async def main():
    # Sample page content (simulating what you'd get from markdownify)
    sample_content = """
    # Property Tax Information
    
    Parcel Number: 13-06-400-002
    Owner Name: John Doe
    Property Address: 123 Main Street, Springfield, IL
    Tax Year: 2024
    Assessed Value: $150,000
    Tax Amount: $3,250.00
    Tax Status: Paid
    Last Payment Date: 03/15/2024
    """
    
    # Define what fields to extract
    fields_to_extract = [
        "parcel_number",
        "owner_name", 
        "property_address",
        "tax_year",
        "assessed_value",
        "tax_amount",
        "tax_status",
        "last_payment_date"
    ]
    
    # Extract structured data
    result = await extract_structured_data_with_gemini(
        page_content=sample_content,
        extraction_goal="Extract property tax details from the page",
        fields=fields_to_extract
    )
    
    # Display results
    print("📊 Extracted JSON Data:")
    print(json.dumps(result, indent=2))
    
    return result


if __name__ == "__main__":
    # Run the async function
    asyncio.run(main())
