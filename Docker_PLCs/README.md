# HMI-PLC System with Docker and PyModbus

This project uses Python and the `pymodbus` library to simulate an air conditioning system consisting of 5 conditioning units with 5 temperature sensors controlled by a PLC. The project includes a client script and a server script that act respectively as the HMI (Human Machine Interface) and the PLC (Programmable Logic Controller). Using Docker, you can create images of both the client (HMI) and the server (PLC), making it easier to deploy the HMI and PLCs in a realistic operational scenario.

## Project Description

The project is made up of two main components:

1. **Client (HMI)**: A Python script that works as a user interface, allowing the user to input the PLC's IP address to take control of it. The HMI allows the user to manually turn the air conditioning units on and off.

2. **Server (PLC)**: A Python script that simulates the behavior of a PLC. This PLC controls the functioning of the air conditioning units. When the air conditioner is on, the temperature is maintained at 8 degrees Celsius; if turned off, the temperature gradually increases up to 25 degrees.

These two components communicate using the Modbus protocol, facilitated by the `pymodbus` library.

## Docker Architecture

The project uses Docker to create images of the client (HMI) and the server (PLC). This approach enables you to:

- Deploy the HMI on a Docker container.
- Create multiple PLC containers, each with a unique IP address, thereby simulating a set of 5 air conditioning units and their temperature sensors.
- Ensure that the HMI and PLC are on the same subnet to allow effective communication using Modbus.

## Project Objective

The project aims to simulate a realistic operational scenario for an air conditioning system consisting of 5 units with 5 temperature sensors. The user can manually control the air conditioning units via the HMI:

- **Turn On**: If the air conditioner is on, the temperature is maintained at 8°C.
- **Turn Off**: If the air conditioner is turned off, the temperature progressively rises until it reaches 25°C.

## File Structure

- **PLC\_hmi.py**: Python script for the HMI client.
- **PLC\_server.py**: Python script for the PLC server.
- **Dockerfile**: Dockerfile for building the PLC server image.
- **Dockerfile.hmi**: Dockerfile for building the HMI image.
- **requirements.txt**: File containing the necessary dependencies for running both scripts, including `pymodbus` and `flask`.

## Requirements

To run the project, you need:

- **Docker**: To create and manage the containers for both the client and server.
- **Python 3**: To run the scripts.
- **Python Libraries**: Specified in `requirements.txt`:
  - `pymodbus`: For Modbus communication between HMI and PLC.
  - `flask`: To handle the HMI web interface.

## Installation and Deployment

1. **Create a Docker Network**:

   ```bash
   docker network create --subnet=172.18.0.0/16 my_network
   ```

2. **Clone the Repository**:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

3. **Build Docker Images**:

   - For the PLC server:
     ```bash
     docker build -f Dockerfile -t plc_server .
     ```
   - For the HMI client:
     ```bash
     docker build -f Dockerfile.hmi -t plc_hmi .
     ```

4. **Start the Containers**:

   - Start the HMI client and map the port to view it in the browser:
     ```bash
     docker run -d --network my_network --name hmi --ip 172.18.0.4 -p 8000:8000 plc_hmi
     ```
     This command starts the HMI container, maps port 8000 from localhost to port 8000 in the container, and assigns a unique IP address to the HMI. This way, the HMI will be accessible via the browser at `http://localhost:8000`.

   - Start multiple PLC servers, assigning unique IP addresses:
     ```bash
     docker run -d --name plc_server_1 --network my_network --ip 172.18.0.2 plc_server
     docker run -d --name plc_server_2 --network my_network --ip 172.18.0.3 plc_server
     # Repeat for all necessary PLC servers
     ```

## Usage

- Once the containers are up and running, the HMI will be accessible via a web interface.
- The user can input the IP of one of the PLCs and take control to turn the associated air conditioning unit on or off.

## Notes

For more details on virtualization using Docker, you can refer to the following link: [Docker\_PLCs/dockerize.md](Docker_PLCs/dockerize.md)

- Ensure that all containers are on the same Docker network to enable Modbus communication between the HMI and PLC.
- It is recommended to use Docker Compose for easier management of deploying multiple containers.

