import socket
import threading
import datetime

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9999
LOG_FILE = "server_log.txt"

clients = []

def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    clients.append(addr)
    with conn:
        while True:
            try:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break
                timestamp = datetime.datetime.now()
                log_entry = f"{timestamp} - {addr} sent: {data}"
                print(log_entry)
                with open(LOG_FILE, "a") as f:
                    f.write(log_entry + "\n")

                # Send response back to client
                response = f"Server received: {data}"
                conn.sendall(response.encode())
            except ConnectionResetError:
                print(f"[-] Client {addr} disconnected abruptly")
                break
    print(f"[-] Connection closed: {addr}")
    clients.remove(addr)

def start_server():
    print(f"[*] Starting server on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()

if __name__ == "__main__":
    start_server()
