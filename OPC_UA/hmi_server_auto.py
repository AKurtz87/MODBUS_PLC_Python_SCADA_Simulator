from flask import Flask, render_template, request, redirect, url_for
from opcua import Client
import logging
import time
import threading

# Configurazione del logging per facilitare il debug
logging.basicConfig(level=logging.INFO)

# Configurazione specifica per i logger di opcua
logging.getLogger("opcua.uaprotocol").setLevel(logging.WARNING)
logging.getLogger("opcua.client.ua_client").setLevel(logging.WARNING)
logging.getLogger("opcua").setLevel(logging.WARNING)

app = Flask(__name__, static_folder='static')

# Connessione al server OPC UA
client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()

# Lista dei reattori
reattori = ["ReattoreA", "ReattoreB", "ReattoreC", "ReattoreD"]

@app.route('/')
def index():
    try:
        # Ottieni l'array dei namespace registrati dal server
        namespace_array = client.get_namespace_array()
        uri = "http://example.org/industria_chimica"

        # Trova l'indice del namespace corrispondente all'URI
        try:
            idx = namespace_array.index(uri)
        except ValueError:
            raise ValueError(f"Namespace '{uri}' non trovato. Assicurati che il namespace sia registrato correttamente nel server.")

        # Accedi al nodo ServerUnico utilizzando l'indice del namespace corretto
        sistema_reattori = client.get_objects_node().get_child([f"{idx}:ContestoIndustriale", f"{idx}:ServerUnico"])

        # Recupera i valori di ciascun reattore (A, B, C, D)
        reattori = ["ReattoreA", "ReattoreB", "ReattoreC", "ReattoreD"]
        variabili_reattori = {}
        for reattore in reattori:
            reattore_node = sistema_reattori.get_child([f"{idx}:{reattore}"])
            temperatura = reattore_node.get_child([f"{idx}:Temperatura"]).get_value()
            pressione = reattore_node.get_child([f"{idx}:Pressione"]).get_value()
            livello = reattore_node.get_child([f"{idx}:Livello"]).get_value()
            valvola_mandata = reattore_node.get_child([f"{idx}:ValvolaMandata"]).get_value()
            valvola_scarico = reattore_node.get_child([f"{idx}:ValvolaScarico"]).get_value()
            camicia_riscaldamento = reattore_node.get_child([f"{idx}:CamiciaRiscaldamento"]).get_value()
            agitatore_status = reattore_node.get_child([f"{idx}:AgitatorStatus"]).get_value()
            agitatore_speed = reattore_node.get_child([f"{idx}:AgitatorSpeed"]).get_value()
            variabili_reattori[reattore] = {
                "temperatura": temperatura,
                "pressione": pressione,
                "livello": livello,
                "valvola_mandata": valvola_mandata,
                "valvola_scarico": valvola_scarico,
                "camicia_riscaldamento": camicia_riscaldamento,
                "agitatore_status": agitatore_status,
                "agitatore_speed": agitatore_speed
            }

        # Passa i dati al template HTML
        return render_template('dashboard.html', variabili_reattori=variabili_reattori)

    except Exception as e:
        logging.error(f"Errore durante l'accesso al server OPC UA: {e}")
        return "Si è verificato un errore durante la connessione al server OPC UA.", 500

@app.route('/valvola_mandata_<reattore>', methods=['POST'])
def gestisci_valvola_mandata(reattore):
    try:
        # Ottieni l'indice del namespace
        namespace_array = client.get_namespace_array()
        uri = "http://example.org/industria_chimica"
        idx = namespace_array.index(uri)

        # Recupera la variabile per la Valvola Mandata del reattore specificato
        sistema_reattori = client.get_objects_node().get_child([f"{idx}:ContestoIndustriale", f"{idx}:ServerUnico"])
        valvola_mandata_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:ValvolaMandata"])

        # Ottieni lo stato della valvola dal modulo HTML (0 per chiudere, 1 per aprire)
        stato_valvola = int(request.form['stato_valvola'])
        if stato_valvola not in [0, 1]:
            raise ValueError("Stato della valvola non valido. Deve essere 0 (chiusa) o 1 (aperta).")

        # Imposta il valore della variabile Valvola Mandata (0 = chiusa, 1 = aperta)
        valvola_mandata_var.set_value(stato_valvola)
        stato_valvola_str = "aperta" if stato_valvola == 1 else "chiusa"
        logging.info(f"Valvola {reattore} impostata a: {stato_valvola_str}")

        # Ritorna alla dashboard
        return redirect(url_for('index'))

    except Exception as e:
        logging.error(f"Errore durante la regolazione della valvola di mandata per {reattore}: {e}")
        return "Si è verificato un errore durante l'aggiornamento dei valori", 500

@app.route('/valvola_scarico_<reattore>', methods=['POST'])
def gestisci_valvola_scarico(reattore):
    try:
        # Ottieni l'indice del namespace
        namespace_array = client.get_namespace_array()
        uri = "http://example.org/industria_chimica"
        idx = namespace_array.index(uri)

        # Recupera la variabile per la Valvola Mandata del reattore specificato
        sistema_reattori = client.get_objects_node().get_child([f"{idx}:ContestoIndustriale", f"{idx}:ServerUnico"])
        valvola_scarico_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:ValvolaScarico"])

        # Ottieni lo stato della valvola dal modulo HTML (0 per chiudere, 1 per aprire)
        stato_valvola = int(request.form['stato_valvola'])
        if stato_valvola not in [0, 1]:
            raise ValueError("Stato della valvola non valido. Deve essere 0 (chiusa) o 1 (aperta).")

        # Imposta il valore della variabile Valvola Mandata (0 = chiusa, 1 = aperta)
        valvola_scarico_var.set_value(stato_valvola)
        stato_valvola_str = "aperta" if stato_valvola == 1 else "chiusa"
        logging.info(f"Valvola {reattore} impostata a: {stato_valvola_str}")

        # Ritorna alla dashboard
        return redirect(url_for('index'))

    except Exception as e:
        logging.error(f"Errore durante la regolazione della valvola di scarico per {reattore}: {e}")
        return "Si è verificato un errore durante l'aggiornamento dei valori", 500

@app.route('/camicia_riscaldamento_<reattore>', methods=['POST'])
def gestisci_camicia_riscaldamento(reattore):
    try:
        # Ottieni l'indice del namespace
        namespace_array = client.get_namespace_array()
        uri = "http://example.org/industria_chimica"
        idx = namespace_array.index(uri)

        # Recupera la variabile per la camicia riscaldamento del reattore specificato
        sistema_reattori = client.get_objects_node().get_child([f"{idx}:ContestoIndustriale", f"{idx}:ServerUnico"])
        camicia_riscaldamento_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:CamiciaRiscaldamento"])
    
        stato_riscaldamento = int(request.form['stato_riscaldamento'])
        if stato_riscaldamento not in [0, 1]:
            raise ValueError("Stato del riscaldamento non valido. Deve essere 0 (spento) o 1 (acceso).")
  
        camicia_riscaldamento_var.set_value(stato_riscaldamento)
        stato_riscaldamento_str = "acceso" if stato_riscaldamento == 1 else "spento"
        logging.info(f"Valvola {reattore} impostata a: {stato_riscaldamento_str}")

        # Ritorna alla dashboard
        return redirect(url_for('index'))

    except Exception as e:
        logging.error(f"Errore durante la regolazione del riscaldamento per {reattore}: {e}")
        return "Si è verificato un errore durante l'aggiornamento dei valori", 500

@app.route('/agitatore_status_<reattore>', methods=['POST'])
def gestisci_agitatore_status(reattore):
    try:
        # Ottieni l'indice del namespace
        namespace_array = client.get_namespace_array()
        uri = "http://example.org/industria_chimica"
        idx = namespace_array.index(uri)

        # Recupera la variabile per lo stato dell'agitatore del reattore specificato
        sistema_reattori = client.get_objects_node().get_child([f"{idx}:ContestoIndustriale", f"{idx}:ServerUnico"])
        agitatore_status_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:AgitatorStatus"])

        # Ottieni lo stato dell'agitatore dal modulo HTML (True per accendere, False per spegnere)
        stato_agitatore = request.form['stato_agitatore'].lower() == 'true'
        
        # Imposta il valore della variabile AgitatorStatus
        agitatore_status_var.set_value(stato_agitatore)
        stato_agitatore_str = "acceso" if stato_agitatore else "spento"
        logging.info(f"Agitatore {reattore} impostato a: {stato_agitatore_str}")

        # Ritorna alla dashboard
        return redirect(url_for('index'))

    except Exception as e:
        logging.error(f"Errore durante la regolazione dello stato dell'agitatore per {reattore}: {e}")
        return "Si è verificato un errore durante l'aggiornamento dei valori", 500

@app.route('/agitatore_speed_<reattore>', methods=['POST'])
def gestisci_agitatore_speed(reattore):
    try:
        # Ottieni l'indice del namespace
        namespace_array = client.get_namespace_array()
        uri = "http://example.org/industria_chimica"
        idx = namespace_array.index(uri)

        # Recupera la variabile per la velocità dell'agitatore del reattore specificato
        sistema_reattori = client.get_objects_node().get_child([f"{idx}:ContestoIndustriale", f"{idx}:ServerUnico"])
        agitatore_speed_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:AgitatorSpeed"])

        # Ottieni la velocità dell'agitatore dal modulo HTML
        velocita_agitatore = int(request.form['velocita_agitatore'])
        
        # Verifica che la velocità sia compresa tra 0 e 300
        if not (0 <= velocita_agitatore <= 300):
            raise ValueError("Velocità dell'agitatore non valida. Deve essere compresa tra 0 e 300 RPM.")
        
        # Imposta il valore della variabile AgitatorSpeed
        agitatore_speed_var.set_value(velocita_agitatore)
        logging.info(f"Velocità dell'agitatore {reattore} impostata a: {velocita_agitatore} RPM")

        # Ritorna alla dashboard
        return redirect(url_for('index'))

    except Exception as e:
        logging.error(f"Errore durante la regolazione della velocità dell'agitatore per {reattore}: {e}")
        return "Si è verificato un errore durante l'aggiornamento dei valori", 500

# Funzione del ciclo di automazione per un singolo reattore
def ciclo_reattore(reattore, idx, sistema_reattori):
    try:
        logging.info(f"Avvio del ciclo per il reattore {reattore}.")

        while True:
            # 1. Apertura della valvola di mandata
            valvola_mandata_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:ValvolaMandata"])
            valvola_mandata_var.set_value(1)

            # 2. Controllare il livello fino a 90.0
            while True:
                livello_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:Livello"])
                livello = livello_var.get_value()
                if livello >= 90.0:
                    logging.info(f"Reattore {reattore}: Livello raggiunto ({livello}).")
                    break
                time.sleep(1)

            # 3. Chiudere la valvola di mandata
            valvola_mandata_var.set_value(0)

            # 4. Impostare velocità degli agitatori a 60 RPM
            agitatore_speed_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:AgitatorSpeed"])
            agitatore_speed_var.set_value(60)

            # 5. Accendere gli agitatori
            agitatore_status_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:AgitatorStatus"])
            agitatore_status_var.set_value(True)

            # 6. Accendere i riscaldamenti
            camicia_riscaldamento_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:CamiciaRiscaldamento"])
            camicia_riscaldamento_var.set_value(1)

            # 7. Attendere 600 secondi
            logging.info(f"Reattore {reattore}: Attesa di 600 secondi.")
            time.sleep(120)

            # 8. Spegnere gli agitatori
            agitatore_status_var.set_value(False)

            # 9. Spegnere il riscaldamento
            camicia_riscaldamento_var.set_value(0)

            # 10. Attendere che la temperatura scenda <= 30 gradi
            while True:
                temperatura_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:Temperatura"])
                temperatura = temperatura_var.get_value()
                if temperatura <= 30.0:
                    logging.info(f"Reattore {reattore}: Temperatura scesa a {temperatura} gradi.")
                    break
                time.sleep(1)

            # 11. Aprire la valvola di scarico
            valvola_scarico_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:ValvolaScarico"])
            valvola_scarico_var.set_value(1)

            # 12. Aspettare che il livello scenda a 0
            while True:
                livello_var = sistema_reattori.get_child([f"{idx}:{reattore}", f"{idx}:Livello"])
                livello = livello_var.get_value()
                if livello <= 5.0:
                    logging.info(f"Reattore {reattore}: Livello sceso a {livello}.")
                    break
                time.sleep(1)

            # 13. Chiudere la valvola di scarico
            valvola_scarico_var.set_value(0)

            # 14. Attendere 60 secondi
            logging.info(f"Reattore {reattore}: Attesa finale di 60 secondi.")
            time.sleep(60)

            logging.info(f"Reattore {reattore}: Ciclo completato. Ricomincio.")
    except Exception as e:
        logging.error(f"Errore nel ciclo del reattore {reattore}: {e}")

# Funzione principale per avviare i thread
def automazione_indipendente():
    try:
        namespace_array = client.get_namespace_array()
        uri = "http://example.org/industria_chimica"
        idx = namespace_array.index(uri)

        sistema_reattori = client.get_objects_node().get_child([f"{idx}:ContestoIndustriale", f"{idx}:ServerUnico"])

        # Creazione e avvio di un thread per ciascun reattore
        for reattore in reattori:
            threading.Thread(target=ciclo_reattore, args=(reattore, idx, sistema_reattori), daemon=True).start()
            logging.info(f"Thread avviato per il reattore {reattore}.")

    except Exception as e:
        logging.error(f"Errore nell'avvio dell'automazione: {e}")

# Avvio dell'automazione all'avvio dell'applicazione
threading.Thread(target=automazione_indipendente, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)

