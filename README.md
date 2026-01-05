# Aegis-Overwatch: AI-Driven SOAR Pipeline

### 🛡️ Project Overview
Aegis-Overwatch is a multi-stage **Security Orchestration, Automation, and Response (SOAR)** pipeline. It integrates local Machine Learning (Random Forest) with Cloud-based Agentic AI (Gemini 2.0) to detect, isolate, and analyze advanced persistent threats (APTs) in real-time.



### 🏗️ Architecture
1. **Sensor Layer:** Monitors host telemetry (Sysmon-style data).
2. **Detection Layer (Aegis Brain):** A containerized Random Forest model serving via FastAPI. 
3. **Isolation Layer (The Shield):** Dockerized microservices running on WSL2 to prevent host-breakout.
4. **Analysis Layer (The Hive):** An Agentic Orchestrator that triggers automated forensic triage using the Gemini 2.0 Flash API.

### 🚀 Key Features
* **Real-time Triage:** Converts raw command-line telemetry into human-readable forensic reports in <2 seconds.
* **MITRE ATT&CK Mapping:** Automatically identifies TTPs such as T1059.001 (PowerShell) and T1027 (Obfuscation).
* **Infrastructure as Code:** Fully containerized deployment for consistent security posture across environments.

### 🛠️ Tech Stack
* **Language:** Python 3.11+
* **ML:** Scikit-Learn (Random Forest Classifier)
* **DevOps:** Docker, WSL2, PowerShell 7
* **AI:** Google Gemini 2.0 Flash SDK

### ⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.
