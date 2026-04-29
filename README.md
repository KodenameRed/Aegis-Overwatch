
🛡️ **Aegis Overwatch**: Autonomous AI-Driven XDR  
**The Zero-Trust, Dual-Hybrid Intelligence Framework**

Aegis Overwatch is a bleeding-edge, autonomous Endpoint Detection and Response (EDR) framework. Unlike traditional signature-based tools, Aegis uses a hybrid mathematical + neural architecture to bridge raw kernel telemetry and high-level cognitive reasoning.

It decouples the **Nervous System** (local sensors + math engine) from the **Brain** (LLM-driven triage) and features a dynamic **Dual-Hybrid Routing System** — cloud-scale AI for speed and an air-gapped Sovereign core as absolute failsafe.

---

### 🏗️ The Aegis Architecture

```mermaid
flowchart LR
    %% Styling
    classDef base fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px,color:#000
    classDef triage fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px,color:#000
    classDef orchestrator fill:#eceff1,stroke:#607d8b,stroke-width:2px,color:#000
    classDef socket fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px,color:#000
    classDef forensic fill:#e0f2f1,stroke:#00897b,stroke-width:2px,color:#000

    %% Core Nodes
    BaseHive["<b>BASE HIVE</b><br/>(Continuous Ingestion)<br/><i>Lightweight, persistent ingestion.<br/>Minimal host impact.</i>"]:::base

    Triage["<b>v35k ONNX SPECIALIST</b><br/>(Triage Nurse)<br/><i>Every event processed.<br/>'S' = simple risk score.</i>"]:::triage

    Router["<b>ORCHESTRATOR & SPECIALIST ROUTER</b><br/><i>If S > 0.70 → routes to correct socket.</i>"]:::orchestrator

    Forensic["<b>LIVE FORENSIC CONTEXTUALIZATION</b><br/><i>Deep context-aware analysis.</i>"]:::forensic

    %% Specialist Sockets
    subgraph Sockets ["SPECIALIST SOCKETS (JIT Provisioning)"]
        direction TB
        C2["<b>C2 / NETWORK SCALPEL</b><br/><i>Beaconing & jitter analysis</i>"]:::socket
        Ransomware["<b>RANSOMWARE SPECIALIST</b><br/><i>Filesystem volatility</i>"]:::socket
        Lolbin["<b>LATERAL / LOLBIN SPECIALIST</b><br/><i>Script & CLI abuse</i>"]:::socket
        Extensible["<b>EXTENSIBLE SOCKET</b><br/><i>Future agents</i>"]:::socket
    end

    %% Flow
    BaseHive -->|Kernel Telemetry| Triage
    BaseHive -->|Registry Changes| Triage
    BaseHive -->|Network Activity| Triage

    Triage -->|Risk Score 'S'| Router
    Triage -->|Feature Vector| Router

    Router -->|Activated| C2
    Router -->|Activated| Ransomware
    Router -->|Activated| Lolbin
    Router -->|Activated| Extensible

    C2 --> Forensic
    Ransomware --> Forensic
    Lolbin --> Forensic
    Extensible --> Forensic
```

---

### ⚡ Core Features

- **Dual-Hybrid Neural Routing** — Cloud (Gemini) or Sovereign Local (Ollama) with automatic fallback
- **Nexus Dossier Compilation** — Auto-correlates host + network anomalies into executive summaries
- **Neural Specialist Pre-Scoring** — v35k ONNX model does sub-millisecond triage
- **Deterministic Intent Governance** — Hardcoded safety layer prevents dangerous AI actions
- **Network Jitter Analysis** — Detects robotic C2 beaconing via rhythm & volume baselines

---

### 🚀 Deployment & Onboarding

**Prerequisites**
- Windows 10/11 (Admin rights required)
- Python 3.10+
- Npcap (for Network Sentinel)
- Ollama (optional but recommended for Sovereign mode)

**One-Click Deploy**
```powershell
.\Deploy-Aegis.bat
```

This script:
- Creates a clean virtual environment
- Installs all dependencies (FastAPI, Jinja2, ONNX, etc.)
- Sets up Ollama automatically if missing
- Creates a desktop shortcut
- Launches the C2 console

After deployment, open `Aegis-Switch.bat` (or the desktop shortcut) → the web dashboard will open at `http://localhost:8000/dashboard`.

**First-Time Setup**
The UI will guide you through:
1. Creating your cryptographic master key (AEGIS_API_KEY)
2. Choosing Cloud (Gemini) or Sovereign (Ollama) mode
3. (Optional) Adding VirusTotal API key

---

### 🛠️ Tech Stack

- **Intelligence**: Gemini 1.5 Flash (Cloud) + Llama 3.2 1B (Sovereign via Ollama)
- **Backend**: FastAPI + Uvicorn + SQLite (WAL)
- **Forensics**: ONNX models, Npcap, Sysmon integration
- **Security**: HMAC-SHA256 signing, Deterministic Intent Governance

---

**License**  
MIT License — see [LICENSE](LICENSE) for details.

**Author**: Jacob Derwojed (KodenameRed)

---


