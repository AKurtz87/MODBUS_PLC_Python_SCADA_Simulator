# Industrial Control System Simulation using Modbus TCP/IP

This repository contains scripts simulating an industrial control system for managing 10 air conditioning units using **Modbus TCP/IP** communication protocol. The system includes a **server-side PLC simulation**, a **client-side HTTP server**, and two web-based interfaces for monitoring and controlling the units.

## Overview

### Key Components:
1. **Two PLCs** (simulated locally) with IDs **1** and **2**.
2. **Modbus TCP/IP** protocol for client-server communication.
3. **Web-based HMIs**:
   - **Control Dashboard**: Allows monitoring and controlling air conditioning units.
   - **Temperature Graph Interface**: Displays temperature trends over time.

## Components and Functionality

### 1. PLC Server (`2PLCs_server_modbus.py`)
- Simulates **two PLCs** (IDs 1 and 2) locally, managing 10 air conditioning units.
- Manages three types of Modbus registers:
  - **Holding Registers**: Store real-time temperature data.
  - **Discrete Inputs**: Represent the ON/OFF status of the air conditioning units.
  - **Coils**: Allow user control to turn units ON or OFF via the HMI.
- Behavior:
  - Units decrease the temperature by **1°C every 10 seconds** when ON.
  - Units increase the temperature by **1°C every 10 seconds** when OFF.
  - Target operating temperature is **7°C**; maximum temperature is **30°C**.

### 2. Client (`2PLCs_client_web_hmi_modbus_graph.py`)
- Implements an **HTTP server** providing web-based HMIs.
- Communicates with the PLCs via Modbus protocol.
- Includes two interfaces:
  - **Dashboard HMI (`dashboard.html`)**:
    - Displays real-time data for temperature, status, and controls.
    - Allows users to turn units ON/OFF.
    - Highlights high temperatures (≥12°C) with 🚨 alerts.
  - **Graph Interface (`graph.html`)**:
    - Displays real-time temperature graphs for all 10 units.
    - Uses **Chart.js** for dynamic graph updates.
    - Highlights critical conditions with visual cues.

### 3. AC System Operation
Once the server-side and client-side scripts are launched, the system operates as follows:
- The **server script** reads the value of the **discrete inputs** to verify if each air conditioning unit is **ON** or **OFF**.
- If an air conditioning unit is **ON**, the system decreases the corresponding **holding register** value (temperature) by **1 degree** every **10 seconds** to simulate cooling.
- If the unit is **OFF**, the **holding register** value (temperature) increases by **1 degree** every **10 seconds** to simulate a lack of cooling.
- The **temperature changes** are visible in the **HMI**, allowing users to monitor the real-time status of each unit.
- Through the **HMI**, users can manually **turn ON or OFF** the air conditioning units by interacting with the **coils** to maintain an **operating temperature of 7 degrees**.
- The **maximum temperature** that can be reached with all air conditioning units **OFF** is **30 degrees**.

### Web Interfaces

#### Dashboard HMI
- Features:
  - Real-time temperature, status, and control actions.
  - Alerts for high temperatures (≥12°C) with 🚨.
  - Buttons for ON/OFF control of each unit.
- Background: Air-conditioning-themed design.


#### Graph Interface
- Features:
  - Line graphs showing temperature trends.
  - Updates every 5 seconds.
  - Color-coded temperature thresholds for clear visualization.
- Design: Minimalist, responsive layout with color-coded graphs.

<img width="1422" alt="Screenshot 2024-11-15 at 14 56 28" src="https://github.com/user-attachments/assets/8f0c7775-9023-46fc-a918-fdda70e71cbf">

## Installation and Usage

### Prerequisites
- Python 3.7 or higher.
- Install dependencies using:
  ```bash
  pip install -r requirements.txt
  ```

### Running the Simulation
1. **Start the PLC Server**:
   ```bash
   python3 2PLCs_server_modbus.py
   ```
   - Simulates the PLCs and initializes Modbus registers.

2. **Start the Client**:
   ```bash
   python3 2PLCs_client_web_hmi_modbus_graph.py
   ```
   - Starts the HTTP server providing access to the HMIs.

3. **Access the HMIs**:
   - **Control Dashboard**: `http://localhost:8000/dashboard`
   - **Graph Interface**: `http://localhost:8000/graph`

## Folder Structure
- `2PLCs_server_modbus.py`: PLC simulation script.
- `2PLCs_client_web_hmi_modbus_graph.py`: HTTP server for HMIs.
- `templatess/dashboard.html`: Control and status interface.
- `templates/graph.html`: Temperature graph visualization interface.
- `requirements.txt`: List of Python dependencies.

## Technologies Used
- **Python**: Core simulation and server.
- **Modbus TCP/IP**: Industrial communication protocol.
- **Flask**: HTTP server for web-based interfaces.
- **Chart.js**: Interactive temperature graphs.
- **HTML/CSS/JavaScript**: Web HMI development.

## Features
- Real-time temperature control and monitoring.
- Dynamic graph visualization.
- Scalable design for additional features.

## Contact
For questions or suggestions, contact [codewars87@gmail.com].

