import asyncio
from pymodbus.server.async_io import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
import logging

# Configurazione del logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Definizione dei registri Modbus per i PLC Operativi
# PLC 1: Holding Registers, Coil Registers, Discrete Inputs
data_block_1 = {
    'holding_registers': ModbusSequentialDataBlock(40001, [0]*5),  # Temperature attuali (Condizionatori 1-5)
    'coil_registers': ModbusSequentialDataBlock(1, [False]*5),     # Comandi ON/OFF (Condizionatori 1-5)
    'discrete_inputs': ModbusSequentialDataBlock(10001, [False]*5) # Stato ON/OFF (Condizionatori 1-5)
}

# PLC 2: Holding Registers, Coil Registers, Discrete Inputs
data_block_2 = {
    'holding_registers': ModbusSequentialDataBlock(40006, [0]*5),  # Temperature attuali (Condizionatori 6-10)
    'coil_registers': ModbusSequentialDataBlock(6, [False]*5),     # Comandi ON/OFF (Condizionatori 6-10)
    'discrete_inputs': ModbusSequentialDataBlock(10006, [False]*5) # Stato ON/OFF (Condizionatori 6-10)
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

# Funzione principale per avviare il server Modbus
async def run_server():
    # Avvio del server TCP con i PLC operativi
    await StartAsyncTcpServer(context, identity=identity, address=("0.0.0.0", 502))

if __name__ == "__main__":
    # Esecuzione del server Modbus asincrono
    asyncio.run(run_server())
