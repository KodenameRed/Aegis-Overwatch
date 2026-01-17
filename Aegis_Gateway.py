import os, time, json, joblib, requests
import pandas as pd
from colorama import Fore, init

init(autoreset=True)

# --- CONFIG ---
HIVE_URL = os.getenv("HIVE_URL", "http://host.docker.internal:8000/analyze")
# HIDDEN: No longer hardcoded. Fetched from the environment.
API_KEY = os.getenv("AEGIS_API_KEY") 
MODEL_PATH = "aegis_model.pkl" 

# Load the local brain
clf = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

def run_sentinel_live():
    if not API_KEY:
        print(f"{Fore.RED}[!] CRITICAL: AEGIS_API_KEY not set in environment.")
        return

    print(f"{Fore.GREEN}[🛡️] AEGIS SENTINEL: LIVE MONITORING MODE")
    print("Ready for collaborator tests. Monitoring interface...")
    
    # This remains clean of hardcoded attack data. 
    # Your collaborator can now run their own tools.
    while True:
        # Placeholder: This will eventually be replaced by your Scapy sniffing logic
        time.sleep(10)

if __name__ == "__main__":
    run_sentinel_live()