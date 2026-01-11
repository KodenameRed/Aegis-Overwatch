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
    df = pd.read_csv(DATA_PATH)
    
    # 1. Encode 'conn_state' into numbers
    le = LabelEncoder()
    df['conn_state'] = le.fit_transform(df['conn_state'].astype(str))
    
    # 2. Define Features (X) and Label (y)
    X = df[['duration', 'orig_bytes', 'resp_bytes', 'conn_state']]
    y = df['label']
    
    # 3. Split: 80% for training, 20% for testing the AI's "unseen" performance
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Initialize and Train the Random Forest
    print(f"Training Aegis-Overwatch on {len(X_train)} rows...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # 5. Evaluate
    y_pred = clf.predict(X_test)
    print("\n--- PERFORMANCE REPORT ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")
    print("\nDetailed Breakdown:")
    print(classification_report(y_test, y_pred))
    
    # 6. Save the Model and the Encoder for future use
    joblib.dump(clf, MODEL_DIR / 'aegis_rf_model.pkl')
    joblib.dump(le, MODEL_DIR / 'conn_state_encoder.pkl')
    print(f"\nModel saved to {MODEL_DIR}")

if __name__ == "__main__":
    train_model()