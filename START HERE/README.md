🛡️ Aegis Overwatch: Autonomous AI-Driven XDR
The Zero-Trust, Dual-Hybrid Intelligence Framework

Aegis Overwatch is a bleeding-edge, autonomous Endpoint Detection and Response (EDR) framework. Unlike traditional signature-based tools, Aegis utilizes a hybrid mathematical and neural architecture to bridge the gap between raw kernel telemetry and high-level cognitive reasoning.

Designed for high-security environments, Aegis operates by decoupling the "Nervous System" (Local Sensors & Math Engine) from the "Brain" (LLM-driven Triage). It features a dynamic Dual-Hybrid Routing System—utilizing cloud-scale AI for lightning-fast concurrent triage, while maintaining an air-gapped Sovereign AI core as an absolute failsafe.

🏗️ The Aegis Architecture
Aegis functions through tightly integrated layers that communicate via a secure, authenticated API.

The Orchestrator (The Spine): A FastAPI-driven hub that ingests telemetry, manages the real-time SQLite Forensic Ledger, and hosts the Live Triage War Terminal. It runs raw math and ONNX models to filter 95% of noise before AI intervention.

The Dual-Hybrid SOC Agent (The Specialist): An autonomous worker powered by Gemini 3.1 Flash (Cloud) and Llama 3.2:1B (Sovereign Local). It consumes high-risk alerts via the Model Context Protocol (MCP), performs forensic triage, and authorizes kinetic SOAR remediation.

The Network Sentinel (The Watchman): A compiled C2 Socket specialist that performs real-time rhythm and volumetric analysis on network traffic to identify stealthy, robotic beaconing or data exfiltration.

Code snippet
graph TD
    A[Kernel / Sysmon Sensors] --> B{Orchestrator Math Engine}
    N[Network Sentinel] --> B
    B -->|Deterministic Filter & ONNX Scoring| C[Zero-Trust Hub & Vault]
    C -->|High-Risk Anomalies| D[MCP SOC Agent]
    
    D -->|AI_ENGINE_MODE=CLOUD| E[Gemini 3.1 Flash <br/> High-Speed Concurrency]
    D -->|Failsafe / LOCAL Mode| F[Llama 3.2:1B <br/> Air-Gapped Sovereign Core]
    
    E --> G[Nexus Master Dossier & UI Update]
    F --> G
    G --> H{Intent Governance Layer}
    H -->|Authorized| I[Kinetic OS Remediation]
⚡ Core Features
Dual-Hybrid Neural Routing: Set the engine to CLOUD for massive 10-thread parallel processing via Gemini, or LOCAL for strict, air-gapped Sovereign inference via Ollama. If the Cloud API drops or is rate-limited, Aegis automatically falls back to the Sovereign core without missing a beat.

Nexus Dossier Compilation: Automatically correlates disparate host (lateral) and network (gateway) anomalies over a 60-second temporal window, generating a highly technical, multi-vector Kill-Chain Executive Summary.

Neural Specialist Pre-Scoring: Utilizes a local v35k ONNX model for sub-millisecond behavioral scoring before any telemetry touches the LLM.

Deterministic Intent Governance: A hardcoded safety layer that intercepts AI-proposed actions. It prevents the AI from targeting critical system primitives (e.g., explorer.exe, lsass.exe) regardless of the threat score.

Network Jitter Analysis: Detects robotic C2 beaconing by analyzing packet rhythm, volume, and exact jitter variance against historical baselines, effectively filtering out benign Cloud/CDN traffic.

🚀 Deployment & Onboarding Guide
Aegis is designed for rapid, frictionless deployment with an automated setup and a guided, web-based initialization process.

1. Prerequisites
Windows 10/11 (Admin privileges required).

Python 3.10+.

Npcap (Required for the Network Sentinel).

Ollama (Optional, but required for Sovereign/Local fallback mode).

2. The One-Click Deploy
Run the automated deployment script to bootstrap the environment:

PowerShell
.\Deploy-Aegis.bat
What it does: Creates the Virtual Environment (venv), installs all dependencies (FastAPI, ONNX, MCP, Google GenAI, OpenAI), initializes the SQLite database and Neural Vault directories, drops an easy-access Shortcut on your Desktop, and automatically launches the Aegis Engine upon completion.

3. Vault Initialization & Key Setup
Once the deployment script finishes, it will automatically launch Aegis-Switch.bat and open the local War Terminal (http://127.0.0.1:8000/dashboard). (For future use, you can simply double-click your new Aegis Overwatch Desktop shortcut or run Aegis-Switch.bat manually).

Upon first boot, the UI will lock down and present the System Initialization Modal. You will be guided through three onboarding steps:

Cryptographic Master Key (Required): You must create a custom Aegis Master Key. This acts as a cryptographic salt (HMAC-SHA256) to sign your behavior whitelists and authenticate local telemetry. Your key never leaves the machine.

Intelligence Core Selection: Choose your primary engine.

CLOUD (Shielded): Select this for maximum speed and logic. You will be prompted to insert a Google Gemini API Key (Obtain a free key from Google AI Studio).

SOVEREIGN (Air-Gapped): Select this to keep all inference strictly local using Llama 3.2:1B via Ollama.

Threat Intelligence Feed (Optional): To enable the UI's real-time malicious signature badges, paste your VirusTotal API key (Obtain a free key here).

Click "Seal Vault & Ignite Core". Aegis will automatically generate your secure .env file, spin up the SOC Agents in the background, and begin protecting the host.

🕹️ Operational Control
Aegis uses a simplified "Switch" system to manage the stack.

Aegis-Switch.bat (or Desktop Shortcut)
This is your primary command interface.

Start Engine: Launches the Orchestrator, the SOC Agent, and the Network Sentinel in synchronized background windows.

Stop Engine: Gracefully terminates all background workers using OS-level SIGKILLs and flushes the buffer.

Aegis-Control.bat
Used for advanced maintenance:

Clear Dashboard: Archives the current Active Incident Buffer to immutable storage.

Compact Forensic Ledger: Purges raw SQLite packet data older than 24 hours while preserving AI-generated behavior baselines.

Sterilize Environment: A "Wipe" command that permanently destroys all SQL and JSON ledgers for post-simulation cleanup.

🛠️ Tech Stack
Intelligence: Google Gemini 3.1 Flash (Cloud), Meta Llama 3.2:1B (Sovereign Local).

Backend: FastAPI (Python), Uvicorn, SQLite (WAL Mode).

Forensics: Windows Sysmon, Npcap, VirusTotal API.

Security: Deterministic Intent Governance, Zero-Trust API Authentication (HMAC-SHA256).

⚖️ License
Distributed under the MIT License. See LICENSE for more information.

Author: Jacob Derwojed (KodenameRed)