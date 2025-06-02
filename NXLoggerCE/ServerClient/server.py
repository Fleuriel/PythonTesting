import socket
import threading
import datetime

HOST = '0.0.0.0'
PORT = 9999
LOG_FILE = "server_log.txt"

def handle_client(conn, addr):
    timestamp = datetime.datetime.now()
    message = f"{addr} connected to server"
    border = "=" * len(message)
    log_connect = f"\n{border}\n{message}\n{border}\n"

    print(log_connect)
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {message}\n")
        f.write(log_connect + "\n")

    with conn:
        while True:
            try:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                timestamp = datetime.datetime.now()
                log_entry = f"{timestamp} - {addr} sent: {data}"

                print(log_entry)

                if data.lower() == "show data":
                    try:
                        with open(LOG_FILE, "r") as f:
                            lines = f.readlines()[-10:]
                        table = "Recent Logs:\n"
                        table += "-" * 60 + "\n"
                        table += "{:<25} | {:<30}\n".format("Timestamp", "Message")
                        table += "-" * 60 + "\n"
                        for line in lines:
                            parts = line.strip().split(" - ")
                            if len(parts) >= 2:
                                ts = parts[0]
                                msg = " - ".join(parts[1:])
                                table += f"{ts:<25} | {msg[:30]}\n"
                        table += "-" * 60
                        conn.sendall(table.encode())
                    except FileNotFoundError:
                        conn.sendall(b"No data available.")
                elif data.lower() in {"quit", "exit", "no", "q"}:
                    message = f"{addr} disconnected gracefully via command: {data}"
                    border = "=" * len(message)
                    log_exit = f"\n{border}\n{message}\n{border}\n"
                    
                    print(log_exit)
                    with open(LOG_FILE, "a") as f:
                        f.write(f"{timestamp} - {addr} sent: {data}\n")
                        f.write(log_exit + "\n")
                    break
                else:
                    with open(LOG_FILE, "a") as f:
                        f.write(log_entry + "\n")
                    conn.sendall(f"Server received: {data}".encode())
            except ConnectionResetError:
                timestamp = datetime.datetime.now()
                log_exit = (
                    f"\n"
                    f"{'=' * 25}\n"
                    f"DISCONNECTED (UNEXPECTEDLY): {addr}\n"
                    f"{'=' * 25}\n"
                )
                print(log_exit)
                with open(LOG_FILE, "a") as f:
                    f.write(log_exit + "\n")
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
