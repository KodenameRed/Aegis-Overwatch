import pandas as pd
from pathlib import Path
import json

BASE = Path(r"C:\Windows\Aegis-Project\Aegis-Lab")
RAW_DIR = BASE / "data" / "raw" / "network" / "zeek"
PROCESSED_DIR = BASE / "data" / "processed" / "malicious" # Saving all to processed folder

def ingest():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    log_files = list(RAW_DIR.glob("*.log"))
    
    for log in log_files:
        print(f"\n--- Processing: {log.name} ---")
        try:
            df = None
            
            # CHECK 1: Try reading as JSON Lines (Mordor Standard)
            try:
                # OTRF logs are usually JSON lines
                df = pd.read_json(log, lines=True)
                print(f"  -> Detected JSON format. Columns: {len(df.columns)}")
            except ValueError:
                # Fallback: Legacy Zeek TSV
                print("  -> JSON failed. Attempting Legacy Zeek TSV...")
                df = pd.read_csv(log, sep='\t', comment='#', header=None, engine='python')
                
                # If TSV, we must rename indices to names manually
                # 8=duration, 9=orig_bytes, 10=resp_bytes, 11=conn_state
                rename_map = {8: 'duration', 9: 'orig_bytes', 10: 'resp_bytes', 11: 'conn_state'}
                df.rename(columns=rename_map, inplace=True)

            # Step 2: Feature Selection & Normalization
            # Ensure the columns exist (Case insensitive check could be added if needed)
            required_cols = ['duration', 'orig_bytes', 'resp_bytes', 'conn_state']
            
            # Check if columns are present
            missing = [c for c in required_cols if c not in df.columns]
            if missing:
                print(f"  -> SKIP: Missing columns {missing} in {log.name}")
                continue

            features = df[required_cols].copy()
            
            # Clean '-' which Zeek uses for nulls in TSV, or nulls in JSON
            features.replace('-', 0, inplace=True)
            
            # Convert numeric columns safely
            for col in ['duration', 'orig_bytes', 'resp_bytes']:
                features[col] = pd.to_numeric(features[col], errors='coerce').fillna(0)
            
            # Step 3: Labeling
            # Label 0 for benign, 1 for malicious (based on filename)
            is_benign = "benign" in log.name.lower()
            features['label'] = 0 if is_benign else 1
            
            # Step 4: Save
            out_name = log.stem + ".csv"
            # If benign, maybe save to a benign folder? For now, putting all in PROCESSED_DIR
            out_path = PROCESSED_DIR / out_name
            features.to_csv(out_path, index=False, header=True)
            
            print(f"SUCCESS: Saved {len(features)} rows to {out_name} (Label: {features['label'].iloc[0]})")

        except Exception as e:
            print(f"CRITICAL ERROR on {log.name}: {e}")

if __name__ == "__main__":
    ingest()