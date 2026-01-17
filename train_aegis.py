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
    print(f"Available columns: {df.columns.tolist()}")

    # 1. Dynamic Feature Selection
    # List all possible features we WANT to use if they exist
    target_features = ['duration', 'orig_bytes', 'resp_bytes', 'orig_pkts', 'resp_pkts', 'conn_state']
    
    # Filter list to only include what is actually in the CSV
    features_to_use = [f for f in target_features if f in df.columns]
    print(f"Training using features: {features_to_use}")

    # 2. Handle Categorical Encoding only if column exists
    if 'conn_state' in df.columns:
        le = LabelEncoder()
        df['conn_state'] = le.fit_transform(df['conn_state'].astype(str))
        joblib.dump(le, MODEL_DIR / 'conn_state_encoder.pkl')
        print("Encoded 'conn_state' and saved encoder.")
    else:
        print("Skipping 'conn_state' encoding (not found in dataset).")

    # 3. Define Features (X) and Label (y)
    X = df[features_to_use]
    y = df['label']
    
    # 4. Split: 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 5. Initialize and Train with "Balanced Subsample"
    print(f"Training Aegis-Overwatch on {len(X_train)} rows with Balanced Weights...")
    clf = RandomForestClassifier(
        n_estimators=100, 
        random_state=42,
        class_weight='balanced_subsample' 
    )
    clf.fit(X_train, y_train)
    
    # 6. Evaluate
    y_pred = clf.predict(X_test)
    print("\n--- PERFORMANCE REPORT ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")
    print("\nDetailed Breakdown (Look at 'Recall' for class 1):")
    print(classification_report(y_test, y_pred))
    
    # 7. Save Model
    joblib.dump(clf, MODEL_DIR / 'aegis_rf_model.pkl')
    print(f"\n[🛡️] Model successfully weighted and saved to {MODEL_DIR}")

if __name__ == "__main__":
    train_model()
