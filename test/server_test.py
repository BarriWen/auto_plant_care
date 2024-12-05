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

            # Parse the received data
            # Split into two parts: sensor type and value
            parts = data.split(" ", 1)
            if len(parts) == 2:
                sensor_type, value = parts
                try:
                    value = float(value)  # Convert the value to a float
                except ValueError:
                    conn.sendall(b"Invalid value\n")
                    continue

                # Respond based on the sensor type
                if sensor_type == "temp":
                    response = f"Temperature received: {value}°C"
                elif sensor_type == "light":
                    response = f"Light level received: {value} lux"
                elif sensor_type == "moisture":
                    response = f"Moisture level received: {value}%"
                else:
                    response = "Invalid sensor type"
            else:
                response = "Invalid command format. Expected format: <sensor_type> <value>"

            # Send the response back to the client
            conn.sendall(response.encode('utf-8'))
except KeyboardInterrupt:
    print("Shutting down server.")
finally:
    for client in clients:
        client.close()
    server_socket.close()
