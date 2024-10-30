# Industrial Control System Simulation using Modbus TCP/IP

This repository contains two scripts that simulate an industrial control system using two Programmable Logic Controllers (PLCs) to control a system of ten air conditioning units. The communication protocol used for controlling these units is **Modbus TCP/IP**. The setup includes a **server-side PLC simulation** and a **client-side HTTP server** that allows users to interact with the system through a web-based HMI (Human-Machine Interface).

## Overview

This simulation involves:
- **Two PLCs** (simulated in a local environment) with IDs **1** and **2**. These PLCs control the air conditioning units.
- **Modbus TCP/IP** protocol is used to communicate between the client and server.
- A **web-based HMI** that allows users to interact with the system through a browser, provided via an HTTP server.
  <img width="1178" alt="Screenshot 2024-10-30 at 08 07 09" src="https://github.com/user-attachments/assets/fdd6f3c8-9c88-4305-9e95-7a60b7e4bebe">


The repository includes two scripts:
https://github.com/AKurtz87/modbus/blob/main/2PLCs_client_web_hmi_modbus.py
1. **`2PLCs_server_modbus.py`**: Simulates two PLCs in a local environment to control the air conditioning units.
2. **`2PLCs_client_web_hmi_modbus.py`**: Implements an HTTP server, providing an HMI that allows user interaction via a web interface.

## Components

### 1. PLC Server (`2PLCs_server_modbus.py`)
- This script simulates **two PLCs** with **IDs 1 and 2**.
- Since the PLCs are simulated locally, the use of unique IP addresses is bypassed by differentiating them based on their IDs.
- The PLCs control **ten air conditioning units** by receiving control commands over the **Modbus TCP/IP** protocol.
- The simulation involves managing three key types of Modbus registers:
  - **Holding Registers**: These registers represent the **temperature values** received from temperature sensors associated with each air conditioning unit. The sensors provide real-time temperature input, which the PLCs use for decision-making.
  - **Discrete Inputs**: These represent the **status (ON/OFF)** of each air conditioning unit. The discrete inputs allow the PLCs to monitor whether each unit is currently active or inactive.
  - **Coils**: These are controlled by the user through the HMI to **turn the air conditioning units ON or OFF**. The coils allow the user to issue direct control commands to each unit through the web interface.

### 2. HTTP Client (`2PLCs_client_web_hmi_modbus.py`)
- This script provides an **HTTP server** that enables a **web-based HMI** for interacting with the PLCs.
- The HMI can be accessed through a browser, allowing users to visualize and control the air conditioning units.
- The client script sends control commands to the simulated PLCs through the Modbus protocol and displays real-time system data.
- Users can view and interact with the system's **holding registers**, **discrete inputs**, and **coils** to manage and monitor the air conditioning units effectively.

## System Operation
Once the server-side and client-side scripts are launched, the system operates as follows:
- The **server script** reads the value of the **discrete inputs** to verify if each air conditioning unit is **ON** or **OFF**.
- If an air conditioning unit is **ON**, the system decreases the corresponding **holding register** value (temperature) by **1 degree** every **10 seconds** to simulate cooling.
- If the unit is **OFF**, the **holding register** value (temperature) increases by **1 degree** every **10 seconds** to simulate a lack of cooling.
- The **temperature changes** are visible in the **HMI**, allowing users to monitor the real-time status of each unit.
- Through the **HMI**, users can manually **turn ON or OFF** the air conditioning units by interacting with the **coils** to maintain an **operating temperature of 7 degrees**.
- The **maximum temperature** that can be reached with all air conditioning units **OFF** is **30 degrees**.

## Features
- **Local Simulation**: Both the PLCs are simulated locally, making it easy to develop and test without actual hardware.
- **Web HMI**: A simple and intuitive HMI that can be accessed via a browser to control the air conditioning units.
- **Modbus TCP/IP Communication**: The use of Modbus for communication between PLCs and the client, which is a common protocol in industrial systems.

## Installation and Usage

### Prerequisites
- Python 3.7 or higher.
- Required Python libraries can be installed via `pip`:

  ```sh
  pip install -r requirements.txt
  ```

- Ensure the `pymodbus` library is installed to handle Modbus TCP/IP communication.

### Running the Simulation

1. **Start the PLC Server**
   - Run the server script to start simulating the PLCs:
     ```sh
     python3 2PLCs_server_modbus.py
     ```
   - This will start two PLCs locally, each managing part of the air conditioning units.

2. **Start the HTTP Client**
   - In a separate terminal, run the client script to start the HTTP server:
     ```sh
     python3 2PLCs_client_web_hmi_modbus.py
     ```
   - Once the server is running, you can access the web-based HMI by opening your browser and navigating to `http://localhost:8000`.

### Web HMI
- The **HMI** allows you to monitor and control the air conditioning units.
- You can adjust setpoints, turn units on or off, and view status data in real-time.
- The HMI provides access to the **holding registers** (temperature values), **discrete inputs** (status of the units), and **coils** (control commands to turn units ON/OFF).

## Folder Structure
- **`2PLCs_server_modbus.py`**: Script for simulating PLCs.
- **`2PLCs_client_web_hmi_modbus.py`**: Script for HTTP server to provide the web HMI.
- **`requirements.txt`**: List of dependencies required to run the scripts.

## Technologies Used
- **Python**: Core language for simulating PLCs and building the HTTP server.
- **Modbus TCP/IP**: Communication protocol for industrial control.
- **HTML/CSS/JavaScript**: Used for building the HMI for user interaction.

## How It Works
- The **server script** simulates two PLCs using Python, each with a distinct ID. It uses **pymodbus** to listen for requests from the client.
- The **client script** implements a simple HTTP server using Flask (or a similar library) to allow users to interact with the PLCs via their web browser.
- Commands issued through the HMI are sent to the server using the Modbus protocol, and responses are displayed on the HMI.
- Users interact with the **holding registers**, **discrete inputs**, and **coils** to monitor temperatures, view unit statuses, and control unit operations.

## Future Enhancements
- **Expand HMI Functionality**: Add more detailed visualizations, graphs, and analytics to the web interface.
- **Security Features**: Implement security features such as authentication for accessing the HMI.
- **Scaling**: Add more PLCs or other devices to simulate a larger industrial environment.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.



## Contact
For any questions or suggestions, please contact [codewars87@gmail.com].

