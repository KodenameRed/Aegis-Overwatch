from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os # Added for professional path handling
from Aegis_Train import extract_features
from colorama import Fore, Back, Style, init

init(autoreset=True)
app = FastAPI(title="Overwatch Security Gateway")

print(f"{Fore.CYAN}[*] Loading Aegis-Brain...")
model = joblib.load('aegis_model.pkl')

class SysmonLog(BaseModel):
    Image: str
    CommandLine: str
    ParentImage: str = ""

@app.post("/analyze")
def analyze_log(log: SysmonLog):
    try:
        data = pd.DataFrame([log.model_dump()])
        features = extract_features(data)
        
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][1])
        verdict = "MALICIOUS" if prediction == 1 else "BENIGN"

        if verdict == "MALICIOUS":
            print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} [!!!] SECURITY ALERT DETECTED [!!!] ")
            print(f"{Fore.RED}PROCESS: {log.Image}")
            print(f"{Fore.RED}RISK:    {probability*100:.2f}%")
        else:
            # FIX: Extract the filename using os.path.basename outside the f-string curly braces
            proc_name = os.path.basename(log.Image)
            print(f"{Fore.GREEN}[OK] Benign Activity: {proc_name}")

        return {"verdict": verdict, "risk_score": round(probability, 4)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Use 0.0.0.0 so the container can communicate with your Windows host
    uvicorn.run(app, host="0.0.0.0", port=8000)