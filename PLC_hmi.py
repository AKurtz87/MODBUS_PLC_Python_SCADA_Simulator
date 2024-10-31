from pymodbus.client import ModbusTcpClient
from flask import Flask, jsonify, render_template_string, request, redirect, url_for
import json

# Dizionario per i client PLC
clients = {}

# Funzione per creare un nuovo client Modbus
def create_client(ip_address):
    client = ModbusTcpClient(ip_address)
    clients[ip_address] = client
    return client

# Funzione per rimuovere un client Modbus
def remove_client(ip_address):
    # Verifica se il client con l'indirizzo IP esiste nel dizionario
    if ip_address in clients:
        client = clients[ip_address]
        # Chiude la connessione del client Modbus se è ancora aperta
        if client.is_socket_open():
            client.close()
        # Rimuove il client dal dizionario
        del clients[ip_address]
        print(f"Client con IP {ip_address} rimosso con successo.")
    else:
        print(f"Client con IP {ip_address} non trovato.")

# Funzione per leggere i registri holding
def read_holding_registers(client, ip_address, address, count):
    response = client.read_holding_registers(address, count)
    if response.isError():
        print(f"[Errore] Lettura registri holding fallita - IP: {ip_address}, Indirizzo: {address}")
        return None
    else:
        print(f"[Successo] Holding Registers - IP: {ip_address}, Indirizzo: {address}: {response.registers}")
        return response.registers

# Funzione per leggere i registri di input discreti
def read_discrete_inputs(client, ip_address, address, count):
    response = client.read_discrete_inputs(address, count)
    if response.isError():
        print(f"[Errore] Lettura registri discreti fallita - IP: {ip_address}, Indirizzo: {address}. Errore: {response}")
        return None
    else:
        bits = response.bits[:count]
        print(f"[Successo] Discrete Inputs - IP: {ip_address}, Indirizzo: {address}: {bits}")
        return bits

# Funzione per scrivere su un coil register
def write_coil(client, ip_address, address, value):
    response = client.write_coil(address, value)
    if response.isError():
        print(f"[Errore] Scrittura del coil register fallita - IP: {ip_address}, Indirizzo: {address}")
    else:
        print(f"[Successo] Scrittura su Coil Register - IP: {ip_address}, Indirizzo: {address}, Valore: {value}")

# Funzione principale per eseguire le richieste al server Modbus
def run_client():
    data = {}
    for ip_address, client in clients.items():
        client.connect()
        if client.connected:
            try:
                # Lettura dei registri holding
                registers = read_holding_registers(client, ip_address=ip_address, address=40000, count=5)
                # Lettura dei registri di input discreti
                inputs = read_discrete_inputs(client, ip_address=ip_address, address=10001, count=5)
                # Salva i dati
                data[ip_address] = {
                    "registers": registers,
                    "inputs": inputs
                }
            finally:
                client.close()
        else:
            print(f"[Errore] Impossibile connettersi al server Modbus - IP: {ip_address}")
            data[ip_address] = {"error": "Impossibile connettersi al server Modbus"}
    return data

# Inizializza l'applicazione Flask
app = Flask(__name__)

# HTML per la pagina che contiene i dati Modbus
HTML_PAGE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Modbus Data</title>
    <style>
        body { display: flex; flex-direction: column; align-items: center; background-color: #99bedd; }
        table { width: 90%; border-collapse: collapse; margin: 20px 0; font-size: 18px; text-align: center; border: solid; }
        h3 { margin: 0px; }
        th, td { padding: 12px; border-bottom: 1px solid; }
        button { min-width: 45px; }
        form { margin: 20px; }
    </style>
<script>
    async function fetchData() {
        try {
            let response = await fetch('/api/data');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            let data = await response.json();
            updateTables(data);
            updateTemperatureAlerts(); // Call this after updating the table
        } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
        }
    }

    function updateTemperatureAlerts() {
        const temperatureCells = document.querySelectorAll('td.temperatureValue');
        temperatureCells.forEach((cell) => {
            let temperatureValue = parseFloat(cell.textContent);
            if (isNaN(temperatureValue)) {
                return;
            }
            if (temperatureValue >= 12) {
                if (!cell.textContent.includes('🚨')) {
                    cell.textContent += ' 🚨';
                }
            } else {
                cell.textContent = cell.textContent.replace(' 🚨', '');
            }
        });
    }

    function removeTable(ip) {
        let table = document.getElementById(`table-${ip}`);
        let button = document.getElementById(`button-${ip}`);
        let h = document.getElementById(`h3-${ip}`);
        if (table) {
            table.remove();
        }
        if (button) {
            button.remove();
        }
        if (h) {
            h.remove();
        }
    }

    function isDataEmpty(registers, inputs) {
        // Controlla se tutti i valori di 'registers' sono "N/A"
        const allRegistersEmpty = registers.every(value => value === "N/A");
        // Controlla se 'inputs' è vuoto o contiene solo valori null o non validi
        const allInputsEmpty = inputs.length === 0 || inputs.every(value => value === null);
        return allRegistersEmpty && allInputsEmpty;
    }

    function updateTables(data) {
        let tablesContainer = document.getElementById('tables-container');
        tablesContainer.innerHTML = '';

        for (let ip in data) {
            let plcData = data[ip];
            let registers = plcData.registers || ["N/A", "N/A", "N/A", "N/A", "N/A"];
            let inputs = (plcData.inputs || []).map(value => value ? "🟢" : "🔴");

            // Controlla se i dati sono vuoti, se lo sono, ignora la creazione della tabella
            if (isDataEmpty(registers, inputs)) {
                continue;
            }

            tablesContainer.innerHTML += `
                <h3 id="h3-${ip}">PLC IP: ${ip}</h3>
                <form action="/remove_plc" method="post">
                    <input type="hidden" id="ip_address_remove" name="ip_address_remove" value="${ip}">
                    <button type="submit" id="button-${ip}">Elimina Tabella</button>
                </form>
                <table id="table-${ip}">                
                    <tr>
                        <td>Temperature</td>
                        ${registers.map(value => `<td class="temperatureValue">${value}</td>`).join('')}
                    </tr>
                    <tr>
                        <td>Status</td>
                        ${inputs.map(value => `<td>${value}</td>`).join('')}
                    </tr>
                    <tr>
                        <td>Coil Control</td>
                        ${[...Array(5).keys()].map(i => `
                            <td>
                                <button onclick="writeCoil('${ip}', ${i}, 1)">ON</button>
                                <button onclick="writeCoil('${ip}', ${i}, 0)">OFF</button>
                            </td>
                        `).join('')}
                    </tr>
                </table>`;
        }
        updateTemperatureAlerts();
    }

    async function writeCoil(ipAddress, address, value) {
        try {
            let response = await fetch(`/api/write_coil?ipAddress=${ipAddress}&address=${address}&value=${value}`, {
                method: 'POST'
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            fetchData();
        } catch (error) {
            console.error('There has been a problem with your write operation:', error);
        }
    }

    setInterval(fetchData, 5000); // Aggiorna i dati ogni 5 secondi
    window.onload = fetchData; // Carica i dati al caricamento della pagina
</script>

  </head>
  <body>
    <h3>CONDIZIONAMENTO LOCALE AGROALIMENTARE</h3>
    <form action="/add_plc" method="post">
        <label for="ip_address">Indirizzo IP PLC:</label>
        <input type="text" id="ip_address" name="ip_address" required>
        <button type="submit">Aggiungi PLC</button>
    </form>
    <div id="tables-container"></div>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/add_plc', methods=['POST'])
def add_plc():
    ip_address = request.form.get('ip_address')
    if ip_address and ip_address not in clients:
        create_client(ip_address)
    return redirect(url_for('index'))

@app.route('/remove_plc', methods=['POST'])
def remove_plc():
    ip_address = request.form.get('ip_address_remove')
    print(ip_address)
    if ip_address and ip_address in clients:
        remove_client(ip_address)
    return redirect(url_for('index'))

@app.route('/api/data', methods=['GET'])
def get_data():
    data = run_client()
    return jsonify(data if data else {"error": "Impossibile ottenere i dati Modbus"})

@app.route('/api/write_coil', methods=['POST'])
def set_coil():
    ip_address = request.args.get('ipAddress')
    address = int(request.args.get('address'))
    value = bool(int(request.args.get('value')))
    client = clients.get(ip_address)
    if client:
        client.connect()
        if client.connected:
            try:
                write_coil(client, ip_address=ip_address, address=address, value=value)
            finally:
                client.close()
            return '', 200
    return jsonify({"error": "Impossibile connettersi al server Modbus"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
