import machine
import utime
from machine import I2C, Pin
from lcd1602 import LCD1602
from dht20 import DHT20
import socket
import network
import time

# Wi-Fi credentials
SSID = 'hhhh'
PASSWORD = ''

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

# sensors
moisture_sensor = machine.ADC(26)
i2c0 = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
temp_sensor = DHT20(0x38, i2c0)
light_sensor = machine.ADC(27)

try:
    while True:
        temp_value = temp_sensor.measurements['t']
        light_value = light_sensor.read_u16()
        moisture_read = moisture_sensor.read_u16()
        moisture_value = round((1 - (moisture_read / 65535)) * 100, 2)
        
        # Send temp to the server
        client_socket.sendall(b"temp " + str(temp_value).encode('utf-8'))
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {data}")
        
        # Send light to the server
        client_socket.sendall(b"light " + str(light_value).encode('utf-8'))
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {data}")
        
        # Send moisture to the server
        client_socket.sendall(b"moisture " + str(moisture_value).encode('utf-8'))
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {data}")

        time.sleep(5)  # Send the next command after a delay
except KeyboardInterrupt:
    print("Disconnecting...")
finally:
    client_socket.close()