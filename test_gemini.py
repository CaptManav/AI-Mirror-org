import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents="We will sign the contract and transfer payment today."
)

print(response.text)
