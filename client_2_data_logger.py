# client_2_data_logger.py

import pandas as pd
import asyncio
import sys
from asyncua import Client, ua

# --- CONFIGURATION ---
# Your server URL
SERVER_URL = "opc.tcp://jarvis:53530/OPCUA/SimulationServer" 

# Your Node ID
NODE_RAW_DATA = "ns=3;i=1013" 

# <-- FIX 1: Changed file name to match your 'ls -l' output
DATA_FILE = "data.xlsx"
# ---------------------

async def main():
    print("--- Starting Client-2 (Data Logger) ---")
    
    # 1. Load data from Excel file
    try:
        print(f"Loading data from {DATA_FILE}...")
        
        #
        # --- FIX 2: Changed from read_csv to read_excel ---
        #
        df = pd.read_excel(
            DATA_FILE,
            header=None,    # No header row
            usecols=[1]     # We only want the second column (power data)
        )
        
        # Convert the data to a list of standard Python floats
        power_data = [float(val) for val in df[1].values]
        print(f"Loaded {len(power_data)} data points from {DATA_FILE}.")
    
    except FileNotFoundError:
        print(f"\n--- ERROR ---")
        print(f"File not found: '{DATA_FILE}'")
        print("Please check that the file is in the same directory as this script.")
        print("---")
        return
    except ImportError:
        print("\n--- ERROR ---")
        print("Missing library. Please run: pip install openpyxl")
        print("---")
        return
    except Exception as e:
        print(f"\n--- ERROR ---")
        print(f"Error reading Excel file: {e}")
        print("---")
        return

    # 2. Connect to OPC UA Server and write data
    try:
        async with Client(url=SERVER_URL) as client:
            print(f"Connected to Prosys Server at {SERVER_URL}")
            
            # Get the node
            node = client.get_node(NODE_RAW_DATA)
            
            # Prepare the data as a UA Variant (Array of Doubles)
            value_to_write = ua.Variant(power_data, ua.VariantType.Double)
            
            # 3. Write the data to the node
            await node.write_value(value_to_write)
            
            print(f"Successfully wrote {len(power_data)} points to node {NODE_RAW_DATA}")

    except Exception as e:
        print(f"\n--- ERROR ---")
        print(f"OPC UA Connection Error: {e}")
        print("Could not connect to server. Is it running?")
        print(f"Is the URL '{SERVER_URL}' correct?")
        print(f"Is the NodeID '{NODE_RAW_DATA}' correct?")
        print("---")


if __name__ == "__main__":
    asyncio.run(main())
    print("--- Client-2 finished. ---")