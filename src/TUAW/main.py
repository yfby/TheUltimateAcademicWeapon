import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")


def main():
    client = genai.Client(api_key=gemini_api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain how to create a basic loop in Python in 3 sentences.",
    )
    print(response.text)


if __name__ == "__main__":
    main()
