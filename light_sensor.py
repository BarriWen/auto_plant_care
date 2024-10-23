import machine
import time

# Initialize the ADC pin where the light sensor is connected (GP26 = ADC0)
light_sensor = machine.ADC(27)  # ADC0 is on GP26

while True:
    # Read the raw value (between 0 and 65535) from the light sensor
    light_value = light_sensor.read_u16()

    # Convert the raw value to a voltage (3.3V max)
    voltage = light_value * 3.3 / 65535

    # Print out the sensor reading and voltage
    print("Light Sensor Value:", light_value)
    print("Voltage:", voltage)

    # Delay for a short time before the next reading
    time.sleep(1)
