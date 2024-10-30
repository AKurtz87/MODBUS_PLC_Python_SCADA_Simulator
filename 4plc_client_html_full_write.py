from pymodbus.client import ModbusTcpClient
from flask import Flask, jsonify, render_template_string, request
import json

# Funzione per leggere i registri holding
def read_holding_registers(client, unit_id, address, count):
    response = client.read_holding_registers(address, count, slave=unit_id)
    if response.isError():
        print(f"[Errore] Lettura registri holding fallita - Unit ID: {unit_id}, Indirizzo: {address}")
        return None
    else:
        print(f"[Successo] Holding Registers - Unit ID: {unit_id}, Indirizzo: {address}: {response.registers}")
        return response.registers

# Funzione per leggere i registri di input discreti
def read_discrete_inputs(client, unit_id, address, count):
    response = client.read_discrete_inputs(address, count, slave=unit_id)
    if response.isError():
        print(f"[Errore] Lettura registri discreti fallita - Unit ID: {unit_id}, Indirizzo: {address}. Errore: {response}")
        return None
    else:
        bits = response.bits[:count]
        print(f"[Successo] Discrete Inputs - Unit ID: {unit_id}, Indirizzo: {address}: {bits}")
        return bits

# Funzione per scrivere su un coil register
def write_coil(client, unit_id, address, value):
    response = client.write_coil(address, value, slave=unit_id)
    if response.isError():
        print(f"[Errore] Scrittura del coil register fallita - Unit ID: {unit_id}, Indirizzo: {address}")
    else:
        print(f"[Successo] Scrittura su Coil Register - Unit ID: {unit_id}, Indirizzo: {address}, Valore: {value}")

# Funzione principale per eseguire le richieste al server Modbus
def run_client():
    client = ModbusTcpClient("127.0.0.1", port=502)
    client.connect()

    if client.connected:
        try:
            # Lettura dei registri holding di PLC1 e PLC2
            registers_1 = read_holding_registers(client, unit_id=1, address=40000, count=5)
            registers_2 = read_holding_registers(client, unit_id=2, address=40005, count=5)

            # Lettura dei registri di input discreti di PLC1 e PLC2
            inputs_1 = read_discrete_inputs(client, unit_id=1, address=10000, count=5)
            inputs_2 = read_discrete_inputs(client, unit_id=2, address=10005, count=5)
            
            # Restituisce i dati letti
            return {
                "registers_1": registers_1,
                "registers_2": registers_2,
                "inputs_1": inputs_1,
                "inputs_2": inputs_2
            }
        finally:
            client.close()
    else:
        print("[Errore] Impossibile connettersi al server Modbus.")
        return None

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
        
    </style>
<script>
    async function fetchData() {
        try {
            let response = await fetch('/api/data');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            let data = await response.json();
            updateTable(data);
            updateTemperatureAlerts(); // Call this after updating the table
        } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
        }
    }

    function updateTemperatureAlerts() {
        // Select all <td> elements with the class 'temperatureValue'
        const temperatureCells = document.querySelectorAll('td.temperatureValue');

        temperatureCells.forEach((cell) => {
            // Get the value inside the <td> element
            let temperatureValue = parseFloat(cell.textContent);

            if (isNaN(temperatureValue)) {
                // Skip if the value is not a number
                return;
            }

            // Check if the value is >= 12
            if (temperatureValue >= 12) {
                // Add the emoji if it's not already there
                if (!cell.textContent.includes('🚨')) {
                    cell.textContent += ' 🚨';
                }
            } else {
                // Remove the emoji if it's present
                cell.textContent = cell.textContent.replace(' 🚨', '');
            }
        });
    }

    function updateTable(data) {
        let modbusTable = document.getElementById('modbus-table');
        // Aggiungi riga con i valori di temperatura (Holding Registers)
        let registers1 = data.registers_1 || ["N/A", "N/A", "N/A", "N/A", "N/A"];
        let registers2 = data.registers_2 || ["N/A", "N/A", "N/A", "N/A", "N/A"];
        modbusTable.innerHTML = `
            <tr>
                <td>Temperature</td>
                ${registers1.map(value => `<td class="temperatureValue">${value}</td>`).join('')}
                ${registers2.map(value => `<td class="temperatureValue">${value}</td>`).join('')}
            </tr>`;

        // Aggiungi riga con lo stato dei PLC (Discrete Inputs)
        let inputs1 = (data.inputs_1 || []).map(value => value ? "🟢" : "🔴");
        let inputs2 = (data.inputs_2 || []).map(value => value ? "🟢" : "🔴");
        modbusTable.innerHTML += `
            <tr>
                <td>Status</td>
                ${inputs1.map(value => `<td>${value}</td>`).join('')}
                ${inputs2.map(value => `<td>${value}</td>`).join('')}
            </tr>`;

        // Aggiungi riga per la scrittura dei coil
        modbusTable.innerHTML += `
            <tr>
                <td></td>
                ${[...Array(10).keys()].map(i => {
                    const unitId = i < 5 ? 1 : 2;
                    const address = i;
                    return `
                        <td>
                            <button onclick="writeCoil(${unitId}, ${address}, 1)">ON</button>
                            <button onclick="writeCoil(${unitId}, ${address}, 0)">OFF</button>
                        </td>`;
                }).join('')}
            </tr>`;

        // Update the temperature alerts after rendering the table
        updateTemperatureAlerts();
    }

    async function writeCoil(unitId, address, value) {
        try {
            let response = await fetch(`/api/write_coil?unitId=${unitId}&address=${address}&value=${value}`, {
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
    <table id="modbus-table">
    </table>
  </body>
</html>
"""

@app.route('/')
def index():
    # Effettua il rendering della pagina HTML
    return render_template_string(HTML_PAGE)

@app.route('/api/data', methods=['GET'])
def get_data():
    # Ottieni i dati Modbus come JSON
    data = run_client()
    return jsonify(data if data else {"error": "Impossibile ottenere i dati Modbus"})

@app.route('/api/write_coil', methods=['POST'])
def set_coil():
    unit_id = int(request.args.get('unitId'))
    address = int(request.args.get('address'))
    value = bool(int(request.args.get('value')))
    client = ModbusTcpClient("127.0.0.1", port=502)
    client.connect()
    if client.connected:
        try:
            write_coil(client, unit_id=unit_id, address=address, value=value)
        finally:
            client.close()
        return '', 200
    else:
        return jsonify({"error": "Impossibile connettersi al server Modbus"}), 500

if __name__ == "__main__":
    # Avvia il server Flask sulla porta 8000
    app.run(debug=True, port=8000)
