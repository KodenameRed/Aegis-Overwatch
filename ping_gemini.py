import os
from google import genai
from dotenv import load_dotenv

# 1. Load the .env file into Python's memory
load_dotenv()

# 2. Get the value BY ITS NAME ("GOOGLE_API_KEY")
# DO NOT put your actual key (AIzaSyA...) here.
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("CRITICAL ERROR: GOOGLE_API_KEY not found in .env file.")
    exit()

def ping_google():
    print(f"--- Aegis Intelligence: Testing Uplink ---")
    try:
        # 3. Use the variable we just pulled from the .env
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Aegis-Overwatch system check: Are you online?"
        )
        
        print(f"\nSTATUS: ONLINE")
        print(f"Cloud Response: {response.text}")
        return True

    except Exception as e:
        print(f"\nCONNECTION FAILED: {e}")
        return False

if __name__ == "__main__":
    ping_google()