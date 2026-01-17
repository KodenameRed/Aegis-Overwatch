import requests
import concurrent.futures
import time

# Target the Hive's own dashboard
TARGET = "http://127.0.0.1:8000/dashboard"

def send_request():
    try:
        # We use a short timeout to keep the "attack" fast
        requests.get(TARGET, timeout=0.1)
    except:
        pass

def run_simulation():
    print(f"\n[🔥] ATTACK COMMENCING: Targeting {TARGET}")
    print("[!] Ensure the Sentinel is in the [2/3] ATTACK WINDOW now!")
    
    # Use ThreadPoolExecutor to send requests in parallel (mimics a burst)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Sending 200 rapid requests
        futures = [executor.submit(send_request) for _ in range(200)]
        concurrent.futures.wait(futures)

    print("[✅] Burst complete. Wait for Sentinel to ship the logs to Hive.")

if __name__ == "__main__":
    run_simulation()
