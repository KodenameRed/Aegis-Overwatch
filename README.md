
🛡️ **Aegis Overwatch**: Autonomous AI-Driven XDR  
**The Zero-Trust, Dual-Hybrid Intelligence Framework**

Aegis Overwatch is a bleeding-edge, autonomous Endpoint Detection and Response (EDR) framework. Unlike traditional signature-based tools, Aegis uses a hybrid mathematical + neural architecture to bridge raw kernel telemetry and high-level cognitive reasoning.

It decouples the **Nervous System** (local sensors + math engine) from the **Brain** (LLM-driven triage) and features a dynamic **Dual-Hybrid Routing System** — cloud-scale AI for speed and an air-gapped Sovereign core as absolute failsafe.

---

### 🏗️ The Aegis Architecture

```mermaid
flowchart LR
    %% Styling
    classDef edge fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px,color:#000
    classDef hunter fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#000
    classDef neural fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px,color:#000
    classDef airlock fill:#fbe9e7,stroke:#ff5722,stroke-width:2px,color:#000
    classDef cognitive fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px,color:#000
    classDef execution fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#000

    %% Edge Layer
    subgraph Edge ["1. SOVEREIGN EDGE (Local Filtering)"]
        direction TB
        Telemetry["<b>NATIVE TELEMETRY</b><br/><i>ETW & WFP Kernel Streams</i>"]:::edge
        Sifter["<b>DETERMINISTIC SIFTER</b><br/><i>Morphological Math & Entropy</i><br/>Drops 95% of benign noise"]:::edge
        Hunter["<b>STRATEGIC DB HUNTER</b><br/><i>Jitter-Traps & Nexus Sweeps</i><br/>Catches Low & Slow APTs"]:::hunter
        Triage["<b>v35k ONNX SPECIALIST</b><br/><i>Neural Scoring & Lineage Checks</i><br/>S > 0.70 triggers orchestration"]:::neural
    end

    %% The Privacy Airlock
    Gateway["<b>CRYPTOGRAPHIC PRIVACY GATEWAY</b><br/><i>HMAC-SHA256 Masking & Semantic Airlock</i><br/>Prevents Prompt Injection & PII Leaks"]:::airlock

    %% Cognitive Layer
    subgraph Brain ["2. DUAL-HYBRID SYNTHESIS"]
        direction TB
        Cloud["<b>STRATEGIC CLOUD ACTUARY</b><br/><i>Hot-Swappable Frontier LLM</i><br/>Temporal Correlation & Playbooks"]:::cognitive
        Failover["<b>LOCAL SOVEREIGN CORE</b><br/><i>Air-Gapped LLM</i><br/>Cognitive Failover (Degraded but Defended)"]:::cognitive
    end

    %% Execution & Governance
    subgraph Terminal ["3. CLINICAL REMEDIATION"]
        direction TB
        Gov["<b>INTENT GOVERNANCE JUDGE</b><br/><i>Deterministic Veto Gatekeeper</i><br/>Mathematically prevents AI Self-Destruction"]:::execution
        War["<b>WAR TERMINAL UI</b><br/><i>Pre-Staged Kinetic Actions</i><br/>(Isolate Host, Memory Dump, Revoke TGT)"]:::execution
    end

    %% Flow Routes
    Telemetry -->|Execution & OS Logs| Sifter
    Telemetry -->|Network DB| Hunter
    Sifter -->|High Risk Feature Vector| Triage
    Hunter -->|7-Day Aggregated Chain| Triage
    
    Triage -->|Validated Threat DNA| Gateway
    
    Gateway -->|Sanitized Context| Cloud
    Gateway -.->|Network Outage / Isolation| Failover

    Cloud -->|Proposes Action Playbook| Gov
    Failover -->|Proposes Action Playbook| Gov

    Gov -->|Intent Verified| War
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


