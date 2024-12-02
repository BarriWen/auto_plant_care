import network
import socket
import binascii
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from lcd1602 import LCD1602
from machine import I2C, Pin

ssid = 'hhhh'
password = ''


def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print(wlan.status())

    while wlan.isconnected() == False:
        print('Waiting for connection...', wlan.status())
        sleep(3)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


def webpage(temperature, state):
    # Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            
            <!-- Textbox form with submit and clear buttons -->
            <form action="./submittext" method="get">
                <label for="textbox">Enter text:</label>
                <input type="text" id="textbox" name="textbox" value="" />
                <input type="submit" value="Submit" />
                <input type="reset" value="Clear Textbox" />
            </form>
            
            <form action="./clear">
                <input type="submit" value="Clear LCD" />
            </form>
            
            </body>
            </html>
            """
    return str(html)


def serve(connection):
    # Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
    d = LCD1602(i2c, 2, 16)
    d.display()
    sleep(1)
    d.clear()
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            state = 'ON'
            pico_led.on()
        elif request == '/lightoff?':
            pico_led.off()
            state = 'OFF'

        elif request.startswith('/submittext?textbox='):
            # Extract the text from the request
            text = request.split('=')[1].replace(
                '%20', ' ')  # Replace URL-encoded spaces
            print(f"Received text: {text}")
            # Limit text length to 16 characters for the LCD
            text1 = text[:16]
            text2 = text[16:]
            d.clear()
            d.print(text1)
            sleep(1)
            d.setCursor(0, 1)
            d.print(text2)
        elif request == '/clear?':
            d.clear()

        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()


try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
