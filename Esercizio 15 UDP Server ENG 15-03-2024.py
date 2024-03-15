import socket

SRV_ADDR = "10.0.2.15" 
SRV_PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SRV_ADDR, SRV_PORT))

print(f"UDP server listening on {SRV_ADDR}:{SRV_PORT}")

try:
    while True:
        data, address = server_socket.recvfrom(1024)
        print(f"UDP packet received from {address}: {data}")

        # Send a response to the client
        response = "Response from UDP server"
        server_socket.sendto(response.encode(), address)
        print(f"Response sent to {address}: {response}")

except KeyboardInterrupt:
    print("Server terminated.")
finally:
    server_socket.close()