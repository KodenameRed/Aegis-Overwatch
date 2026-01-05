import xml.etree.ElementTree as ET
import pandas as pd
import os

def load_aegis_data(filename="Sysmon_Report_Final.xml"):
    """
    Parses the local Sysmon XML and extracts features 
    based on the sysmon_config.txt filters.
    """
    if not os.path.exists(filename):
        print(f"[!] Error: {filename} not found in the current folder.")
        return None

    # Standard Windows Event Namespace
    ns = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}
    
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        records = []

        for event in root.findall('ns:Event', ns):
            # Extract Event ID (e.g., 1 for Process Create)
            eid = event.find('.//ns:EventID', ns).text
            
            # Extract Data fields (CommandLine, Image, ParentImage, User)
            data_points = {d.get('Name'): d.text for d in event.findall('.//ns:Data', ns)}
            data_points['EventID'] = eid
            
            records.append(data_points)

        df = pd.DataFrame(records)
        print(f"[*] Successfully loaded {len(df)} events from {filename}")
        return df

    except Exception as e:
        print(f"[!] Critical Error: {e}")
        return None

def main():
    # 1. Ingest Data
    df = load_aegis_data()
    
    if df is not None:
        # 2. Quick Security Summary
        print("\n--- Security Log Overview ---")
        print(f"Total Events: {len(df)}")
        
        # Check for Process Create (EventID 1)
        if 'EventID' in df.columns:
            proc_count = len(df[df['EventID'] == '1'])
            print(f"Process Creation Events: {proc_count}")
            
        # 3. Feature Preview
        # We only show columns that exist in your current log data
        cols = [c for c in ['Image', 'CommandLine', 'ParentImage'] if c in df.columns]
        if cols:
            print("\n--- Telemetry Preview ---")
            print(df[cols].tail(5))

if __name__ == "__main__":
    main()