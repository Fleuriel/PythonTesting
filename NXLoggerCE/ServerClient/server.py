import socket
import threading
import datetime

HOST = '0.0.0.0'
PORT = 9999
NXLOG_HOST = '127.0.0.1'
NXLOG_PORT = 1514

def send_to_nxlog(message: str):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((NXLOG_HOST, NXLOG_PORT))
            s.sendall((message + "\n").encode())
    except Exception as e:
        print(f"[!] NXLog send failed: {e}")

def handle_client(conn, addr):
    timestamp = datetime.datetime.now()
    message = f"{addr} connected to server"
    border = "=" * len(message)
    log_connect = f"\n{border}\n{message}\n{border}\n"

    print(log_connect)
    send_to_nxlog(f"{timestamp} - {message}")
    send_to_nxlog(log_connect)

    with conn:
        while True:
            try:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                timestamp = datetime.datetime.now()
                log_entry = f"{timestamp} - {addr} sent: {data}"
                print(log_entry)
                send_to_nxlog(log_entry)

                if data.lower() == "show data":
                    conn.sendall(b"This version does not support local log history.")
                elif data.lower() in {"quit", "exit", "no", "q"}:
                    message = f"{addr} disconnected gracefully via command: {data}"
                    border = "=" * len(message)
                    log_exit = f"\n{border}\n{message}\n{border}\n"
                    print(log_exit)
                    send_to_nxlog(f"{timestamp} - {addr} sent: {data}")
                    send_to_nxlog(log_exit)
                    break
                else:
                    conn.sendall(f"Server received: {data}".encode())
            except ConnectionResetError:
                timestamp = datetime.datetime.now()
                message = f"{addr} disconnected unexpectedly"
                border = "=" * len(message)
                log_exit = f"\n{border}\n{message}\n{border}\n"
                print(log_exit)
                send_to_nxlog(log_exit)
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
