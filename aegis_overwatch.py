import joblib
import pandas as pd
import time
import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_PATH = Path("./Aegis-Lab/models/aegis_rf_model.pkl")
MONITOR_DIR = Path("./Aegis-Lab/data/incoming_telemetry")

def verbalize_threat(threat_row):
    print("[*] Contacting Gemini for analysis...")
    prompt = f"Analyze this network threat: {threat_row.to_json()}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text

def start_watchdog():
    print("[*] Initialization started...")
    
    # Check if model exists
    if not MODEL_PATH.exists():
        print(f"CRITICAL ERROR: Model not found at {MODEL_PATH}")
        return

    # Check if monitor folder exists
    if not MONITOR_DIR.exists():
        print(f"[*] Creating monitor directory at {MONITOR_DIR}")
        MONITOR_DIR.mkdir(parents=True, exist_ok=True)

    clf = joblib.load(MODEL_PATH)
    print("\n" + "="*40)
    print("      AEGIS-OVERWATCH: ONLINE")
    print("   Monitoring incoming telemetry...")
    print("="*40 + "\n")
    
    # State mapping for Zeek strings
    state_map = {'SF': 1, 'S0': 2, 'REJ': 3, 'RSTR': 4, 'RSTO': 5, 'S1': 6}

    while True:
        # HEARTBEAT: This shows you the script is still alive
        print(".", end="", flush=True) 
        
        for log in MONITOR_DIR.glob("*.csv"):
            print(f"\n[!] New file detected: {log.name}")
            try:
                df = pd.read_csv(log)
                df['conn_state'] = df['conn_state'].apply(lambda x: state_map.get(x, 0))
                
                # Match your 0.99 Model's Features
                features = df[['duration', 'orig_bytes', 'resp_bytes', 'conn_state']].fillna(0)
                predictions = clf.predict(features)
                
                if 1 in predictions:
                    print(f"[!] THREAT CONFIRMED by Local RF.")
                    mal_sample = df[predictions == 1].iloc[0]
                    report = verbalize_threat(mal_sample)
                    print(f"\n--- AEGIS INTELLIGENCE REPORT ---\n{report}\n")
                
                log.unlink()
                print("[*] Analysis complete. File removed.")
                
            except Exception as e:
                print(f"\n[X] Error processing {log.name}: {e}")
        
        time.sleep(5)

# CRITICAL: THIS IS THE ENGINE STARTER
if __name__ == "__main__":
    try:
        start_watchdog()
    except KeyboardInterrupt:
        print("\n[!] Aegis Overwatch shutting down gracefully...")