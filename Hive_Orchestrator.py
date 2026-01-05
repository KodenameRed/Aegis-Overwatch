import os
import json
import requests
from google import genai
from colorama import Fore, Style, init

init(autoreset=True)

# 1. Configuration
GATEWAY_URL = "http://127.0.0.1:8000/analyze"
# Pulls the key from the environment variable you set in the registry
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

# 2. Initialize the Hive Mind
client = genai.Client(api_key=GEMINI_API_KEY)

def request_ai_forensics(telemetry):
    """Sends raw log to Gemini for real Tier-3 analysis."""
    print(f"\n{Fore.MAGENTA}[⚡] HIVE ORCHESTRATOR: CONSULTING AI ANALYST...")
    
    prompt = f"""
    Analyze this malicious telemetry caught by the Overwatch Gateway. 
    Identify the MITRE ATT&CK TTPs for the CommandLine and provide remediation.
    
    TELEMETRY:
    {json.dumps(telemetry, indent=2)}
    """
    
    try:
        # Calls the live cloud AI model you enabled
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        print(f"{Fore.YELLOW}--- [ LIVE AI FORENSIC REPORT ] ---")
        print(Style.BRIGHT + response.text)
        print(f"{Fore.YELLOW}----------------------------------")
    except Exception as e:
        print(f"{Fore.RED}[!] Hive Mind Error: {str(e)}")

def monitor_gateway(log_entry):
    """Bridges Local Docker Shield to Cloud AI Hive."""
    print(f"{Fore.CYAN}[*] Sending event to Overwatch Shield...")
    try:
        response = requests.post(GATEWAY_URL, json=log_entry)
        result = response.json()
        
        # Check if the Aegis Brain flagged it as 60% risk or higher
        if result['verdict'] == "MALICIOUS":
            print(f"{Fore.RED}[!] SHIELD ALERT: Risk {result['risk_score']*100:.2f}%")
            request_ai_forensics(log_entry)
        else:
            print(f"{Fore.GREEN}[OK] Hive Monitoring: Event Benign (Risk: {result['risk_score']*100:.2f}%)")
    except Exception as e:
        print(f"{Fore.RED}[!] Connection Error: Is the Docker container running? {e}")

if __name__ == "__main__":
    # FULL Attack Payload (No dots!)
    attack_test = {
        "Image": "C:\\Windows\\System32\\powershell.exe",
        "CommandLine": "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -EncodedCommand JABzAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAEkATwAuAE0AZQBtAG8AcgB5AFMAdAByAGUAYQBtACgAWwBDAG8AbgB2AGUAcgB0AF0AOgA6AEYAcgBvAG0AQgBhAHBASE64U3RyaW5nKAAiAEgA...",
        "ParentImage": "C:\\Windows\\system32\\services.exe"
    }
    monitor_gateway(attack_test)