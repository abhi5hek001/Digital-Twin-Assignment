# client_3_arduino.py

import asyncio
import serial
import time
import sys
from asyncua import Client, ua

# --- CONFIGURATION ---
# <-- IMPORTANT: Change this to your Prosys Server's endpoint URL
SERVER_URL = "opc.tcp://jarvis:53530/OPCUA/SimulationServer"

# <-- IMPORTANT: Change these to the Node IDs from your Prosys server
NODE_FORECAST = "ns=3;i=1014"
NODE_OBSERVATION = "ns=3;i=1015"

# <-- IMPORTANT: Change this to your Arduino's Serial Port
ARDUINO_PORT = "/dev/ttyACM0" 
BAUD_RATE = 9600
# ---------------------

async def main():
    print("--- Starting Client-3 (Arduino Interface) ---")
    
    # 1. Connect to Arduino
    try:
        print(f"Attempting to connect to Arduino on {ARDUINO_PORT}...")
        # timeout=1 allows read() to not block forever
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        time.sleep(2) # Wait for serial connection to establish
        print("Arduino connected successfully.")
    except serial.SerialException as e:
        print(f"Error: Could not open serial port {ARDUINO_PORT}.")
        print(f"Details: {e}")
        print("Please check your Arduino connection and port name.")
        return

    # 2. Connect to OPC UA Server
    try:
        async with Client(url=SERVER_URL) as client:
            print(f"Connected to Prosys Server at {SERVER_URL}")
            
            # Get nodes
            forecast_node = client.get_node(NODE_FORECAST)
            observation_node = client.get_node(NODE_OBSERVATION)

            while True:
                try:
                    # 3a. Read forecasted data from Client-1
                    print("\nReading forecasted power from server...")
                    forecast_data = await forecast_node.read_value()
                    
                    if not forecast_data:
                        print("No forecast data found. Waiting 10s...")
                        await asyncio.sleep(10)
                        continue

                    print(f"Received {len(forecast_data)}-hour forecast.")

                    # 3a. Send to Arduino and display on serial monitor (this terminal)
                    print("Sending data to Arduino...")
                    for val in forecast_data:
                        # Format as a string with a newline
                        line = f"{val:.2f}\n" 
                        ser.write(line.encode('utf-8')) # Send as bytes
                        
                        # This print fulfills "display on the serial monitor"
                        print(f"Sent to Arduino: {line.strip()}")
                        await asyncio.sleep(0.5) # Pause to not flood Arduino
                    
                    print("Finished sending data to Arduino.")

                    # 3b. Log max power observation
                    max_power = max(forecast_data)
                    await observation_node.write_value(ua.Variant(max_power, ua.VariantType.Double))
                    print(f"Wrote max power observation ({max_power:.2f}) to server.")
                    
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
    finally:
        ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    asyncio.run(main())