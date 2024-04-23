import socket
import tkinter as tk
from threading import Thread
from connection import *

class TouchpadServer:
    con = connection()
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Touchpad Server")

        self.label = tk.Label(self.root, text="Touchpad Server Running")
        self.label.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.close_server)
        self.exit_button.pack()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.con.bluetooth, 4))
        self.server_socket.listen(1)

        self.client_socket = None
        self.client_info = None

        self.listen_thread = Thread(target=self.listen_for_connections)
        self.listen_thread.daemon = True  # Daemonize the thread to stop when the main thread stops

    def start(self):
        self.listen_thread.start()
        self.root.mainloop()

    def listen_for_connections(self):
        print("Bluetooth server started, waiting for connections...")
        self.client_socket, self.client_info = self.server_socket.accept()
        print(f"Bluetooth connection from {self.client_info}")

        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                if data.strip().lower() == "exit":
                    self.close_server()
                    break
                x, y = map(int, data.split(','))
                print(f"Received touchpad input: x={x}, y={y}")

            except Exception as e:
                print(f"Error: {e}")
                break

    def close_server(self):
        if self.client_socket:
            self.client_socket.close()
        self.server_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    touchpad_server = TouchpadServer()
    touchpad_server.start()
