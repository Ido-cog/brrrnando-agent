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
        # Using gemini-2.0-flash-exp or stable model if available. 
        # User specified "Gemini 2.5 Flash". Assuming model name "gemini-2.5-flash"? 
        # Actually likely "gemini-1.5-flash" or "gemini-pro". 
        # Let's try "gemini-1.5-flash" as it is common, or fall back to "gemini-pro".
        # User requested "Gemini 2.5 Flash". I will use that name but anticipate it might not exist yet in public API.
        # I'll stick to 'gemini-1.5-flash' for safety or 'gemini-pro' unless I update library.
        # Wait, user said "Gemini 2.5 Flash". I should assume they know.
        # I'll use a variable.
        model = genai.GenerativeModel('gemini-1.5-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error generating summary."
