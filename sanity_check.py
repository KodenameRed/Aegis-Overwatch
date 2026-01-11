import pandas as pd
from pathlib import Path

# Updated paths based on your Get-ChildItem results
BENIGN_PATH = Path(r"C:\Windows\Aegis-Project\Aegis-Lab\data\processed\malicious\benign_baseline.csv")
MALICIOUS_PATH = Path(r"C:\Windows\Aegis-Project\Aegis-Lab\data\processed\malicious\combined_zeek_day1.csv")

def run_check():
    if not BENIGN_PATH.exists():
        print(f"Error: {BENIGN_PATH} not found!")
        return

    # Load the data
    benign_df = pd.read_csv(BENIGN_PATH)
    # We take the END of Day 1 for malicious data to ensure the attack is active
    malicious_df = pd.read_csv(MALICIOUS_PATH).tail(500) 

    print("--- Aegis Efficacy: Baseline vs. Attack ---")
    
    # Compare feature averages (The 'Signal')
    stats = pd.DataFrame({
        'Feature': ['avg_duration', 'avg_orig_bytes', 'avg_resp_bytes'],
        'Benign (Label 0)': [benign_df['duration'].mean(), benign_df['orig_bytes'].mean(), benign_df['resp_bytes'].mean()],
        'Malicious (Label 1)': [malicious_df['duration'].mean(), malicious_df['orig_bytes'].mean(), malicious_df['resp_bytes'].mean()]
    })
    
    print(stats.to_string(index=False))

    # Calculate Efficacy
    # If malicious bytes are > 2x benign bytes, the 'Signal' is strong enough
    if stats.iloc[1, 2] > (stats.iloc[1, 1] * 2):
        print("\n[!] VERDICT: HIGH EFFICACY. The attack footprint is distinct.")
    else:
        print("\n[?] VERDICT: LOW EFFICACY. Your baseline might be 'contaminated' with attack noise.")

if __name__ == "__main__":
    run_check()