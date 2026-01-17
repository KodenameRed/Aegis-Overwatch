import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def extract_features(df):
    """The 'Standardized Feature Extractor' used by both Training and Gateway."""
    df['CommandLine'] = df['CommandLine'].fillna('')
    df['Image'] = df['Image'].fillna('')
    
    features = pd.DataFrame()
    features['cmd_length'] = df['CommandLine'].apply(len)
    features['is_shell'] = df['Image'].str.contains('powershell|cmd.exe', case=False).astype(int)
    features['is_system_dir'] = df['Image'].str.contains('System32', case=False).astype(int)
    return features

def train():
    print("[*] Training Phase starting...")
    if not os.path.exists('benign.csv'):
        print("[!] Error: benign.csv missing.")
        return

    # Load and Label Benign
    df_b = pd.read_csv('benign.csv')
    X_b = extract_features(df_b)
    y_b = [0] * len(X_b)

    # Load and Label Malicious
    m_events = []
    if os.path.exists('malicious_sample.json'):
        with open('malicious_sample.json', 'r') as f:
            for line in f:
                try:
                    ev = json.loads(line)
                    data = ev.get('event_data', {})
                    m_events.append({'CommandLine': data.get('CommandLine', ''), 'Image': data.get('Image', '')})
                except: continue
    
    df_m = pd.DataFrame(m_events)
    X_m = extract_features(df_m)
    y_m = [1] * len(X_m)

    # Combine and Train
    X = pd.concat([X_b, X_m])
    y = y_b + y_m
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, 'aegis_model.pkl')
    print("[OK] Brain trained and saved as aegis_model.pkl")

if __name__ == "__main__":
    train()
