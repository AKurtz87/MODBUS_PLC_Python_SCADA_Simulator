from opcua import Client
import time

# Connessione al server OPC UA
client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()

try:
    print("Client connesso al server OPC UA")
    
    # Ottieni l'array dei namespace registrati dal server
    namespace_array = client.get_namespace_array()
    uri = "http://example.org/deposito_agroalimentare"
    
    # Trova l'indice del namespace corrispondente all'URI
    try:
        idx = namespace_array.index(uri)
    except ValueError:
        raise ValueError(f"Namespace '{uri}' non trovato. Assicurati che il namespace sia registrato correttamente nel server.")

    # Accedi al nodo SistemaCondizionamento utilizzando l'indice del namespace corretto
    sistema_condizionamento = client.get_objects_node().get_child([f"{idx}:SistemaCondizionamento"])

    # Recupera i valori di temperatura dai sensori
    temperature = []
    for i in range(10):
        variabile_temperatura = sistema_condizionamento.get_child([f"{idx}:Temperatura_Sensore_{i+1}"])
        valore = variabile_temperatura.get_value()
        temperature.append(valore)
        print(f"Sensore_{i+1}: {valore:.2f} °C")
    
    # Controlla lo stato dell'allarme critico
    allarme_critico = sistema_condizionamento.get_child([f"{idx}:Allarme_Critico"]).get_value()
    if allarme_critico:
        print("ALLARME CRITICO ATTIVO!")

except Exception as e:
    print(f"Errore: {e}")

finally:
    client.disconnect()
