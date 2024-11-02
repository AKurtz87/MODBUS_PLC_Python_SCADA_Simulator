from opcua import Server
from datetime import datetime
import time

# Creazione del server OPC UA
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

# Imposta un namespace URI per evitare conflitti di nomi
uri = "http://example.org/deposito_agroalimentare"
idx = server.register_namespace(uri)

# Aggiungi un oggetto che simula il sistema di condizionamento del deposito
sistema_condizionamento = server.nodes.objects.add_object(idx, "SistemaCondizionamento")

# Aggiungi variabili per i 10 sensori di temperatura
sensori_temperatura = []
for i in range(10):
    # Inizializza la temperatura a 25.0
    sensore = sistema_condizionamento.add_variable(idx, f"Temperatura_Sensore_{i+1}", 25.0)
    sensore.set_writable()  # Rendi la variabile scrivibile per testare la scrittura dal client
    sensori_temperatura.append(sensore)

# Aggiungi variabili per indicare lo stato ON/OFF di ciascun condizionatore
condizionatori_stato = []
for i in range(10):
    stato = sistema_condizionamento.add_variable(idx, f"Stato_Condizionatore_{i+1}", False)  # False indica OFF
    stato.set_writable()  # Rendi la variabile scrivibile per poter essere controllato dal client
    condizionatori_stato.append(stato)

# Variabile di allarme critico generale
allarme_critico = sistema_condizionamento.add_variable(idx, "Allarme_Critico", False)
allarme_critico.set_writable()

# Variabile per indicare quali sensori sono in stato di allarme
sensori_in_allarme = sistema_condizionamento.add_variable(idx, "Sensori_In_Allarme", "")
sensori_in_allarme.set_writable()

# Avvio del server
server.start()

try:
    print("Server OPC UA in esecuzione...")
    while True:
        # Simulazione del cambiamento di temperatura e controllo degli allarmi
        allarme = False
        sensori_oltre_soglia = []  # Lista per tenere traccia dei sensori in stato di allarme

        for i, sensore in enumerate(sensori_temperatura):
            # Ottieni lo stato del condizionatore associato
            stato_condizionatore = condizionatori_stato[i].get_value()

            # Ottieni il valore corrente della temperatura
            temperatura_corrente = sensore.get_value()

            # Modifica la temperatura in base allo stato del condizionatore
            if stato_condizionatore:
                # Se il condizionatore è ON, diminuisci la temperatura di 1 grado
                nuova_temperatura = max(temperatura_corrente - 1, 8)  # La temperatura non può scendere sotto 8
            else:
                # Se il condizionatore è OFF, aumenta la temperatura di 1 grado
                nuova_temperatura = min(temperatura_corrente + 1, 25)  # La temperatura non può salire sopra 25

            # Imposta il nuovo valore della temperatura
            sensore.set_value(nuova_temperatura)

            # Stampa la temperatura con un solo decimale
            print(f"Sensore_{i+1}: {nuova_temperatura:.1f} °C")

            # Controlla se la temperatura supera una soglia di sicurezza (ad esempio 24 °C)
            if nuova_temperatura > 12.0:
                allarme = True
                sensori_oltre_soglia.append(f"Sensore_{i+1}")

        # Imposta lo stato dell'allarme critico
        allarme_critico.set_value(allarme)

        # Imposta la lista dei sensori in stato di allarme come una stringa
        sensori_in_allarme_str = ", ".join(sensori_oltre_soglia)
        sensori_in_allarme.set_value(sensori_in_allarme_str)

        if allarme:
            print("ALLARME CRITICO: I seguenti sensori hanno superato la soglia: " + sensori_in_allarme_str)

        # Stampa lo stato corrente di ciascun condizionatore (nessuna modifica automatica dello stato)
        stati_condizionatori_valori = [stato.get_value() for stato in condizionatori_stato]
        print("Stato Condizionatori:", stati_condizionatori_valori)

        time.sleep(10)
except KeyboardInterrupt:
    print("Chiusura del server OPC UA...")
finally:
    server.stop()
