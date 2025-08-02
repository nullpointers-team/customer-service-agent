import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Load dummy orders
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "dummy_db.json")

def load_orders():
    with open(DATA_PATH, "r") as f:
        return json.load(f)["orders"]

def handle_db_query(query: str) -> str:
    orders = load_orders()

    # Format user prompt + database
    prompt = f"""
You are a helpful customer support agent. Below is a database of user orders:

{json.dumps(orders, indent=2)}

Based on this data, answer the following user query in a helpful tone:

User Query: "{query}"

If the query cannot be answered from the orders, say so politely.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error from Gemini: {str(e)}"

