import socket
from connection import *

con = connection()
# Set up Bluetooth server socket
server_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server_socket.bind((con.bluetooth, 4))  # Bind to first available RFCOMM channel
server_socket.listen(1)

print("Bluetooth server started, waiting for connections...")

# Accept incoming Bluetooth connections
client_socket, client_info = server_socket.accept()
print(f"Bluetooth connection from {client_info}")

while True:
    try:
        # Receive touchpad input (x, y coordinates)
        data = client_socket.recv(1024).decode()
        if not data:
            break
        if data.strip().lower() == "exit":  # Check for termination command
            break  # Exit the loop if termination command is received
        x, y = map(int, data.split(','))

        # Move cursor using pyautogui or other cursor control mechanism
        # Replace this with your cursor control logic
        print(f"Received touchpad input: x={x}, y={y}")

    except KeyboardInterrupt:
        break

client_socket.close()
server_socket.close()