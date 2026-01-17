import os, time, json, joblib, requests
import pandas as pd
from colorama import Fore, init

init(autoreset=True)

# --- CONFIG ---
HIVE_URL = os.getenv("HIVE_URL", "http://host.docker.internal:8000/analyze")
API_KEY = "Burn_Greek_Fire_Burn1088"
MODEL_PATH = "aegis_model.pkl" 

# Load the local brain
clf = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

def run_sentinel_drill():
    print(f"{Fore.CYAN}--- AEGIS SENTINEL: 30-SECOND DRILL ---")
    print("[1/3] BASELINE: 15 seconds of idle...")
    time.sleep(15)
    
    print(f"{Fore.YELLOW}[2/3] ATTACK WINDOW: 10 seconds. (GO!)")
    drill_data = {
        "duration": 10.0,
        "orig_bytes": 45000, 
        "resp_bytes": 500,
        "orig_pkts": 300,
        "resp_pkts": 50,
        "conn_state": "SF"
    }
    time.sleep(10)
    
    print("[3/3] COOLDOWN: 5 seconds.")
    time.sleep(5)
    
    # --- UPDATED DETECTION LOGIC ---
    if clf:
        # Align features exactly as the Hive does
        feat = pd.DataFrame([drill_data])[["duration", "orig_bytes", "resp_bytes", "orig_pkts", "resp_pkts"]]
        
        # Use Probability to match Hive sensitivity
        probs = clf.predict_proba(feat)
        malicious_prob = probs[0][1]
        
        # Apply the 0.25 threshold
        verdict = "MALICIOUS" if malicious_prob >= 0.25 else "BENIGN"
        
        v_color = Fore.RED if verdict == "MALICIOUS" else Fore.GREEN
        print(f"{v_color}[⚡] LOCAL VERDICT: {verdict} (Confidence: {malicious_prob:.2f})")

    # Ship to Hive
    print(f"[📫] SHIPPING TO HIVE: {HIVE_URL}...")
    headers = {"X-AEGIS-KEY": API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.post(HIVE_URL, json=drill_data, headers=headers, timeout=5)
        print(f"{Fore.GREEN}[✅] HIVE RESPONSE: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"{Fore.RED}[X] CONNECTION ERROR: {str(e)}")

if __name__ == "__main__":
    run_sentinel_drill()