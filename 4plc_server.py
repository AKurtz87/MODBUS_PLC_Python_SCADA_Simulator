from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
import logging
import threading
import time

# Configurazione del logging
#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

# Definizione dei registri Modbus per i PLC Operativi
# PLC 1: Holding Registers, Coil Registers, Discrete Inputs
data_block_1 = {
    'holding_registers': ModbusSequentialDataBlock(40001, [15, 10, 9, 11, 12]),  # Temperature attuali (Condizionatori 1-5)
    'coil_registers': ModbusSequentialDataBlock(1, [False]*5),     # Comandi ON/OFF (Condizionatori 1-5)
    'discrete_inputs': ModbusSequentialDataBlock(10001, [True, False, True, False, True]) # Stato ON/OFF (Condizionatori 1-5)
}

# PLC 2: Holding Registers, Coil Registers, Discrete Inputs
data_block_2 = {
    'holding_registers': ModbusSequentialDataBlock(40006, [10, 11, 10, 10, 8]),  # Temperature attuali (Condizionatori 6-10)
    'coil_registers': ModbusSequentialDataBlock(6, [False]*5),     # Comandi ON/OFF (Condizionatori 6-10)
    'discrete_inputs': ModbusSequentialDataBlock(10006, [False, True, False, True, False]) # Stato ON/OFF (Condizionatori 6-10)
}

# Creazione dei contesti per i PLC operativi
slave_1 = ModbusSlaveContext(
    di=data_block_1['discrete_inputs'],
    co=data_block_1['coil_registers'],
    hr=data_block_1['holding_registers'],
    ir=data_block_1['holding_registers']
)

slave_2 = ModbusSlaveContext(
    di=data_block_2['discrete_inputs'],
    co=data_block_2['coil_registers'],
    hr=data_block_2['holding_registers'],
    ir=data_block_2['holding_registers']
)

# Configurazione del contesto globale per il server Modbus
# Definizione dei due slave operativi con ID 1 e 2
context = ModbusServerContext(slaves={1: slave_1, 2: slave_2}, single=False)

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
        context[0x01].setValues(2, 10000, coils_1)  # Aggiorna i valori dei discrete inputs (indirizzo 10001-10005)
        
        # Aggiorna gli input discreti del PLC 2 in base ai coil
        coils_2 = context[0x02].getValues(1, 5, count=5)  # Legge i valori dei coil (indirizzo 6-10)
        context[0x02].setValues(2, 10005, coils_2)  # Aggiorna i valori dei discrete inputs (indirizzo 10006-10010)
        
        time.sleep(5)  # Attendi 1 secondo prima di aggiornare nuovamente

# Funzione principale per avviare il server Modbus
def run_server():
    # Avvio del thread per aggiornare i discrete inputs
    update_thread = threading.Thread(target=update_discrete_inputs)
    update_thread.daemon = True
    update_thread.start()
    
    # Avvio del server TCP con i PLC operativi
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 502))

if __name__ == "__main__":
    # Esecuzione del server Modbus sincrono
    run_server()
