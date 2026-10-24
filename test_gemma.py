
import tomllib
from pathlib import Path
from google import genai

# Load the API key from your secure file
secrets_path = Path(".streamlit/secrets.toml")

with secrets_path.open("rb") as file:
    secrets = tomllib.load(file)

api_key = secrets.get("GEMINI_API_KEY")

if not api_key or api_key == "paste_your_actual_api_key_here":
    raise ValueError("Check your API key in .streamlit/secrets.toml")

# Connect to Gemma
client = genai.Client(api_key=api_key)

print("Connecting to Gemma...")

response = client.models.generate_content(
    model="gemma-4-26b-a4b-it",
    contents="Introduce yourself as the AI assistant for MediPilot AI in one short sentence."
)

print("\nGemma's response:")
print(response.text)
