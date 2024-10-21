import time
from machine import ADC, Pin

# Set up ADC for the moisture sensor (e.g., connected to ADC pin 28)
moisture_sensor = ADC(Pin(26))

try:
    while True:
        # Read the analog value from the sensor
        # sensor_data = round((1 - (moisture_sensor.read_u16() / 65535.0)) * 100, 2)
        sensor_data = moisture_sensor.read_u16()
        humidity_percent = round((1 - (sensor_data / 65535)) * 100, 2)
        print("Humidity: {}%".format(humidity_percent))
        time.sleep(0.25)

except KeyboardInterrupt:
    # Exit the loop cleanly when interrupted
    print("Program stopped")
