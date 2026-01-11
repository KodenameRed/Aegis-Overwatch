import pandas as pd
from pathlib import Path

# Set the path to the LAB data folder
PROCESSED_DIR = Path(r"C:\Windows\Aegis-Project\Aegis-Lab\data\processed")
OUTPUT_FILE = Path(r"C:\Windows\Aegis-Project\Aegis-Lab\data\Aegis_Training_Master.csv")

def merge_and_balance():
    # 1. Recursive search for all CSVs in processed/ or any subfolders
    csv_files = list(PROCESSED_DIR.rglob("*.csv"))
    
    if not csv_files:
        print(f"CRITICAL ERROR: No CSV files found in {PROCESSED_DIR}")
        print("Did you run 'python ingest_all_zeek.py' successfully first?")
        return

    print(f"Found {len(csv_files)} files. Merging...")
    
    all_dfs = []
    for f in csv_files:
        all_dfs.append(pd.read_csv(f))
    
    df = pd.concat(all_dfs, ignore_index=True)
    
    # 2. Split for Balancing
    malicious = df[df['label'] == 1]
    benign = df[df['label'] == 0]
    
    print(f"Original Pool -> Malicious: {len(malicious)}, Benign: {len(benign)}")
    
    # 3. Downsample Benign to 10,000 rows (The "Bullshit Filter" Tuning)
    # This prevents the 1 million rows from drowning out the 7k attacks
    if len(benign) > 10000:
        benign_balanced = benign.sample(n=10000, random_state=42)
    else:
        benign_balanced = benign
    
    # 4. Final Merge & Save
    final_df = pd.concat([malicious, benign_balanced])
    final_df.to_csv(OUTPUT_FILE, index=False)
    
    print("\n--- BALANCED DATASET SUMMARY ---")
    print(f"Total Training Rows: {len(final_df)}")
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_and_balance()