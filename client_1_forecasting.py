# client_1_forecasting.py

import asyncio
import numpy as np
import sys
from asyncua import Client, ua
from statsmodels.tsa.ar_model import AutoReg # Using a simple AutoReg model for forecasting

# --- CONFIGURATION ---
# <-- IMPORTANT: Change this to your Prosys Server's endpoint URL
SERVER_URL = "opc.tcp://jarvis:53530/OPCUA/SimulationServer"

# <-- IMPORTANT: Change these to the Node IDs from your Prosys server
NODE_RAW_DATA = "ns=3;i=1013" 
NODE_FORECAST = "ns=3;i=1014"
NODE_OBSERVATION = "ns=3;i=1015"
# ---------------------

async def main():
    print("--- Starting Client-1 (Forecasting & Monitoring) ---")
    
    try:
        async with Client(url=SERVER_URL) as client:
            print(f"Connected to Prosys Server at {SERVER_URL}")
            
            # Get nodes
            raw_data_node = client.get_node(NODE_RAW_DATA)
            forecast_node = client.get_node(NODE_FORECAST)
            observation_node = client.get_node(NODE_OBSERVATION)

            while True:
                try:
                    # 1a. Read power data from Client-2
                    print("\nReading raw power data from server...")
                    raw_data = await raw_data_node.read_value()
                    
                    if not raw_data or len(raw_data) < 25:
                        print("No raw data (or not enough) found. Waiting 10s...")
                        await asyncio.sleep(10)
                        continue
                    
                    print(f"Received {len(raw_data)} data points.")

                    # 1a. Run forecasting model (AutoReg for 24 steps)
                    print("Running forecasting model for next 24 hours...")
                    # A lag of 24 is suitable for hourly data with daily patterns
                    model = AutoReg(raw_data, lags=24) 
                    model_fit = model.fit()
                    
                    # Predict next 24 hours
                    forecast_values = model_fit.predict(
                        start=len(raw_data), 
                        end=len(raw_data) + 23 # 24 steps total
                    )
                    
                    # Convert numpy floats to standard Python floats for OPC UA
                    forecast_list = [float(val) for val in forecast_values]
                    print(f"Forecast complete. First value: {forecast_list[0]:.2f}")

                    # 1b. Write forecasted data back to server
                    value_to_write = ua.Variant(forecast_list, ua.VariantType.Double)
                    await forecast_node.write_value(value_to_write)
                    print("Wrote 24-hour forecast to server.")

                    # 3b. Read observation from Client-3 and display in terminal
                    max_power_obs = await observation_node.read_value()
                    print(f"\n*** CLIENT-1 TERMINAL DISPLAY ***")
                    print(f"Latest Max Power Observation (from C3): {max_power_obs}\n")
                    
                    # Wait before running the cycle again
                    print("Cycle complete. Waiting 60 seconds...")
                    await asyncio.sleep(60)

                except Exception as e:
                    print(f"An error occurred in the loop: {e}")
                    print("Retrying in 10 seconds...")
                    await asyncio.sleep(10)

    except Exception as e:
        print(f"OPC UA Connection Error: {e}")
        print("Could not connect to server. Is it running?")

if __name__ == "__main__":
    asyncio.run(main())