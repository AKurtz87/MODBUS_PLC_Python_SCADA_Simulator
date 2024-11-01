# HMI-PLC System with Docker and PyModbus

Questo progetto utilizza Python e la libreria `pymodbus` per simulare un sistema di condizionamento che comprende 10 unità di condizionamento con 10 sensori di temperatura. Il progetto include uno script client e uno script server che agiscono rispettivamente come HMI (Human Machine Interface) e PLC (Programmable Logic Controller). Utilizzando Docker, è possibile creare immagini del client (HMI) e del server (PLC), facilitando il deploy di HMI e dei PLC in uno scenario operativo realistico.

## Descrizione del Progetto

Il progetto è composto da due componenti principali:

1. **Client (HMI)**: Uno script Python che funziona come interfaccia utente, permettendo di inserire l'indirizzo IP del PLC per prenderne il controllo. L'HMI consente all'utente di accendere e spegnere manualmente le unità di condizionamento.

2. **Server (PLC)**: Uno script Python che simula il comportamento di un PLC. Questo PLC controlla il funzionamento delle unità di condizionamento. Se il condizionatore è acceso, la temperatura viene mantenuta a 8 gradi Celsius; se viene spento, la temperatura aumenta progressivamente fino a 25 gradi.

Le due componenti comunicano tramite il protocollo Modbus, reso possibile grazie alla libreria `pymodbus`.

## Architettura con Docker

Il progetto utilizza Docker per creare le immagini del client (HMI) e del server (PLC). Questo approccio consente di:

- Effettuare il deploy dell'HMI su un container Docker.
- Creare diversi container PLC, ognuno con un indirizzo IP univoco, simulando in questo modo le 10 unità di condizionamento e i loro sensori di temperatura.
- Assicurare che HMI e PLC siano nella stessa subnet per consentire una comunicazione efficace tramite Modbus.

## Scopo del Progetto

Il progetto mira a simulare uno scenario operativo realistico per un sistema di condizionamento composto da 10 unità con 10 sensori di temperatura. L'utente può controllare manualmente le unità di condizionamento tramite l'HMI:

- **Accensione**: Se il condizionatore è acceso, la temperatura viene mantenuta a 8°C.
- **Spegnimento**: Se il condizionatore viene spento, la temperatura aumenta progressivamente fino a raggiungere 25°C.

## Struttura dei File

- **PLC_hmi.py**: Script Python del client HMI.
- **PLC_server.py**: Script Python del server PLC.
- **Dockerfile**: Dockerfile per la creazione dell'immagine del server PLC.
- **Dockerfile.hmi**: Dockerfile per la creazione dell'immagine dell'HMI.
- **requirements.txt**: File contenente le dipendenze necessarie per eseguire i due script, che include `pymodbus` e `flask`.

## Requisiti

Per eseguire il progetto, sono necessari:

- **Docker**: Per creare e gestire i container per il client e i server.
- **Python 3**: Per eseguire gli script.
- **Librerie Python**: Specificate in `requirements.txt`:
  - `pymodbus`: Per la comunicazione Modbus tra HMI e PLC.
  - `flask`: Per gestire l'interfaccia web del client HMI.

## Installazione e Deploy

1. **Creare una rete Docker**:
   ```bash
   docker network create --subnet=172.18.0.0/16 my_network
   ```

1. **Clonare la repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Costruire le immagini Docker**:
   - Per il server PLC:
     ```bash
     docker build -f Dockerfile -t plc_server .
     ```
   - Per il client HMI:
     ```bash
     docker build -f Dockerfile.hmi -t plc_hmi .
     ```

3. **Avviare i container**:
   - Avviare il client HMI:
     ```bash
     docker run -d --name hmi_client --network my_network plc_hmi
     ```
   - Avviare più server PLC, assegnando indirizzi IP univoci:
     ```bash
     docker run -d --name plc_server_1 --network my_network --ip 172.18.0.2 plc_server
     docker run -d --name plc_server_2 --network my_network --ip 172.18.0.3 plc_server
     # Ripetere per tutti i server PLC necessari
     ```

## Utilizzo

- Una volta avviati i container, l'HMI sarà accessibile tramite un'interfaccia web.
- L'utente potrà inserire l'IP di uno dei PLC e prendere il controllo per accendere o spegnere l'unità di condizionamento associata.

## Note

- Assicurarsi che tutti i container siano nella stessa rete Docker per consentire la comunicazione Modbus tra HMI e PLC.
- Si consiglia di utilizzare Docker Compose per facilitare la gestione del deploy di più container.

## License

Questo progetto è distribuito sotto la licenza MIT. Sentiti libero di contribuire e migliorare il codice!

