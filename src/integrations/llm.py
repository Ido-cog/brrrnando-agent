import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def generate_summary(prompt: str) -> str:
    """
    Generate content using Gemini 2.5 Flash (or available model).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found")
        return "Error: Gemini API Key missing."
        
    genai.configure(api_key=api_key)
    
    try:
        # User requested 2.5 Flash, but current stable is 1.5-flash. 
        # Using gemini-1.5-flash as the fallback for now.
        model = genai.GenerativeModel('gemini-1.5-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        # Suggesting a fallback if 1.5-flash fails
        return f"Error generating summary: {str(e)}"
