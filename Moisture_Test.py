import time
from machine import ADC, Pin

# Set up ADC for the moisture sensor (e.g., connected to ADC pin 28)
moisture_sensor = ADC(Pin(26))

try:
    while True:
        # Read the analog value from the sensor
        sensor_value = (moisture_sensor.read_u16() / 65535.0) * 100
        print(sensor_value)
        time.sleep(0.25)

except KeyboardInterrupt:
    # Exit the loop cleanly when interrupted
    print("Program stopped")
