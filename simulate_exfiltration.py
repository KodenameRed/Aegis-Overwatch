import requests
import random
import string
import time

TARGET = "http://127.0.0.1:8000/dashboard"

def generate_garbage(size_kb):
    """Creates a random string to mimic file data."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size_kb * 1024))

def run_exfiltration():
    print(f"[🔥] COMMENCING EXFILTRATION DRILL...")
    # Generate a 'heavy' payload (e.g., 500 KB of data)
    heavy_data = generate_garbage(500)
    
    for i in range(5):
        print(f" -> Shipping chunk {i+1}/5...")
        try:
            # We send this as a POST with a custom header to look 'suspicious'
            requests.post(TARGET, data={"data": heavy_data}, timeout=1)
        except:
            pass
        time.sleep(0.5)
    
    print("[✅] Exfiltration burst complete.")

if __name__ == "__main__":
    run_exfiltration()
