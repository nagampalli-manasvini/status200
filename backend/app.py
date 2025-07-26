from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
apiKey=os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=apiKey)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)