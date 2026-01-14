import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path

# Load Master Dataset
DATA_PATH = Path(r"C:\Windows\Aegis-Project\Aegis-Lab\data\Aegis_Training_Master.csv")
MODEL_DIR = Path(r"C:\Windows\Aegis-Project\Aegis-Lab\models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def train_model():
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found!")
        return

    df = pd.read_csv(DATA_PATH)
    
    # 1. Encode 'conn_state' into numbers
    le = LabelEncoder()
    df['conn_state'] = le.fit_transform(df['conn_state'].astype(str))
    
    # 2. Define Features (X) and Label (y)
    X = df[['duration', 'orig_bytes', 'resp_bytes', 'conn_state']]
    y = df['label']
    
    # 3. Split: 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Initialize and Train with "Balanced Subsample"
    # This specifically forces the model to pay 10x more attention to malware samples
    print(f"Training Aegis-Overwatch on {len(X_train)} rows with Balanced Weights...")
    clf = RandomForestClassifier(
        n_estimators=100, 
        random_state=42,
        class_weight='balanced_subsample' # <--- THE CRITICAL FIX
    )
    clf.fit(X_train, y_train)
    
    # 5. Evaluate
    y_pred = clf.predict(X_test)
    print("\n--- PERFORMANCE REPORT ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")
    print("\nDetailed Breakdown (Look at 'Recall' for class 1):")
    print(classification_report(y_test, y_pred))
    
    # 6. Save
    joblib.dump(clf, MODEL_DIR / 'aegis_rf_model.pkl')
    joblib.dump(le, MODEL_DIR / 'conn_state_encoder.pkl')
    print(f"\n[🛡️] Model successfully weighted and saved to {MODEL_DIR}")

if __name__ == "__main__":
    train_model()