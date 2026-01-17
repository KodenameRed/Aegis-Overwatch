import joblib
import pandas as pd

# Load the brain
clf = joblib.load("./Aegis-Lab/models/aegis_rf_model.pkl")

# Define the features we used
features = ['duration', 'orig_bytes', 'resp_bytes', 'conn_state']

# Get the importance scores
importance = clf.feature_importances_

print("--- AEGIS FEATURE IMPORTANCE ---")
for i, v in enumerate(importance):
    print(f"{features[i]}: {v:.4f}")
