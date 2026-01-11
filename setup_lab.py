import os
from pathlib import Path

# Define the root of your new development structure
base_dir = Path("Aegis-Lab")

# Standard directory conventions
folders = [
    "data/raw/sysmon",
    "data/raw/network/zeek",
    "data/processed/malicious",
    "data/processed/benign",
    "Aegis-Hydrate-Dev",
]

for folder in folders:
    (base_dir / folder).mkdir(parents=True, exist_ok=True)
    print(f"Created: {base_dir / folder}")