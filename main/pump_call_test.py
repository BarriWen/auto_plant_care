from Class.screen.minihat import Minihat
from Class.camera import camera
import socket

screen = Minihat()
plant_classifier = camera.PlantClassifier()

HOST = '0.0.0.0'
PORT = 65432
# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Allow up to 5 connections
print(f"Server listening on {HOST}:{PORT}")
clients = []


try:
    while True:
        conn, addr = server_socket.accept()  # Accept a new client
        print(f"Connected by {addr}")
        clients.append(conn)

        while True:
            hmdmsg = 'Low environmental humidity'
            conn.sendall(hmdmsg.encode('utf-8'))

except KeyboardInterrupt:
    print("Shutting down server.")
finally:
    for client in clients:
        client.close()
    server_socket.close()
