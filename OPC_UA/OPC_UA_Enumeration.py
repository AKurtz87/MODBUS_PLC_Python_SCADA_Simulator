import socket
import ipaddress
from opcua import Client
import csv
import os

# Immagine ASCII per l'introduzione
def print_banner():
    banner = """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░╔═══╦═══╦═══╗╔╗░╔╦═══╗╔═══╦═══╦═══╦═╗░╔╗░░░░░░░░░░░
░░░░░░░░░░║╔═╗║╔═╗║╔═╗║║║░║║╔═╗║║╔═╗║╔═╗║╔═╗║║╚╗║║░░░░░░░░░░░
░░░░░░░░░░║║░║║╚═╝║║░╚╝║║░║║║░║║║╚══╣║░╚╣║░║║╔╗╚╝║░░░░░░░░░░░
░░░░░░░░░░║║░║║╔══╣║░╔╗║║░║║╚═╝║╚══╗║║░╔╣╚═╝║║╚╗║║░░░░░░░░░░░
░░░░░░░░░░║╚═╝║║░░║╚═╝║║╚═╝║╔═╗║║╚═╝║╚═╝║╔═╗║║░║║║░░░░░░░░░░░
░░░░░░░░░░╚═══╩╝░░╚═══╝╚═══╩╝░╚╝╚═══╩═══╩╝░╚╩╝░╚═╝░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

  OPC UA Scanner - Find OPC UA Server in a specific Subnet!
    """
    print(banner)

# Fase 1: Scansione della subnet per identificare i server
# Prompt per l'utente per inserire la subnet
print_banner()
subnet = input("Enter the subnet (e.g., 192.168.1.0/24): ")
porta = 4840

def scan_for_servers(subnet, port):
    servers = []
    for ip in ipaddress.IPv4Network(subnet, strict=False):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((str(ip), port)) == 0:
                print(f"Server found: opc.tcp://{ip}:{port}")
                servers.append(f"opc.tcp://{ip}:{port}")
            s.close()
        except Exception as e:
            pass
    return servers

# Scansiona la subnet per individuare i server
servers = scan_for_servers(subnet, porta)

if not servers:
    print("No servers found on the specified subnet.")
    exit()

# Elenca i server trovati e consenti all'utente di scegliere
print("\nServer trovati:")
for idx, server in enumerate(servers):
    print(f"{idx + 1}. {server}")

# Salva i server trovati in un file per l'uso successivo
with open("servers_found.txt", "w") as file:
    for server in servers:
        file.write(f"{server}\n")

print("\nScan complete. The found servers have been saved in 'servers_found.txt'.")

# Fase 2: Selezione e scansione del server
def scan_server(server_url):
    # Crea il client OPC UA
    client = Client(server_url)
    csv_filename = server_url.replace("opc.tcp://", "").replace(":", "_").replace("/", "_") + ".csv"

    # Rimuovi il file CSV esistente se presente, per evitare append
    if os.path.exists(csv_filename):
        os.remove(csv_filename)

    # Funzione per eseguire la scansione dei nodi ricorsivamente e salvarli in CSV
    def scan_node_csv(node, csv_writer, path="Root"):
        try:
            children = node.get_children()
            for child in children:
                # Ottieni le informazioni del nodo
                node_id = str(child.nodeid)
                node_name = child.get_display_name().Text
                current_path = f"{path} -> {node_name}"

                # Scrivi i dati del nodo nel file CSV
                csv_writer.writerow([node_id, node_name, current_path])

                # Richiamo ricorsivo per i figli di questo nodo
                scan_node_csv(child, csv_writer, current_path)
        except Exception as e:
            # Scrivi un errore nel file CSV se non è possibile enumerare i figli
            csv_writer.writerow(["Errore", str(e), path])

    try:
        # Connessione al server
        client.connect()
        print(f"Connected to OPC UA server at address {server_url}")

        # Apri il file CSV per scrivere i risultati della scansione
        with open(csv_filename, "w", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Scrivi l'intestazione del file CSV
            csv_writer.writerow(["NodeId", "Name", "Path"])
            
            # Ottieni il nodo root
            root_node = client.get_root_node()
            print("\nNodes Enumeration:\n")
            
            # Avvia la scansione dal nodo root e salva la struttura in CSV
            scan_node_csv(root_node, csv_writer)

        print(f"Scan complete. The results have been saved in '{csv_filename}'.")

    except Exception as e:
        print(f"Error during connection or scanning: {e}")

    finally:
        # Disconnect from the server
        client.disconnect()
        print("\nDisconnected from the OPC UA server.")

# Loop per permettere all'utente di scansionare diversi server
def main():
    while True:
        # Carica i server salvati
        with open("servers_found.txt", "r") as file:
            servers = [line.strip() for line in file.readlines()]

        # List the found servers and allow the user to choose
        print("\nServers found:")
        for idx, server in enumerate(servers):
            print(f"{idx + 1}. {server}")
        print("0. Exit")

        try:
            server_index = int(input("\nSelect the server by entering the corresponding number (0 to exit): ")) - 1
            if server_index == -1:
                print("Exiting the program.")
                break
            elif server_index < -1 or server_index >= len(servers):
                raise ValueError("Invalid choice.")
            server_url = servers[server_index]
            scan_server(server_url)
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()
