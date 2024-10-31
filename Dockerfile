# Usa un'immagine base di Python ufficiale
FROM python:3.9-slim

# Imposta una directory di lavoro nel container
WORKDIR /app

# Copia il file dello script PLC e le dipendenze nel container
COPY PLC_server.py /app/PLC_server.py
COPY requirements.txt /app/requirements.txt

# Installa le dipendenze Python necessarie
RUN pip install --no-cache-dir -r requirements.txt

# Espone la porta 502 (Modbus TCP/IP standard)
EXPOSE 502

# Definisce il comando per avviare il server PLC
CMD ["python", "PLC_server.py"]
