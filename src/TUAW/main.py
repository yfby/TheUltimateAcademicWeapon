import os

from dotenv import load_dotenv

from .ai_client import AIClient

env_status = load_dotenv()

if not env_status:
    raise SystemExit("missing .env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def main() -> None:
    client = AIClient(api_key=GEMINI_API_KEY, model="gemini-2.5-flash")
    print(f"AIClient initialized with model: {client.model}")
    print(client.answer("what is 1+1?"))


if __name__ == "__main__":
    main()
