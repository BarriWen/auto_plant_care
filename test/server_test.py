import socket

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 65432      # Port to listen on

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
            # Receive data from the client
            data = conn.recv(1024).decode('utf-8')
            if not data:
                print(f"Client {addr} disconnected")
                clients.remove(conn)
                conn.close()
                break

            print(f"Received: {data} from {addr}")

            # Respond based on the received command
            if data == "temp":
                response = "25.6"  # Simulated temperature
            elif data == "light":
                response = "350"  # Simulated light level
            elif data == "moisture":
                response = "60.5"  # Simulated moisture level
            else:
                response = "Invalid command"

            # Send the response back to the client
            conn.sendall(response.encode('utf-8'))
except KeyboardInterrupt:
    print("Shutting down server.")
finally:
    for client in clients:
        client.close()
    server_socket.close()
