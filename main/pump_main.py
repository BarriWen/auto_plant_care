import machine
from machine import Pin
import socket
import network
import time

# Wi-Fi credentials
SSID = 'hello'
PASSWORD = ''

# Server details
SERVER_IP = '10.42.0.1'  # Replace with the Raspberry Pi's IP address
PORT = 65432

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting to Wi-Fi...")
while not wifi.isconnected():
    time.sleep(1)
print(f"Connected to Wi-Fi. IP: {wifi.ifconfig()[0]}")

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print(f"Connected to server at {SERVER_IP}:{PORT}")

try:
    while True:
        haha = "pump"
        client_socket.sendall(haha.encode('utf-8'))
        time.sleep(5)
        print("1")
        # Receive pump instruction from the server
        data = client_socket.recv(1024).decode('utf-8')
        print("?")
        if data == "Low environmental humidity":
            # pump on
            relay_pin = Pin(18, Pin.OUT)
            time.sleep(2)
            # pump off
            relay_pin = Pin(18, Pin.IN)
            data = ""

except KeyboardInterrupt:
    print("Disconnecting...")
finally:
    client_socket.close()
