# M2M Power Forecasting with OPC UA and Arduino

A Machine-to-Machine (M2M) communication system implementing Industrial IoT (IIoT) standards for predictive power analytics using OPC UA protocol, Python clients, and Arduino hardware.

## 🎥 Demonstration Video

<video width="800" height="450" src="https://github.com/abhi5hek001/Digital-Twin-Assignment/raw/main/group5.webm" autoplay loop muted playsinline></video>

## 🎯 Project Overview

This project demonstrates a complete M2M architecture that simulates real-world industrial data flow:

- **Data Logging**: Historical power consumption data is uploaded to a central OPC UA server
- **Predictive Analytics**: Time-series forecasting predicts the next 24 hours of power usage
- **Physical Integration**: Forecast data is transmitted to an Arduino device for display and monitoring

## 🏗️ System Architecture

```
data.xlsx → Client-2 → [RawPowerData] → OPC UA Server
                                              ↓
                                    [ForecastedPower] ← Client-1 (Forecasting)
                                              ↓
                                         Client-3 → Arduino UNO R4
                                              ↓
                                  [MaxPowerObservation] → Client-1 (Display)
```

### Components

| Component | File | Purpose |
|-----------|------|---------|
| **OPC UA Server** | Prosys Simulation Server | Central data broker hosting all variables |
| **Client-2** | `client_2_data_logger.py` | Uploads 8760 historical data points from Excel |
| **Client-1** | `client_1_forecasting.py` | Runs forecasting model and monitors observations |
| **Client-3** | `client_3_arduino.py` | Interfaces with Arduino via serial communication |
| **Arduino** | `sketch_oct30a.ino` | Displays received power values on Serial Monitor |

### OPC UA Node Structure

The server maintains three key variables under the `MyData` folder:

- **RawPowerData** (Double Array): 8760 historical power measurements
- **ForecastedPower** (Double Array): 24-hour power usage predictions
- **MaxPowerObservation** (Double): Maximum forecasted value for monitoring

## 🚀 Setup Instructions

### Step 1: Configure OPC UA Server

1. Launch **Prosys OPC UA Simulation Server**
2. Navigate to the **Address Space** tab
3. Create folder structure:
   - Right-click **Objects** → Add Node → Folder
   - Name it `MyData`
4. Add three variables inside `MyData`:

| Variable Name | Data Type | Array | Description |
|---------------|-----------|-------|-------------|
| RawPowerData | Double | Yes (1-D) | Historical power data |
| ForecastedPower | Double | Yes (1-D) | 24-hour forecast |
| MaxPowerObservation | Double | No | Maximum forecast value |

5. **Record NodeIDs**: Click each variable and copy its `NodeId` from the Attributes panel (e.g., `ns=3;i=1013`)

### Step 2: Configure Python Scripts

Edit the configuration section in all three client files:

```python
# --- CONFIGURATION ---
SERVER_URL = "opc.tcp://jarvis:53530/OPCUA/SimulationServer" 
NODE_RAW_DATA = "ns=3;i=1013"           # RawPowerData NodeId
NODE_FORECAST = "ns=3;i=1014"           # ForecastedPower NodeId
NODE_OBSERVATION = "ns=3;i=1015"        # MaxPowerObservation NodeId
```

**For `client_3_arduino.py` only**, also configure the Arduino port:

```python
ARDUINO_PORT = "/dev/ttyACM0"  # Linux
```

💡 **Finding your Arduino port:**
- Linux: `ls /dev/ttyACM*`

### Step 3: Configure Arduino

1. Open `sketch_oct30a/sketch_oct30a.ino` in Arduino IDE
2. Connect Arduino UNO R4 to your computer
3. Select: **Tools** → **Board** → Arduino UNO R4
4. Select: **Tools** → **Port** → (your Arduino's port)
5. Click **Upload** ⬆️

## ▶️ Running the Project

You'll need **4 windows** open simultaneously:

### Terminal 1: Data Logger (Run Once)

```bash
conda activate opcua_env
python client_2_data_logger.py
```

**Expected Output:**
```
--- Starting Client-2 (Data Logger) ---
Loading data from data.xlsx...
Loaded 8760 data points from data.xlsx.
Connected to Prosys Server at opc.tcp://jarvis:53530/OPCUA/SimulationServer
Successfully wrote 8760 points to node ns=3;i=1013
--- Client-2 finished. ---
```

### Terminal 2: Forecasting Engine (Continuous)

```bash
conda activate opcua_env
python client_1_forecasting.py
```

**Expected Output:**
```
--- Starting Client-1 (Forecasting & Monitoring) ---
Connected to Prosys Server at opc.tcp://jarvis:53530/OPCUA/SimulationServer
Reading raw power data from server...
Received 8760 data points.
Running forecasting model for next 24 hours...
Forecast complete. First value: 13113.02
Wrote 24-hour forecast to server.

*** CLIENT-1 TERMINAL DISPLAY ***
Latest Max Power Observation (from C3): 19231.00647987835
```

### Terminal 3: Arduino Interface (Continuous)

```bash
conda activate opcua_env
python client_3_arduino.py
```

**Expected Output:**
```
--- Starting Client-3 (Arduino Interface) ---
Attempting to connect to Arduino on /dev/ttyACM0...
Arduino connected successfully.
Connected to Prosys Server at opc.tcp://jarvis:53530/OPCUA/SimulationServer

Reading forecasted power from server...
Received 24-hour forecast.
Sending data to Arduino...
Sent to Arduino: 13113.02
Sent to Arduino: 12301.27
...
Finished sending data to Arduino.
Wrote max power observation (19231.01) to server.
Cycle complete. Waiting 60 seconds...
```

### Window 4: Arduino Serial Monitor

1. Open: **Tools** → **Serial Monitor** in Arduino IDE
2. Set baud rate to **9600** (bottom-right corner)
3. Watch incoming power values display in real-time

## 🔄 Data Flow Summary

1. **Client-2** uploads historical data → `RawPowerData` node
2. **Client-1** reads `RawPowerData` → runs forecast → writes to `ForecastedPower` node
3. **Client-3** reads `ForecastedPower` → sends to Arduino → calculates max → writes to `MaxPowerObservation` node
4. **Client-1** reads `MaxPowerObservation` → displays feedback in terminal
5. Loop continues every 60 seconds

## 📚 Technologies Used

- **OPC UA**: Industry-standard M2M communication protocol
- **Python asyncua**: Asynchronous OPC UA client library
- **Statsmodels**: Time-series forecasting (ARIMA/SARIMAX)
- **PySerial**: Serial communication with Arduino
- **Pandas**: Data manipulation and Excel I/O
- **Arduino**: Physical device integration


---

*This project demonstrates the integration of industrial communication protocols, predictive analytics, and embedded systems in a unified IoT architecture.*
