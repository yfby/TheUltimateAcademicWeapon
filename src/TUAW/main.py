import os
import sys

import pyperclip
from dotenv import load_dotenv

from .ai_client import AIClient
from .capture import select_region
from .config import load_config
from .screenshot import capture_region


def main() -> None:
    env_status = load_dotenv()
    if not env_status:
        raise SystemExit("missing .env")

    config = load_config()
    client = AIClient(api_key=os.getenv("GEMINI_API_KEY"), config=config)
    print(f"AIClient initialized with model: {client.model}")
    print(f"Listening for {config.hotkey.keys}... (press Ctrl+C to quit)")
    pyperclip.copy(config.clipboard_indicators.initialized)

    try:
        while True:
            print(f"\n[{config.hotkey.keys}] Hold hotkey + move mouse to select region...")
            region = select_region(hotkey_str=config.hotkey.keys)
            if region is None:
                print("Selection cancelled.")
                continue

            print(f"Region: {region}")
            image = capture_region(region)

            pyperclip.copy(config.clipboard_indicators.analysis)
            print("Sending to AI...")
            result = client.solve(image)
            print(f"\n{result}")

            pyperclip.copy(result)
            print("\n[Copied to clipboard]")
    except KeyboardInterrupt:
        print("\nBye!")
        pyperclip.copy(config.clipboard_indicators.exit)
        sys.exit(0)


if __name__ == "__main__":
    main()
