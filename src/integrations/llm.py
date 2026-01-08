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
        # Using gemini-2.5-flash as found in the user's compatible models list.
        model = genai.GenerativeModel('gemini-2.5-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        # Debug: List available models if initialization fails
        try:
            print("Listing available models for debugging...")
            models = [m.name for m in genai.list_models()]
            print(f"Compatible models: {models}")
        except Exception as list_err:
            print(f"Could not list models: {list_err}")
            
        return f"Error: {str(e)}"
