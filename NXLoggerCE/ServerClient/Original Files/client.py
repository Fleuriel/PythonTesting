import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9999
EXIT_COMMANDS = {'quit', 'q', 'no', 'exit'}

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

print("Client connected. Type commands. Type 'QUIT' or 'NO' to exit.\n")

while True:
    try:
        cmd = input(">> ").strip()
        client_socket.sendall(cmd.encode())
        response = client_socket.recv(4096).decode()
        print(f"Server: {response}")

        if cmd.lower() in EXIT_COMMANDS:
            print("Exiting client.")
            break
    except Exception as e:
        print("Error:", e)
        break

client_socket.close()
