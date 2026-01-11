import msticpy as mp
from msticpy.dataprovider import data_processor

# Initialize the data provider using the generic factory method
try:
    # This tells MSTICPy to search its internal drivers for 'Mordor'
    mrd = mp.dataprovider.query_provider.QueryProvider("Mordor")
    print("MSTICPy Mordor Data Provider Initialized Successfully.")
except Exception as e:
    print(f"Direct Initialization failed, attempting fallback... Error: {e}")
    # Fallback to the direct import if the factory fails
    from msticpy.data.mordor import MordorData
    mrd = MordorData()

def get_benign_list():
    print("--- Querying OTRF for Benign Datasets ---")
    
    # Retrieve the list using the standardized provider interface
    all_datasets = mrd.list_datasets()
    
    # Filter for 'small', 'normal', or 'background'
    benign_options = [d for d in all_datasets if any(word in d.lower() for word in ["small", "normal", "background"])]
    
    if not benign_options:
        print("No exact matches. Showing the first 10 datasets in the repo:")
        for idx, name in enumerate(all_datasets[:10]):
             print(f"[{idx}] {name}")
        return []

    for idx, name in enumerate(benign_options):
        print(f"[{idx}] {name}")
    
    return benign_options

if __name__ == "__main__":
    options = get_benign_list()