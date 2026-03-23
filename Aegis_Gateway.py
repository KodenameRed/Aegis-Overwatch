import os, time, uuid, joblib, socket
import pandas as pd
from pathlib import Path
from scapy.all import sniff, IP
from colorama import Fore, init
from google import genai
from dotenv import load_dotenv

# --- [1] PATHS & ENVIRONMENT ---
BASE_DIR = Path(r"C:\Windows\Spritz-Project")
load_dotenv(dotenv_path=BASE_DIR / ".env")
init(autoreset=True)

LOCAL_IP = socket.gethostbyname(socket.gethostname())
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

RF_MODEL_PATH = BASE_DIR / "Aegis-Lab" / "models" / "aegis_rf_model.pkl"
TIMESTAMP = time.strftime("%Y%m%d_%H%M%S")
SESSION_ID = f"{TIMESTAMP}_{str(uuid.uuid4())[:4]}"

# --- [2] SILENT MODEL LOAD ---
try:
    rf_classifier = joblib.load(RF_MODEL_PATH)
    MODEL_FEATURES = rf_classifier.feature_names_in_.tolist() if hasattr(rf_classifier, 'feature_names_in_') else ["duration", "orig_bytes", "orig_pkts", "resp_bytes", "resp_pkts"]
except:
    rf_classifier = None 

class ZeekStats:
    def __init__(self):
        self.orig_bytes = self.orig_pkts = self.resp_bytes = self.resp_pkts = 0

def analyze_packet(pkt, stats):
    if pkt.haslayer(IP):
        size = len(pkt)
        if pkt[IP].src == LOCAL_IP:
            stats.orig_pkts += 1
            stats.orig_bytes += size
        else:
            stats.resp_pkts += 1
            stats.resp_bytes += size

def capture_session(duration):
    stats = ZeekStats()
    sniff(iface="\\Device\\NPF_Loopback", prn=lambda pkt: analyze_packet(pkt, stats), timeout=duration, store=False, filter="ip")
    return stats

def ask_gemini_forensics(telemetry, phase="VERDICT", context=None, is_threat=False):
    """Surgical Forensic Prompt: Binary logic for professional stability."""
    detail_request = "one-sentence technical summary" if not is_threat else "detailed threat-actor behavior analysis"
    
    prompt = f"""
    ROLE: Senior Cyber Forensic Analyst.
    INPUT: Zeek Telemetry {telemetry}
    PHASE: {phase}
    CONTEXT: {context}

    STRICT INSTRUCTIONS:
    1. Start your response with exactly 'VERDICT: BENIGN' or 'VERDICT: MALICIOUS'.
    2. Provide a {detail_request}.
    3. If 0 bytes transferred, it is likely BENIGN background noise unless frequency is extreme.
    4. No conversational filler or advice.
    """
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text.strip()
    except:
        return "VERDICT: ERROR. AI Analysis Unavailable."

def run_aegis_sentinel():
    print(f"{Fore.CYAN}[🛡️] AEGIS-SENTINEL ACTIVE | ID: {SESSION_ID}")
    
    # PHASE 1: BASELINE
    print(f"{Fore.WHITE}[...] Profiling Baseline (15s) - Stay Still")
    baseline = capture_session(15)

    print(f"\n{Fore.RED}{'='*40}")
    print(f"{Fore.YELLOW}  >>> FIRE ATTACK SCRIPTS NOW <<<")
    print(f"{Fore.RED}{'='*40}\n")
    drill = capture_session(15)

    # --- [3] OBSERVANT TELEMETRY (1.2x Noise Floor) ---
    TOLERANCE = 1.2 
    telemetry = {
        "duration": 15.0,
        "orig_bytes": max(0, drill.orig_bytes - baseline.orig_bytes) if drill.orig_bytes > (baseline.orig_bytes * TOLERANCE) else 0,
        "orig_pkts": max(0, drill.orig_pkts - baseline.orig_pkts) if drill.orig_pkts > (baseline.orig_pkts * TOLERANCE) else 0,
        "resp_bytes": max(0, drill.resp_bytes - baseline.resp_bytes) if drill.resp_bytes > (baseline.resp_bytes * TOLERANCE) else 0,
        "resp_pkts": max(0, drill.resp_pkts - baseline.resp_pkts) if drill.resp_pkts > (baseline.resp_pkts * TOLERANCE) else 0
    }

    # --- [4] UNIFIED INTELLIGENCE ENGINE ---
    raw_rf_score = rf_classifier.predict_proba(pd.DataFrame([telemetry])[MODEL_FEATURES])[0][1] if rf_classifier else 0.5
    
    # Senior Analyst Review
    refinement = ask_gemini_forensics(telemetry, "REFINE", f"Baseline Reference: {baseline.orig_bytes} bytes")
    
    # Logical Synchronization: Overriding ML noise with AI intuition
    is_benign_ai = "VERDICT: BENIGN" in refinement.upper()
    is_malicious_ai = "VERDICT: MALICIOUS" in refinement.upper()

    if is_benign_ai:
        aegis_confidence = min(raw_rf_score, 0.05) # Suppress noise
    elif is_malicious_ai:
        aegis_confidence = max(raw_rf_score, 0.95) # Boost identified threats
    else:
        aegis_confidence = raw_rf_score

    is_threat = aegis_confidence > 0.85
    final_audit = ask_gemini_forensics(telemetry, "VERDICT", refinement, is_threat=is_threat)

    # --- [5] PROFESSIONAL OUTPUT ---
    status_color = Fore.RED if is_threat else Fore.GREEN
    print(f"VERDICT: {status_color}{'🚨 THREAT DETECTED' if is_threat else '✅ BENIGN'}")
    
    # Unified score prevents conflicting data points
    print(f"AEGIS CONFIDENCE: {aegis_confidence:.2%}")
    print(f"FORENSIC REPORT: {final_audit}")

    # ARCHIVE
    save_path = BASE_DIR / "Aegis-Lab" / "data" / f"session_{SESSION_ID}.csv"
    pd.DataFrame([telemetry]).to_csv(save_path, index=False)
    print(f"\n{Fore.GREEN}[*] Session Archived: {save_path.name}")

if __name__ == "__main__":
    run_aegis_sentinel()