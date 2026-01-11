import os
import json
import time
import joblib
import threading
import pandas as pd
from pathlib import Path
from google import genai
from colorama import Fore, Style, init
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

# --- INITIALIZATION ---
init(autoreset=True)
app = FastAPI(title="Aegis Hive Orchestrator")

# Constants
MODEL_PATH = Path("./Aegis-Lab/models/aegis_rf_model.pkl")
MONITOR_DIR = Path("./Aegis-Lab/data/incoming_telemetry")
STATE_MAP = {'SF': 1, 'S0': 2, 'REJ': 3, 'RSTR': 4, 'RSTO': 5, 'S1': 6}

# Load Brain & API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
clf = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None

# --- DATA SCHEMA FOR REMOTE AGENTS ---
class Telemetry(BaseModel):
    duration: float
    orig_bytes: int
    resp_bytes: int
    conn_state: str

# --- CORE LOGIC ---

def request_ai_forensics(threat_data):
    """Sends telemetry to Gemini for a CONCISE expert report."""
    print(f"\n{Fore.MAGENTA}[⚡] HIVE ORCHESTRATOR: CONSULTING AI ANALYST...")
    prompt = f"""
    You are a Tier-3 SOC Analyst. Analyze this network threat: {json.dumps(threat_data)}
    Provide a concise report in exactly this format:
    - ATTACK TYPE: (Likely name)
    - RISK LEVEL: (1-10)
    - WHY: (1 sentence on the specific pattern)
    - REMEDIATION: (1 step to fix)
    DO NOT explain what the fields mean.
    """
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        print(f"\n{Fore.YELLOW}--- [ AEGIS INTELLIGENCE BRIEF ] ---")
        print(Style.BRIGHT + response.text.strip())
        print(f"{Fore.YELLOW}------------------------------------\n")
        return response.text.strip()
    except Exception as e:
        print(f"{Fore.RED}[!] Hive Mind Error: {str(e)}")
        return "Forensic analysis failed."

def run_detection(data_dict):
    """The Shared Brain: Used by both local folder and remote API."""
    # Map connection state string to the numeric model format
    mapped_state = STATE_MAP.get(data_dict['conn_state'], 0)
    features = [[data_dict['duration'], data_dict['orig_bytes'], data_dict['resp_bytes'], mapped_state]]
    
    prediction = clf.predict(features)
    return True if prediction[0] == 1 else False

# --- AGENT ENDPOINT (FOR YOUR FRIEND) ---
@app.post("/analyze")
async def remote_detection(data: Telemetry):
    """This allows your friend's Agent to 'call' your brain."""
    is_malicious = run_detection(data.dict())
    
    if is_malicious:
        report = request_ai_forensics(data.dict())
        return {"verdict": "MALICIOUS", "report": report}
    return {"verdict": "BENIGN"}

# --- SENTINEL LOOP (LOCAL WATCHER) ---
def local_sentinel_loop():
    """Watches your local folder exactly like your original script."""
    print(f"{Fore.CYAN}[🛡️] LOCAL SENTINEL AGENT: ACTIVE")
    MONITOR_DIR.mkdir(parents=True, exist_ok=True)
    
    while True:
        logs = list(MONITOR_DIR.glob("*.csv"))
        for log in logs:
            try:
                df = pd.read_csv(log)
                for _, row in df.iterrows():
                    sample = row.to_dict()
                    if run_detection(sample):
                        print(f"{Fore.RED}[!] ALERT: Local Threat Confirmed in {log.name}")
                        request_ai_forensics(sample)
                log.unlink() # SOAR Containment
            except Exception as e:
                print(f"{Fore.RED}[!] Sentinel Error: {e}")
        
        print(f"{Fore.BLUE}.", end="", flush=True)
        time.sleep(5)

# --- STARTUP ---
if __name__ == "__main__":
    if not clf:
        print(f"{Fore.RED}CRITICAL: Model not found at {MODEL_PATH}")
    else:
        # Start the local watcher in a separate thread
        sentinel_thread = threading.Thread(target=local_sentinel_loop, daemon=True)
        sentinel_thread.start()

        # Start the Hive API (This blocks the main thread and stays alive)
        print(f"{Fore.GREEN}[🐝] HIVE API LISTENER: STARTING ON PORT 8000")
        uvicorn.run(app, host="127.0.0.1", port=8000)