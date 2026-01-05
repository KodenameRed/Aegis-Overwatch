# 1. Start with a lightweight Python base
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your project files into the container
# We copy the model, the training logic, and the gateway
COPY Aegis_Train.py Aegis_Gateway.py aegis_model.pkl benign.csv ./

# 4. Install the specific libraries needed for the Brain and Gateway
RUN pip install --no-cache-dir pandas scikit-learn fastapi uvicorn colorama joblib

# 5. Open Port 8000 (The Gateway's port)
EXPOSE 8000

# 6. The "Launch Code"
CMD ["python", "Aegis_Gateway.py"]