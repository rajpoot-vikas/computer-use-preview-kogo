from openai import AsyncOpenAI
import dotenv
import asyncio
from typing import AsyncGenerator, List, Optional, Dict
import os 
import logging
import json
dotenv.load_dotenv()  # Load environment variables from .env

# Use centralized logger
logger = logging.getLogger(__name__)

from common.data_extraction_prompt import EXTRACTION_PROMPT_V3

SYSTEM_PROMPT = """ 
    You are expert in the data filtring and responding in the json format.
"""


default_config = {
    "api_key": os.environ.get("OPENAI_API_KEY"),
    "model": "gpt-4o-mini-2024-07-18",
    "max_tokens": 4096,
    "system_prompt": SYSTEM_PROMPT,
}

class OpenAIChat:
    def __init__(self, config=None):
        # Merge user config with defaults
        self.config = {**default_config, **(config or {})}
        self._validate_config()
        self.client = AsyncOpenAI(api_key=self.config["api_key"])

    def _validate_config(self):
        """Validate required configuration values."""
        if not self.config["api_key"]:
            raise ValueError("Missing required configuration: OPENAI_API_KEY")


    async def chat(self, user_input: str) -> AsyncGenerator[str, None]:
        try:
            logger.debug("Chat method called with input: %s", user_input)
            response = await self.client.chat.completions.create(
                model=self.config["model"],
                messages=[
                    {"role": "system", "content": self.config["system_prompt"]},
                    {"role": "user", "content": user_input}
                ],
                stream=False
            )
            
            return response.choices[0].message.content 
            
        except Exception as e:
            logger.error(f"Chat error: {e}")


def is_valid_json(response_text: str) -> dict:
    """
    Check if the response is valid JSON format.
    
    Args:
        response_text (str): The response text to validate
        
    Returns:
        dict: A dictionary containing:
            - 'is_valid': bool indicating if the JSON is valid
            - 'data': parsed JSON data if valid, None if invalid
            - 'error': error message if invalid, None if valid
    """
    try:
        # Strip any markdown code block formatting if present
        cleaned_text = response_text.strip()
        if cleaned_text.startswith('```json'):
            cleaned_text = cleaned_text[7:]  # Remove ```json
        if cleaned_text.endswith('```'):
            cleaned_text = cleaned_text[:-3]  # Remove ```
        cleaned_text = cleaned_text.strip()
        
        # Try to parse the JSON
        parsed_data = json.loads(cleaned_text)
        
        return {
            'is_valid': True,
            'data': parsed_data,
            'error': None
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON validation error: {e}")
        return {
            'is_valid': False,
            'data': None,
            'error': f"Invalid JSON format: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error during JSON validation: {e}")
        return {
            'is_valid': False,
            'data': None,
            'error': f"Unexpected error: {str(e)}"
        }


# -------------------------------
# Tax-bill extraction with V3 prompt
# -------------------------------

V3_OUTPUT_KEYS = [
    "ParcelNumber",
    "TaxYear",
    "InstallmentNumber",
    "BaseAmount",
    "AlreadyAmount",
    "PenaltyAndInterest",
    "Fee",
    "TotalDue",
    "DueDate",
    "PaidDate",
    "Comments",
]


def _build_v3_prompt(document_text: str, parcel_number: str = "", tax_year: str = "", installment: str = "") -> str:
    """
    Safely build the EXTRACTION_PROMPT_V3 without triggering Python format on JSON braces.
    We only replace the specific placeholders present in the template.
    """
    prompt = EXTRACTION_PROMPT_V3
    # Perform targeted replacements to avoid interfering with JSON braces in the template
    replacements = {
        "{documentText}": document_text,
        "{parcelNumber}": parcel_number,
        "{taxYear}": tax_year,
        "{installment}": installment,
    }
    for token, value in replacements.items():
        prompt = prompt.replace(token, value)
    return prompt


async def extract_tax_filter_data(
    document_text: str,
    parcel_number: str = "",
    tax_year: str = "",
    installment: str = "",
    openai_config: Optional[Dict] = None,
) -> Dict:
    """
    Use EXTRACTION_PROMPT_V3 to extract tax-bill fields from the provided document text.

    Inputs:
    - document_text: Full page text (e.g., markdown) to analyze
    - parcel_number, tax_year, installment: Optional filters to guide selection
    - openai_config: Optional config override for OpenAIChat

    Output:
    - dict parsed from model JSON. On invalid JSON, returns a dict with V3 keys set to None.
    """
    try:
        user_prompt = _build_v3_prompt(
            document_text=document_text,
            parcel_number=parcel_number or "",
            tax_year=tax_year or "",
            installment=installment or "",
        )

        response = await OpenAIChat(config=openai_config).chat(user_prompt)
        logger.debug("V3 extraction raw response: %s", response)

        validation = is_valid_json(response)
        if validation["is_valid"]:
            return validation["data"]

        logger.error("V3 extraction returned invalid JSON: %s", validation["error"])
    except Exception as e:
        logger.error(f"Error in extract_tax_bill_v3: {e}")

    # Fallback on error/invalid JSON: return all expected keys as None
    return {key: None for key in V3_OUTPUT_KEYS}


# # Example usage and testing function
# async def main():
#     """
#     Example function to test filter_data functionality
#     """
#     # Sample data to test with
#     sample_data = "📄  Extracted from page\n: ```md\n# Detailed Tax Information for Parcel in Northampton County\n\n## Parcel Information\n- **Parcel ID**: M7 2 17A 0204\n- **Owner**: MEADOWS AT LEHIGH VALLEY LP\n- **Address**: EAST BLVD\n\n## Tax Billing Details\n- **Date of Billing**: 30-JAN-25\n- **Discount Tax Amount**: \n  - **$16,465.53** if paid on or before **31-MAR-25**\n- **Base Tax Amount**: \n  - **$16,801.56** if paid on or before **02-JUN-25**\n- **Penalty Tax Amount**: \n  - **$18,481.72** if paid after **02-JUN-25**\n\n## Important Notes\n- This information is current as of the date of billing and may not reflect any payments made.\n- Additional information can be obtained directly from the Revenue Office at **610-829-6186**.\n- In accordance with Act No 394 of 1945, failure to receive a real estate tax bill does not excuse or delay payment of taxes and does not avoid any penalty, interest, or charge for such delay. (Purdons Statute 72, Section 5511.7)\n- Please make checks payable to County of Northampton.\n```\n\n"
    
#     # Fields to filter
#     requested_fields = ["date", "baseamount", "address", "parcel_number"] 
    
#     print("Testing filter_data function...")
#     print(f"Original data: {sample_data}")
#     print(f"Requested fields: {requested_fields}")
#     print("-" * 50)
    
#     try:
#         result = await filter_data(requested_fields, sample_data)
#         print("Filtered result:")
#         print(json.dumps(result, indent=2))
        
#         if "error" in result:
#             print("Error occurred during filtering!")
#         else:
#             print("Filtering completed successfully!")
            
#     except Exception as e:
#         print(f"Error running filter_data: {e}")


# # Run the example if this file is executed directly
# if __name__ == "__main__":
#     asyncio.run(main())