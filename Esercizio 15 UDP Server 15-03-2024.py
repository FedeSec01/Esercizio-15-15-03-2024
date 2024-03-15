import socket

SRV_ADDR = "10.0.2.15" 
SRV_PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SRV_ADDR, SRV_PORT))

print(f"Server UDP in ascolto su {SRV_ADDR}:{SRV_PORT}")

try:
    while True:
        data, address = server_socket.recvfrom(1024)
        print(f"Pacchetto UDP ricevuto da {address}: {data}")

        # Invia una risposta al client
        response = "Risposta dal server UDP"
        server_socket.sendto(response.encode(), address)
        print(f"Risposta inviata a {address}: {response}")

except KeyboardInterrupt:
    print("Server terminato.")
finally:
    server_socket.close()