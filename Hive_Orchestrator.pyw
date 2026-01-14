import os, json, time, joblib, threading, uvicorn, csv
import pandas as pd
from pathlib import Path
from google import genai
from colorama import Fore, Style, init
from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# --- INITIALIZATION ---
init(autoreset=True)
app = FastAPI(title="Aegis Hive Orchestrator [Level 2]")
DETECTION_HISTORY = [] 

# Paths
MODEL_PATH = Path("./Aegis-Lab/models/aegis_rf_model.pkl")
LAB_LOG_PATH = Path("./Aegis-Lab/data/lab_captures.csv")
LAB_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# Encoding Maps
STATE_MAP = {'SF': 1, 'S0': 2, 'REJ': 3, 'RSTR': 4, 'RSTO': 5, 'S1': 6}
SERVICE_MAP = {'-': 0, 'http': 1, 'dns': 2, 'ssl': 3, 'ssh': 4, 'ftp': 5}

# Security Config
API_KEY_NAME = "X-AEGIS-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
AEGIS_API_KEY = os.getenv("AEGIS_API_KEY", "Burn_Greek_Fire_Burn1088")

# AI Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
clf = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None

# --- MODELS ---

class Telemetry(BaseModel):
    duration: float
    orig_bytes: int
    resp_bytes: int
    conn_state: str
    orig_pkts: int = 0    # NEW Level 2 Field
    resp_pkts: int = 0    # NEW Level 2 Field
    service: str = "-"    # NEW Level 2 Field

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != AEGIS_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid Key")
    return api_key

# --- CORE LOGIC ---

def log_to_lab_capture(data_dict, verdict):
    """Saves every session to CSV for the AI Auditor to analyze later."""
    file_exists = LAB_LOG_PATH.exists()
    with open(LAB_LOG_PATH, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state', 'orig_pkts', 'resp_pkts', 'service', 'verdict'])
        if not file_exists:
            writer.writeheader()
        
        row = data_dict.copy()
        row['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
        row['verdict'] = verdict
        writer.writerow(row)

def request_ai_forensics(threat_data):
    """Consults Gemini for high-level analysis."""
    print(f"\n{Fore.MAGENTA}[⚡] HIVE ORCHESTRATOR: CONSULTING AI ANALYST...")
    prompt = f"Analyze threat: {json.dumps(threat_data)}. Focus on Packet-to-Byte ratios. Provide: Attack Type, Risk (1-10), and 1 Remediation."
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI Analysis Failed: {str(e)}"

def run_detection(data_dict):
    """ML Engine: Level 2 Detection."""
    if not clf: return False
    
    m_state = STATE_MAP.get(data_dict['conn_state'], 0)
    
    # Features must match the order in your training script
    # Note: If your model only has 4 features, it will ignore the new ones until you retrain.
    feat = pd.DataFrame([[
        data_dict['duration'], 
        data_dict['orig_bytes'], 
        data_dict['resp_bytes'], 
        m_state
    ]], columns=['duration', 'orig_bytes', 'resp_bytes', 'conn_state'])
    
    prediction = clf.predict(feat)
    return True if prediction[0] == 1 else False

# --- API ENDPOINTS ---

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    rows = "".join([f"<tr><td>{e['time']}</td><td>{e['src']}</td><td style='color:#ff4444;font-weight:bold;'>{e['v']}</td><td>{e['rep']}</td></tr>" for e in DETECTION_HISTORY])
    return f"""
    <html><head><meta http-equiv='refresh' content='10'><style>
    body{{background:#0d1117;color:#c9d1d9;font-family:sans-serif;padding:30px;}}
    h1{{color:#238636;border-bottom:1px solid #333;}}
    table{{width:100%;border-collapse:collapse;margin-top:20px;}}
    th,td{{padding:12px;border-bottom:1px solid #333;text-align:left;}}
    th{{background:#161b22;color:#8b949e;}}
    </style></head><body>
    <h1>[🐝] Aegis Hive | Level 2 Dashboard</h1>
    <p>Monitoring Node: <b>bachus</b> | Mode: <b>Lab Audit (Passive)</b></p>
    <table><tr><th>Time</th><th>Source</th><th>Verdict</th><th>AI Forensic Report</th></tr>
    {rows if rows else "<tr><td colspan='4'>Monitoring 30s Drills... No threats captured yet.</td></tr>"}
    </table></body></html>"""

@app.post("/analyze", dependencies=[Depends(verify_api_key)])
async def analyze(data: Telemetry):
    payload = data.model_dump()
    is_malicious = run_detection(payload)
    verdict = "MALICIOUS" if is_malicious else "BENIGN"
    
    # 1. Log to the Lab Capture CSV (For the AI Auditor)
    log_to_lab_capture(payload, verdict)
    
    if is_malicious:
        report = request_ai_forensics(payload)
        event = {"time": time.strftime("%H:%M:%S"), "src": "Remote-VM", "v": "MALICIOUS", "rep": report}
        DETECTION_HISTORY.insert(0, event)
        if len(DETECTION_HISTORY) > 20: DETECTION_HISTORY.pop()
        return {"verdict": "MALICIOUS", "report": report}
    
    return {"verdict": "BENIGN"}

if __name__ == "__main__":
    print(f"{Fore.GREEN}[🐝] HIVE LEVEL 2 ACTIVE | PORT: 8000")
    print(f"{Fore.CYAN}Lab Logging enabled: {LAB_LOG_PATH}")
    uvicorn.run(app, host="0.0.0.0", port=8000)