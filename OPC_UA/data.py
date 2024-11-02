from opcua import Client
from datetime import datetime
import time
import csv

# Connessione al server OPC UA
client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()

try:
    print("Client connesso al server OPC UA")
    
    # Ottieni il nodo di Sistema di Condizionamento
    sistema_condizionamento = client.get_objects_node().get_child(["0:SistemaCondizionamento"])
    
    # Apri un file CSV per salvare i dati
    with open('dati_temperatura.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Scrivi l'intestazione
        writer.writerow(["Timestamp"] + [f"Temperatura_Sensore_{i+1}" for i in range(10)])

        while True:
            # Raccogli i dati di temperatura
            timestamp = datetime.now().isoformat()
            temperature = []
            for i in range(10):
                variabile_temperatura = sistema_condizionamento.get_child([f"2:Temperatura_Sensore_{i+1}"])
                valore = variabile_temperatura.get_value()
                temperature.append(valore)

            # Scrivi i dati nel file CSV
            writer.writerow([timestamp] + temperature)
            print(f"Raccolti dati: {temperature}")

            time.sleep(5)  # Raccogli i dati ogni 5 secondi

except KeyboardInterrupt:
    print("Chiusura del client OPC UA...")
finally:
    client.disconnect()
