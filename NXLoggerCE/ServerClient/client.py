from pynput import keyboard
import socket
import threading

SERVER_IP = '127.0.0.1'  # Change this to your server IP
SERVER_PORT = 9999
ALLOWED_KEYS = {'w', 'a', 's', 'd', 'q'}

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

def on_press(key):
    try:
        k = key.char.lower()
        if k in ALLOWED_KEYS:
            client_socket.sendall(k.encode())
            if k == 'q':
                print("Exiting...")
                client_socket.close()
                return False  # Stop listener
            # Receive server response
            response = client_socket.recv(1024).decode()
            print(f"Server: {response}")
    except AttributeError:
        pass

print("Client connected. Press WASD to send. Press 'q' to quit.")
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
