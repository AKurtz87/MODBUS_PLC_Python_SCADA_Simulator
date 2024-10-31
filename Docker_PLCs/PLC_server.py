from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
#import logging
import threading
import time

# Definizione dei registri Modbus per i PLC Operativi
# PLC 1: Holding Registers, Coil Registers, Discrete Inputs
data_block_1 = {
    'holding_registers': ModbusSequentialDataBlock(40001, [15, 10, 9, 11, 12]),  # Temperature attuali (Condizionatori 1-5)
    'coil_registers': ModbusSequentialDataBlock(1, [False]*5),     # Comandi ON/OFF (Condizionatori 1-5)
    'discrete_inputs': ModbusSequentialDataBlock(10001, [False]*5) # Stato ON/OFF (Condizionatori 1-5)
}

# Creazione del contesto per il PLC 1
slave_1 = ModbusSlaveContext(
    di=data_block_1['discrete_inputs'],
    co=data_block_1['coil_registers'],
    hr=data_block_1['holding_registers'],
    ir=data_block_1['holding_registers']
)

# Creazione del contesto globale per il server Modbus
# Definizione dei due slave operativi con ID 1
context = ModbusServerContext(slaves={1: slave_1}, single=False)

# Identificazione del dispositivo Modbus
identity = ModbusDeviceIdentification()
identity.VendorName = 'OpenAI Example Vendor'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Modbus Server'
identity.ModelName = 'Modbus Server Model'
identity.MajorMinorRevision = '1.0'

# Funzione per aggiornare i discrete inputs in base ai valori dei coil
def update_discrete_inputs():
    while True:
        # Aggiorna gli input discreti del PLC 1 in base ai coil
        coils_1 = context[0x01].getValues(1, 0, count=5)  # Legge i valori dei coil (indirizzo 1-5)
        context[0x01].setValues(2, 10001, coils_1)  # Aggiorna i valori dei discrete inputs (indirizzo 10001-10005)

        # Legge i discrete inputs (indirizzi 10001-10005)
        discrete_inputs = context[0x01].getValues(2, 10001, count=5)
        print(discrete_inputs)

        # Legge i primi cinque holding registers (indirizzi 40000-40004)
        holding_registers = context[0x01].getValues(3, 40000, count=5)
        print(holding_registers)
        
        # Aggiorna ciascun holding register in base al valore del discrete input
        for i in range(5):
            if discrete_inputs[i]:  # Se il discrete input è True
                if holding_registers[i] > 8:
                    holding_registers[i] -= 1  # Diminuisce di 1 il valore del holding register
            else:  # Se il discrete input è False
                if holding_registers[i] < 25:
                    holding_registers[i] += 1  # Aumenta di 1 il valore del holding register

        # Aggiorna i primi cinque holding registers con i nuovi valori
        context[0x01].setValues(3, 40000, holding_registers)

        time.sleep(5)  # Attendi 5 secondi prima di aggiornare nuovamente



# Funzione principale per avviare il server Modbus
def run_server():
    # Avvio del thread per aggiornare i discrete inputs
    update_thread = threading.Thread(target=update_discrete_inputs)
    update_thread.daemon = True
    update_thread.start()

    # Avvio del server TCP con il PLC operativo
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 502))

if __name__ == "__main__":
    # Esecuzione del server Modbus sincrono
    run_server()