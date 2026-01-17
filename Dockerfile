# 1. Start with a lightweight Python base
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy necessary files (Ensure paths match your folder structure)
# We copy the scripts from the root and the model from the subfolder
COPY Aegis_Train.py Aegis_Gateway.py benign.csv ./
COPY Aegis-Lab/models/aegis_rf_model.pkl ./aegis_model.pkl

# 4. Install the specific libraries needed
RUN pip install --no-cache-dir pandas scikit-learn fastapi uvicorn colorama joblib requests

# 5. Open Port 8000
EXPOSE 8000

# 6. Launch the Sentinel Gateway
CMD ["python", "Aegis_Gateway.py"]