import socket
import threading
import datetime
import os

HOST = '0.0.0.0'
PORT = 9998
LOG_FILE = os.path.join(os.path.dirname(__file__), "server_log_textFile.txt")

def write_to_logfile(message: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def handle_client(conn, addr):
    timestamp = datetime.datetime.now()
    message = f"{addr} connected to server"
    border = "=" * len(message)
    log_connect = f"\n{border}\n{message}\n{border}\n"

    print(log_connect)
    write_to_logfile(f"{timestamp} - {message}")
    write_to_logfile(log_connect)

    with conn:
        while True:
            try:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                timestamp = datetime.datetime.now()
                if data.lower() in {"quit", "exit", "no", "q"}:
                    message = f"{addr} disconnected gracefully via command: {data}"
                    border = "=" * len(message)
                    log_exit = f"\n{border}\n{message}\n{border}\n"
                    print(log_exit)
                    write_to_logfile(f"{timestamp} - {addr} sent: {data}")
                    write_to_logfile(log_exit)
                    break

                log_entry = f"{timestamp} - {addr} sent: {data}"
                print(log_entry)
                write_to_logfile(log_entry)

                if data.lower() == "show data":
                    conn.sendall(b"This version does not support local log history.")
                else:
                    conn.sendall(f"Server received: {data}".encode())
            except ConnectionResetError:
                timestamp = datetime.datetime.now()
                message = f"{addr} disconnected unexpectedly"
                border = "=" * len(message)
                log_exit = f"\n{border}\n{message}\n{border}\n"
                print(log_exit)
                write_to_logfile(log_exit)
                break

    print(f"[-] Connection closed: {addr}")

def start_server():
    print(f"[*] Starting server on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
