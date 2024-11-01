### Guida per la Gestione di Immagini PLC e HMI con Docker Desktop
Ecco come utilizzare Docker Desktop per costruire e gestire le immagini dei PLC e dell'HMI, usando `PLC_server.py` e uno script client, combinando l'interfaccia visuale e alcuni comandi da terminale.

#### 1. Installare Docker Desktop

#### 2. Preparare il Progetto
- Crea una directory di lavoro, ad esempio `modbus_project`, e posiziona al suo interno i file necessari:
  - `PLC_server.py`: il tuo script PLC.
  - `requirements.txt`: un elenco delle librerie Python richieste.

#### 3. Creare un Dockerfile per il PLC
Nella directory di lavoro (`modbus_project`), crea un file `Dockerfile` per costruire l'immagine del PLC. Ecco un esempio:

```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY PLC_server.py /app/PLC_server.py
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 502
CMD ["python", "PLC_server.py"]
```

#### 4. Costruire l'Immagine Docker dal Terminale
- **Apri il terminale** e vai alla directory del progetto:
  ```sh
  cd path/to/modbus_project
  ```
- **Costruisci l'immagine Docker**:
  ```sh
  docker build -t plc_image .
  ```
  Dopo la costruzione, vedrai l'immagine disponibile nella sezione **Images** di Docker Desktop.

#### 5. Creare una Rete Virtuale Docker
Per connettere i tuoi container, crea una rete virtuale:
```sh
docker network create plc_net --subnet=172.16.0.0/24
```
Questa rete (`plc_net`) verrà mostrata nella sezione **Networks** di Docker Desktop.

#### 6. Avviare i Container PLC Usando Docker Desktop
- **Tramite Docker Desktop GUI**:
  - Apri Docker Desktop e vai nella sezione **Images**.
  - Trova `plc_image` e clicca su **Run**.
  - Configura le opzioni:
    - Nome del container: `plc1`
    - Network: `plc_net`

- **Tramite Terminale**:
  ```sh
  docker run -d --network plc_net --name plc1 --ip 172.16.0.2 plc_image
  docker run -d --network plc_net --name plc2 --ip 172.16.0.3 plc_image
  ```
  I container saranno visibili nella sezione **Containers** di Docker Desktop.

#### 7. Creare l'Immagine del Client HMI
Se hai uno script HMI (`4plc_client_html_full_write.py`), crea un altro `Dockerfile` chiamato `Dockerfile.hmi`:

```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY 4plc_client_html_full_write.py /app/4plc_client_html_full_write.py
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "4plc_client_html_full_write.py"]
```

Costruisci l'immagine:
```sh
docker build -t hmi_image -f Dockerfile.hmi .
```
Avvia il container HMI:
```sh
docker run -d --network plc_net --name hmi --ip 172.16.0.4 -p 8000:8000 hmi_image
```

#### 8. Verifica tramite Docker Desktop
- Puoi visualizzare i container in esecuzione nella sezione **Containers**.
- Usa **Logs** per controllare che tutto funzioni correttamente.
- Controlla la sezione **Networks** per verificare le connessioni alla rete `plc_net`.

#### 9. Creare una Semplice Immagine di un Sistema Operativo Linux
Per creare una semplice immagine Docker con un sistema operativo Linux di base, puoi utilizzare un `Dockerfile` come segue:

```Dockerfile
# Usa un'immagine base di Ubuntu
FROM ubuntu:latest

# Aggiorna il sistema e installa alcune utility di base
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    net-tools \
    iputils-ping

# Imposta una directory di lavoro
WORKDIR /root

# Definisce il comando di default per il container
CMD ["bash"]
```

Costruisci l'immagine con il seguente comando:
```sh
docker build -t simple_linux_image .
```

Questa immagine conterrà una versione di Ubuntu con alcune utility di base preinstallate, come `curl`, `vim`, `net-tools`, e `ping`. Potrai eseguire un container basato su questa immagine utilizzando il comando:
```sh
docker run -it simple_linux_image
```


Per eseguire il comando `tcpdump` in background e mantenere il terminale disponibile per altri comandi, puoi seguire questi passaggi:


### TCPDUMP su UBUNTU container per catturare il traffico
Aggiungere `&` alla fine del comando per eseguire `tcpdump` in background:

```sh
sudo tcpdump -i eth0 -w capture.pcap &
```

- Questo manderà il comando in background e restituirà immediatamente il prompt del terminale.
- Dopo averlo inviato in background, il processo verrà assegnato a un **job ID**, e potrai vedere l'ID associato al comando.

### Opzione 2: Usare `nohup` per Non Far Interrompere il Processo
Se desideri che il processo continui a funzionare anche dopo aver chiuso il terminale, puoi usare `nohup`:

```sh
sudo nohup tcpdump -i eth0 -w capture.pcap > tcpdump.log 2>&1 &
```

- **`nohup`**: Assicura che il processo continui a funzionare anche dopo la chiusura del terminale.
- **`> tcpdump.log 2>&1`**: Reindirizza l'output e gli errori a un file chiamato `tcpdump.log`, in modo da poter vedere cosa è successo durante l'esecuzione.
- **`&`**: Manda il processo in background.

### Controllare i Processi in Background
- Dopo aver inviato il comando in background, puoi utilizzare `jobs` per vedere l'elenco dei job in background:
  ```sh
  jobs
  ```
- Questo mostrerà un elenco dei job attivi, con un numero associato a ciascuno di essi.

### Riprendere o Fermare il Processo in Background
- Se vuoi riportare il processo in foreground, puoi usare `fg %<job_id>`:
  ```sh
  fg %1
  ```
  Dove `1` è l'ID del job.
- Se vuoi interrompere il processo, puoi usare `kill` seguito dal **PID** (Process ID), che puoi trovare con `ps` o `jobs`.

### Verifica del Processo
Puoi anche verificare che `tcpdump` stia effettivamente funzionando in background con il comando:

```sh
ps aux | grep tcpdump
```

Questo ti mostrerà tutte le istanze attive di `tcpdump`.

### Riepilogo
- **Esegui in Background**: Aggiungi `&` alla fine del comando.
  ```sh
  sudo tcpdump -i eth0 -w capture.pcap &
  ```
- **Continua dopo la Chiusura del Terminale**: Usa `nohup`.
  ```sh
  sudo nohup tcpdump -i eth0 -w capture.pcap > tcpdump.log 2>&1 &
  ```

Questi metodi ti permetteranno di catturare il traffico di rete in background e utilizzare lo stesso terminale per altri comandi contemporaneamente.
