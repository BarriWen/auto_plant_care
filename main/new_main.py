from Class.screen.minihat import Minihat
from Class.camera import camera
import socket
import threading

screen = Minihat()
plant_classifier = camera.PlantClassifier()

HOST = '0.0.0.0'
PORT = 65432

# Global variables
temperature = 0
humidity = 0
light_level = 0

# Plant type
# results = plant_classifier.detect_and_classify()
results = "golden"
if results:
    print("Detections:", results)

# Client handler


def handle_client(conn, addr):
    global temperature, humidity, light_level, plant_type
    print(f"Connected by {addr}")
    try:
        while True:
            # Receive data from the client
            data = conn.recv(1024).decode('utf-8')
            if not data:
                print(f"Client {addr} disconnected")
                break

            print(f"Received: {data} from {addr}")

            # Parse the received data
            parts = data.split(" ", 1)
            if len(parts) == 2:
                sensor_type, value = parts
                try:
                    value = float(value)  # Convert the value to a float
                except ValueError:
                    conn.sendall(b"Invalid value\n")
                    continue

                # Get the plant type
                plant_type = results

                # Respond based on the sensor type
                if sensor_type == "temp":
                    temperature = value
                    response = f"Temperature received: {value}°C"
                elif sensor_type == "light":
                    light_level = value
                    response = f"Light level received: {value} lux"
                elif sensor_type == "moisture":
                    humidity = value
                    response = f"Moisture level received: {value}%"
                elif sensor_type == "pump":
                    response = "pump received"
                else:
                    response = "Invalid sensor type"
            else:
                response = "Invalid command format. Expected format: <sensor_type> <value>"

            # Plant care logic
            tmpmsg = "No warnings"
            hmdmsg = "No warnings"
            ligmsg = "No warnings"

            if plant_type == "golden":
                if temperature < 15:
                    tmpmsg = 'Environment temperature too low'
                if temperature > 29:
                    tmpmsg = 'Environment temperature too high'
                if humidity < 50:
                    hmdmsg = 'Low environmental humidity'
                    print("low water")
                    conn.sendall(hmdmsg.encode('utf-8'))
                if humidity > 60:
                    hmdmsg = 'High environmental humidity'
                if light_level < 5000:
                    ligmsg = 'Excessive environmental light'
                if light_level > 15000:
                    ligmsg = 'Low environmental light'

            if plant_type == "ribbon":
                if temperature < 21:
                    tmpmsg = 'Environment temperature too low'
                if temperature > 29:
                    tmpmsg = 'Environment temperature too high'
                if humidity < 40:
                    hmdmsg = 'Low environmental humidity'
                    print("low water")
                    conn.sendall(hmdmsg.encode('utf-8'))
                if humidity > 60:
                    hmdmsg = 'High environmental humidity'
                if light_level < 10000:
                    ligmsg = 'Excessive environmental light'
                if light_level > 20000:
                    ligmsg = 'Low environmental light'

            # Send response back to the client
            conn.sendall(response.encode('utf-8'))

            # Button controls
            if screen.displayhatmini.read_button(screen.displayhatmini.BUTTON_A):
                screen.display_BUTTON_A(temperature, humidity, light_level, 1)
            elif screen.displayhatmini.read_button(screen.displayhatmini.BUTTON_B):
                screen.display_BUTTON_B(tmpmsg, hmdmsg, ligmsg)
            else:
                screen.display_BUTTON_A(temperature, humidity, light_level, 1)
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()

# Main server


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(conn, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down server.")
        server_socket.close()
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
