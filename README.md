
🛡️ **Aegis Overwatch**: Autonomous AI-Driven XDR  
**The Zero-Trust, Dual-Hybrid Intelligence Framework**

Aegis Overwatch is a bleeding-edge, autonomous Endpoint Detection and Response (EDR) framework. Unlike traditional signature-based tools, Aegis uses a hybrid mathematical + neural architecture to bridge raw kernel telemetry and high-level cognitive reasoning.

It decouples the **Nervous System** (local sensors + math engine) from the **Brain** (LLM-driven triage) and features a dynamic **Dual-Hybrid Routing System** — cloud-scale AI for speed and an air-gapped Sovereign core as absolute failsafe.

---

### 🏗️ The Aegis Architecture

```mermaid
flowchart LR
    %% Styling
    classDef raw fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px,color:#000
    classDef edge fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px,color:#000
    classDef gateway fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px,color:#000
    classDef cloud fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#000
    classDef govern fill:#ffebee,stroke:#f44336,stroke-width:2px,color:#000
    classDef terminal fill:#e0f2f1,stroke:#00897b,stroke-width:2px,color:#000

    subgraph Edge ["🔒 Phase 1: Sovereign Local Core (Nervous System)"]
        direction TB
        Telemetry["<b>RAW OS TELEMETRY</b><br/><i>Native ETW & WFP Hooks</i>"]:::raw
        Hunter["<b>STRATEGIC DB HUNTER</b><br/><i>Temporal Sweeps & Jitter-Trap Test</i>"]:::edge
        ONNX["<b>DETERMINISTIC EDGE FILTERING</b><br/><i>v35k ONNX & Morphological Math</i>"]:::edge
    end

    subgraph Airlock ["🛡️ Phase 2: Zero-Trust Data Sanitization"]
        direction TB
        Crypto["<b>CRYPTOGRAPHIC GATEWAY</b><br/><i>HMAC-SHA256 PII & Host Masking</i>"]:::gateway
        Semantic["<b>SEMANTIC AIRLOCK</b><br/><i>Neutralizes Prompt-Poisoning & Base64</i>"]:::gateway
    end

    subgraph Actuary ["☁️ Phase 3: Strategic Cloud Actuary (Brain)"]
        direction TB
        Audit["<b>MASTER STRATEGIC AUDIT</b><br/><i>Aggregates 7-Day Nexus Dossier</i>"]:::cloud
        LLM["<b>HOT-SWAPPABLE CLOUD LLM</b><br/><i>MITRE Mapping & Semantic Synthesis</i>"]:::cloud
    end

    subgraph Execution ["⚡ Phase 4: Intent Governance & Remediation"]
        direction TB
        Judge["<b>INTENT GOVERNANCE JUDGE</b><br/><i>Mathematical Veto vs OS Self-Destruction</i>"]:::govern
        WarTerm["<b>WAR TERMINAL UI</b><br/><i>Pre-Staged Actions (Isolate, Dump, Suspend)</i>"]:::terminal
        Learn["<b>CRYPTOGRAPHIC RULE SEALING</b><br/><i>'Mark Safe & Learn' Organic Maturation</i>"]:::terminal
    end

    %% Flow Path
    Telemetry --> Hunter
    Telemetry --> ONNX
    Hunter -->|Drops 95% benign noise| ONNX
    
    ONNX -->|Forwards Abstracted Threat DNA| Crypto
    Hunter -.->|Triggers 12h Slow-and-Low Nexus| Audit
    
    Crypto --> Semantic
    Semantic -->|Air-gapped Context Stream| LLM
    Audit --> LLM
    
    LLM -->|Proposes SOAR Playbook| Judge
    Judge -- "Intent Vetoed (Targeting svchost/lsass)" --> Judge
    Judge -->|"Intent Mathematically Verified"| WarTerm
    
    WarTerm -.->|"Analyst Confirms Benign DevOps"| Learn
    Learn -.->|"Injects Signed Rule to Failsafe"| ONNX
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


