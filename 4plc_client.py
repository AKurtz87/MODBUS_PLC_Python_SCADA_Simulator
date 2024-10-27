import asyncio
from pymodbus.client import AsyncModbusTcpClient

# Funzione per leggere i registri holding
async def read_holding_registers(client, unit_id, address, count):
    response = await client.read_holding_registers(address, count, slave=unit_id)
    if response.isError():
        print(f"Errore nella lettura dei registri holding unit_id={unit_id}, address={address}")
    else:
        print(f"Holding Registers unit_id={unit_id}, address={address}: {response.registers}")

# Funzione per scrivere su un coil register
async def write_coil(client, unit_id, address, value):
    response = await client.write_coil(address, value, slave=unit_id)
    if response.isError():
        print(f"Errore nella scrittura del coil register unit_id={unit_id}, address={address}")
    else:
        print(f"Scrittura su Coil Register unit_id={unit_id}, address={address} riuscita: {value}")

# Funzione per leggere i registri di input discreti
async def read_discrete_inputs(client, unit_id, address, count):
    response = await client.read_discrete_inputs(address, count, slave=unit_id)
    if response.isError():
        print(f"Errore nella lettura dei registri discreti unit_id={unit_id}, address={address}")
    else:
        print(f"Discrete Inputs unit_id={unit_id}, address={address}: {response.bits}")

# Funzione principale per eseguire le richieste al server Modbus
async def run_client():
    client = AsyncModbusTcpClient("127.0.0.1", port=502)
    await client.connect()

    if client.connected:
        while True:
            print("\n--- Menu delle Opzioni ---")
            print("1. Lettura dei registri holding")
            print("2. Scrittura su un coil register")
            print("3. Lettura degli input discreti")
            print("4. Uscita")
            scelta = input("Seleziona un'opzione: ")

            if scelta == '1':
                # Lettura dei registri holding
                unit_id = int(input("Inserisci l'unit ID del PLC: "))
                address = int(input("Inserisci l'indirizzo del registro holding: "))
                count = int(input("Inserisci il numero di registri da leggere: "))
                await read_holding_registers(client, unit_id=unit_id, address=address, count=count)
            elif scelta == '2':
                # Scrittura su un coil register
                unit_id = int(input("Inserisci l'unit ID del PLC: "))
                address = int(input("Inserisci l'indirizzo del coil register: "))
                valore = input("Inserisci il valore (True/False): ").lower() == 'true'
                await write_coil(client, unit_id=unit_id, address=address, value=valore)
            elif scelta == '3':
                # Lettura degli input discreti
                unit_id = int(input("Inserisci l'unit ID del PLC: "))
                address = int(input("Inserisci l'indirizzo degli input discreti: "))
                count = int(input("Inserisci il numero di input da leggere: "))
                await read_discrete_inputs(client, unit_id=unit_id, address=address, count=count)
            elif scelta == '4':
                print("Disconnessione del client...")
                await client.close()
                break
            else:
                print("Opzione non valida. Riprova.")
    else:
        print("Errore nella connessione al server Modbus")

if __name__ == "__main__":
    asyncio.run(run_client())
