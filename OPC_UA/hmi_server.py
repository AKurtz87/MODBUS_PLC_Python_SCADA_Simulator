from flask import Flask, render_template, request, redirect, url_for
from opcua import Client
import logging

# Configurazione del logging per facilitare il debug
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Connessione al server OPC UA
client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()

@app.route('/')
def index():
    try:
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

        # Recupera lo stato di ciascun condizionatore (ON/OFF)
        condizionatori_stato = []
        for i in range(10):
            stato_condizionatore = sistema_condizionamento.get_child([f"{idx}:Stato_Condizionatore_{i+1}"]).get_value()
            condizionatori_stato.append(stato_condizionatore)

        # Recupera la lista dei sensori in stato di allarme
        sensori_in_allarme = sistema_condizionamento.get_child([f"{idx}:Sensori_In_Allarme"]).get_value()
        sensori_in_allarme_list = sensori_in_allarme.split(", ") if sensori_in_allarme else []

        # Passa i dati al template HTML
        return render_template('dashboard.html', temperature=temperature, 
                               condizionatori_stato=condizionatori_stato,
                               sensori_in_allarme=sensori_in_allarme_list)

    except Exception as e:
        logging.error(f"Errore durante l'accesso al server OPC UA: {e}")
        return "Si è verificato un errore durante la connessione al server OPC UA.", 500

@app.route('/controlla_condizionatore', methods=['POST'])
def controlla_condizionatore():
    try:
        # Ottieni l'indice del namespace
        namespace_array = client.get_namespace_array()
        uri = "http://example.org/deposito_agroalimentare"
        idx = namespace_array.index(uri)

        # Ottieni l'ID del condizionatore e il nuovo stato dal modulo HTML
        condizionatore_id = int(request.form['condizionatore_id'])
        nuovo_stato = request.form['stato'] == 'on'

        # Recupera il nodo corrispondente al condizionatore e aggiorna il suo stato
        sistema_condizionamento = client.get_objects_node().get_child([f"{idx}:SistemaCondizionamento"])
        condizionatore_node = sistema_condizionamento.get_child([f"{idx}:Stato_Condizionatore_{condizionatore_id}"])
        condizionatore_node.set_value(nuovo_stato)

        # Ritorna alla dashboard
        return redirect(url_for('index'))

    except Exception as e:
        logging.error(f"Errore durante il controllo del condizionatore: {e}")
        return "Si è verificato un errore durante l'aggiornamento dello stato del condizionatore.", 500

if __name__ == "__main__":
    app.run(debug=True)
