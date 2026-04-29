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

TARGET_URL = "http://127.0.0.1:8000/drift"
HEADERS = {
    "x-aegis-key": AEGIS_SECRET,
    "x-aegis-signature": hashlib.sha256(b"AEGIS_CORE_AUTHORIZED_RUNTIME").hexdigest(),
    "Content-Type": "application/json"
}

print(f"{Fore.MAGENTA}--- AEGIS PRO: 4-VECTOR NOISE SIMULATOR ---")

payloads = [
    {
        "name": "1. Ransomware DNA + VT WannaCry Hash Test",
        "data": {
            "type": "Process", "eid": 1,
            "data": "vssadmin.exe delete shadows /all /quiet",
            "payload": {
                "Image": "C:\\Windows\\System32\\vssadmin.exe",
                "CommandLine": "vssadmin.exe delete shadows /all /quiet",
                "ParentImage": "C:\\Windows\\System32\\cmd.exe",
                "Hash": "SHA256=24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c",
                "ProcessId": "9991"
            }
        }
    },
    {
        "name": "2. Geopolitical Threat + VT Clean Hash Test",
        "data": {
            "type": "Process", "eid": 1,
            "data": "WeChatAppEx.exe --type=renderer",
            "payload": {
                "Image": "C:\\Program Files\\WeChat\\WeChatAppEx.exe",
                "CommandLine": "WeChatAppEx.exe --type=renderer",
                "ParentImage": "C:\\Program Files\\WeChat\\WeChat.exe",
                "Hash": "SHA256=E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
                "ProcessId": "9992"
            }
        }
    },
    {
        "name": "3. The Log Wiper (Exploit Guard Test)",
        "data": {
            "type": "Process", "eid": 1,
            "data": "wevtutil.exe cl System",
            "payload": {
                "Image": "C:\\Windows\\System32\\wevtutil.exe",
                "CommandLine": "wevtutil.exe cl System",
                "ParentImage": "C:\\Windows\\System32\\powershell.exe",
                "Hash": "NO_HASH_AVAILABLE",
                "ProcessId": "9993"
            }
        }
    },
    {
        "name": "4. Fileless Base64 Obfuscation (Entropy Test)",
        "data": {
            "type": "Process", "eid": 1,
            "data": "powershell.exe -nop -w hidden -EncodedCommand JAB...",
            "payload": {
                "Image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
                "CommandLine": "powershell.exe -nop -w hidden -EncodedCommand JABzAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAEkATwAuAE0AZQBtAG8AcgB5AFMAdAByAGUAYQBtACgAWwBDAG8AbgB2AGUAcgB0AF0AOgA6AEYAcgBvAG0AQgBhAHMAZQA2ADQAUwB0AHIAaQBuAGcAKAAiAEgA",
                "ParentImage": "C:\\Windows\\explorer.exe",
                "Hash": "NO_HASH_AVAILABLE",
                "ProcessId": "9994"
            }
        }
    }
]

for p in payloads:
    print(f"{Fore.CYAN}[🚀] Injecting: {p['name']}")
    try:
        response = sim_client.post(TARGET_URL, json=[p["data"]], headers=HEADERS, timeout=20.0)
        print(f"{Fore.GREEN}    -> Status: {response.status_code}")
    except Exception as e:
        print(f"{Fore.RED}    -> [!] ERROR: {e}")
    time.sleep(1)