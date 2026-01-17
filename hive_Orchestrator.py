import os, json, time, joblib, csv, uvicorn
import pandas as pd
from pathlib import Path
from google import genai
from colorama import Fore, init
from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

# --- INITIALIZATION ---
init(autoreset=True)
app = FastAPI(title="Aegis Hive Orchestrator [Level 2]")
DETECTION_HISTORY = [] 

# Absolute Paths
PROJECT_ROOT = Path(r"C:\Windows\Aegis-Project")
MODEL_PATH = PROJECT_ROOT / "Aegis-Lab/models/aegis_rf_model.pkl"
LAB_LOG_PATH = PROJECT_ROOT / "Aegis-Lab/data/lab_captures.csv"
LAB_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# Security Config
API_KEY_NAME = "X-AEGIS-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
AEGIS_API_KEY = os.getenv("AEGIS_API_KEY", "Burn_Greek_Fire_Burn1088")

# AI Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Load Model
clf = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None
if clf: print(f"{Fore.GREEN}[✅] Behavioral Model Loaded.")

# --- MODELS ---

class Telemetry(BaseModel):
    duration: float
    orig_bytes: int
    resp_bytes: int
    orig_pkts: int
    resp_pkts: int
    conn_state: Optional[str] = "SF"
    service: Optional[str] = "-"

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != AEGIS_API_KEY: raise HTTPException(status_code=403, detail="Invalid Key")
    return api_key

# --- CORE LOGIC ---

def run_detection(data_dict):
    """ML Engine with High-Sensitivity Override."""
    if not clf: return False
    
    # Strictly aligned feature order
    column_order = ['duration', 'orig_bytes', 'resp_bytes', 'orig_pkts', 'resp_pkts']
    
    feat = pd.DataFrame([{
        "duration": data_dict['duration'],
        "orig_bytes": data_dict['orig_bytes'],
        "resp_bytes": data_dict['resp_bytes'],
        "orig_pkts": data_dict.get('orig_pkts', 0),
        "resp_pkts": data_dict.get('resp_pkts', 0)
    }])[column_order]
    
    # Probability Check (Threshold override)
    probs = clf.predict_proba(feat)
    malicious_prob = probs[0][1] 
    
    # SENSITIVITY FIX: If the model is even 25% sure it's an attack, flag it.
    # This catches the subtle bursts in your simulated attack scripts.
    return True if malicious_prob >= 0.25 else False

def request_ai_forensics(threat_data):
    """Tier-3 AI Analysis using Gemini 2.0 Flash."""
    print(f"\n{Fore.MAGENTA}[⚡] CONSULTING AI ANALYST...")
    
    # Strictly enforced forensic persona
    prompt = f"""
    [SYSTEM ROLE: ELITE SOC ANALYST]
    Analyze telemetry: {json.dumps(threat_data)}.
    
    OUTPUT REQUIREMENTS:
    - Start immediately with 🔍 ANALYSIS SUMMARY. 
    - Do NOT say "Okay", "I will", or "Here is".
    - Use technical, cold, forensic language.
    - Keep bullet points clean.
    
    STRUCTURE:
    1. 🔍 ANALYSIS SUMMARY
    2. 🚨 RISK LEVEL (1-10)
    3. 🛡️ TECHNICAL REMEDIATION
    """
    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI Analysis Failed: {str(e)}"

def log_to_lab_capture(data_dict, verdict):
    file_exists = LAB_LOG_PATH.exists()
    with open(LAB_LOG_PATH, 'a', newline='') as f:
        fieldnames = ['timestamp', 'duration', 'orig_bytes', 'resp_bytes', 'orig_pkts', 'resp_pkts', 'service', 'verdict']
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        if not file_exists: writer.writeheader()
        row = data_dict.copy()
        row['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
        row['verdict'] = verdict
        writer.writerow(row)

# --- API ENDPOINTS ---

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    cards = ""
    for e in DETECTION_HISTORY:
        v_color = "#ff4444" if e['v'] == "MALICIOUS" else "#00d4ff"
        
        # POLISH: Clean the AI text of Markdown debris and conversational filler
        clean_report = e['rep'].replace("**", "") # Remove bold markdown
        clean_report = clean_report.replace("Okay, ", "").replace("I will analyze ", "")
        
        # STYLING: Delineate categories with Span tags for CSS targeting
        formatted_report = clean_report.replace("🔍 ANALYSIS SUMMARY", "<span class='report-head'>🔍 ANALYSIS SUMMARY</span>")
        formatted_report = formatted_report.replace("🚨 RISK LEVEL", "<span class='report-head'>🚨 RISK LEVEL</span>")
        formatted_report = formatted_report.replace("🛡️ TECHNICAL REMEDIATION", "<span class='report-head'>🛡️ TECHNICAL REMEDIATION</span>")
        formatted_report = formatted_report.replace("\n", "<br>")

        cards += f"""
        <div class="incident-card" style="border-left: 4px solid {v_color};">
            <div class="card-header">
                <span class="timestamp">{e['time']}</span>
                <span class="source-tag">{e['src']}</span>
                <span class="verdict-tag" style="background: {v_color}22; color: {v_color};">● {e['v']}</span>
            </div>
            <div class="forensic-report">
                {formatted_report}
            </div>
        </div>
        """

    return f"""
    <html>
    <head>
        <meta http-equiv='refresh' content='10'>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg: #0b0f1a;
                --card: #161b2a;
                --accent: #38bdf8;
                --text: #f1f5f9;
            }}
            body {{ background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; padding: 50px; margin: 0; }}
            h1 {{ font-weight: 700; font-size: 1.8rem; letter-spacing: -1px; margin-bottom: 5px; color: var(--accent); }}
            .node-status {{ color: #64748b; font-size: 0.85rem; margin-bottom: 40px; text-transform: uppercase; letter-spacing: 1px; }}
            
            .incident-card {{ 
                background: var(--card); 
                border-radius: 12px; 
                padding: 30px; 
                margin-bottom: 30px; 
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
                transition: transform 0.2s ease;
            }}
            .card-header {{ 
                display: flex; 
                align-items: center; 
                gap: 15px; 
                margin-bottom: 20px; 
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.8rem;
            }}
            .timestamp {{ color: #94a3b8; }}
            .source-tag {{ background: #1e293b; padding: 4px 10px; border-radius: 4px; color: var(--accent); }}
            .verdict-tag {{ padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.75rem; letter-spacing: 0.5px; }}
            
            .forensic-report {{ font-size: 0.95rem; line-height: 1.8; color: #cbd5e1; }}
            .report-head {{ 
                display: block; 
                margin-top: 20px; 
                margin-bottom: 8px; 
                font-weight: 700; 
                color: var(--accent); 
                font-size: 0.9rem;
                text-transform: uppercase;
            }}
            .report-head:first-child {{ margin-top: 0; }}
        </style>
    </head>
    <body>
        <h1>[🐝] Aegis Hive | Elite Security Terminal</h1>
        <div class="node-status">Secure Connection: bachus | Mode: Level 2 Behavioral Analysis</div>
        <div class="feed">
            {cards if cards else "<p style='color:#475569'>Monitoring network interface... No active threats.</p>"}
        </div>
    </body>
    </html>
    """

@app.post("/analyze", dependencies=[Depends(verify_api_key)])
async def analyze(data: Telemetry):
    payload = data.model_dump()
    is_malicious = run_detection(payload)
    verdict = "MALICIOUS" if is_malicious else "BENIGN"
    log_to_lab_capture(payload, verdict)
    
    if is_malicious:
        report = request_ai_forensics(payload)
        event = {"time": time.strftime("%H:%M:%S"), "src": "Remote-Host", "v": "MALICIOUS", "rep": report}
        DETECTION_HISTORY.insert(0, event)
        if len(DETECTION_HISTORY) > 20: DETECTION_HISTORY.pop()
        print(f"{Fore.RED}[!!!] THREAT DETECTED")
        return {"verdict": "MALICIOUS", "report": report}
    
    print(f"{Fore.GREEN}[OK] Nominal")
    return {"verdict": "BENIGN"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
