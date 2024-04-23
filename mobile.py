# main.py
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from jnius import autoclass
import socket

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')

# Bluetooth UUID for RFCOMM
uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")

# Bluetooth server address (your laptop's Bluetooth MAC address)
server_address = "XX:XX:XX:XX:XX:XX"  # Replace with your laptop's Bluetooth MAC address

class TouchpadApp(App):
    def build(self):
        layout = FloatLayout()
        self.label = Label(text="Drag your finger to move the cursor.")
        layout.add_widget(self.label)

        self.connect_button = Button(text="Connect to Server")
        self.connect_button.bind(on_press=self.connect_to_server)
        layout.add_widget(self.connect_button)

        return layout

    def connect_to_server(self, instance):
        try:
            adapter = BluetoothAdapter.getDefaultAdapter()
            device = adapter.getRemoteDevice(server_address)
            socket = device.createRfcommSocketToServiceRecord(uuid)
            socket.connect()

            # Start sending touchpad input
            # Here you would capture touch events and convert them to x, y coordinates
            # and send them to the server using socket.send()
            # For simplicity, we'll just send a sample message
            socket.send("10,20")

            self.label.text = "Connected to server. Start moving the cursor!"
        except Exception as e:
            self.label.text = f"Error: {e}"

if __name__ == "__main__":
    TouchpadApp().run()
