import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file.")

# Initialize Gemini 1.5 Flash model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def handle_misc_query(query: str) -> str:
    """
    Handle general queries that are not related to the database or contact.
    """
    prompt = f"""
You are a helpful assistant in a customer service chat system.

Answer the following user query as clearly and helpfully as possible:

User Query: "{query}"
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini Error in Misc Agent: {str(e)}"
