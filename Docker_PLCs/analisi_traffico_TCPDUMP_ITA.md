#### Creare una Semplice Immagine di un Sistema Operativo Linux per effettuare l'analisi del traffico di rete tramite TCPDUMP
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
