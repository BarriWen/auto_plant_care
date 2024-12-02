import socket
import network
import time

# Wi-Fi credentials
SSID = 'YourSSID'
PASSWORD = 'YourPassword'

# Server details
SERVER_IP = '192.168.x.x'  # Replace with the Raspberry Pi's IP address
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
        # Send a command to the server
        client_socket.sendall(b"temp")
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {data}")

        time.sleep(5)  # Send the next command after a delay
except KeyboardInterrupt:
    print("Disconnecting...")
finally:
    client_socket.close()
