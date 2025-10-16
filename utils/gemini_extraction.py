# from google import generativeai as genai
# import os
# import json
# import termcolor

# import dotenv 
# dotenv.load_dotenv() 

# def extract_data_with_gemini(
#     content: str,
# ) -> dict:
#     """
#     Extracts structured data from content using the Gemini API.

#     Args:
#         content: The text content to extract data from (e.g., Markdown).
#         extraction_goal: A description of what to extract.
#         fields: A dictionary of fields to extract, with descriptions.

#     Returns:
#         A dictionary containing the extracted data.
#     """
#     api_key = os.environ.get("GEMINI_API_KEY")
#     if not api_key:
#         raise ValueError("GEMINI_API_KEY environment variable not set.")

#     genai.configure(api_key=api_key)

#     model = genai.GenerativeModel('gemini-pro')

#     extraction_goal = " Extract the Parts Availability numbers. complete row of Companies and Total Inquiries from the table. "
#     prompt_parts = f"""
#         Instructions: You are an expert data extractor. Your task is to extract information from the provided text content based on the user's goal.
#         Extraction Goal: {extraction_goal}
#         \nContent to analyze:\n---\n {content}
#     """

#     # if fields:
#     #     prompt_parts.append("Extract the following fields:")
#     #     for field, description in fields.items():
#     #         prompt_parts.append(f"- {field}: {description}")
#     #     prompt_parts.append("Format the output as a JSON object with the specified field names.")
#     # else:
#     #     prompt_parts.append("Format the output as a JSON object.")

#     # prompt_parts.append("\nContent to analyze:\n---\n")
#     # prompt_parts.append(content)

#     # prompt = "\n".join(prompt_parts)

#     try:
#         response = model.generate_content(prompt_parts)
#         # The response might be in a markdown block
#         json_response = response.text.strip().replace("```json", "").replace("```", "").strip()
#         return json.loads(json_response)
#     except (json.JSONDecodeError, AttributeError) as e:
#         termcolor.cprint(f"❌ Error parsing Gemini response: {e}", color="red")
#         return {"error": "Failed to parse Gemini response as JSON", "details": str(e), "raw_response": response.text if 'response' in locals() else 'No response object'}
#     except Exception as e:
#         termcolor.cprint(f"❌ An unexpected error occurred during Gemini call: {e}", color="red")
#         return {"error": "An unexpected error occurred during Gemini response processing", "details": str(e)}

# if __name__ == "__main__":
#     # Example usage:
#     sample_content = """
# | Companies | Parts Availability | Total Inquiries |
# |---|---|---|
# | Company A | 95% | 250 |
# | Company B | 88% | 320 |
# | Company C | 92% | 180 |
# """
#     extracted_data = extract_data_with_gemini(sample_content)
#     print("Extracted data:")
#     print(json.dumps(extracted_data, indent=2))



from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text) 

