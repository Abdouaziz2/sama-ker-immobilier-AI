import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("Clé API Gemini détectée.")
else:
    print("Clé API Gemini introuvable.")