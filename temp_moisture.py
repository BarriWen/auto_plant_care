import machine
import time, utime
from machine import I2C, Pin

soil_humidity_adc = machine.ADC(26)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)

devices = i2c.scan()

if devices:
    print("I2C device(s) found:")
    for device in devices:
        print(f"Device at address: {hex(device)}")
else:
    print("No I2C devices found.")

def read_temp():
    i2c.writeto(0x38, b'\xF5')  # Send measurement command
    time.sleep(0.5)
    data = i2c.readfrom(0x38, 2)  # Read data
    temperature = data[0]
    return temperature

try:
    while True:
        raw_value = soil_humidity_adc.read_u16()
    
        humidity_percentage = (raw_value / 65535.0) * 100
        print(f"Soil Moisture: {humidity_percentage:.2f}%")
        
        temp = read_temp()
        print(f'Temperature: {temp} °C')
        
        utime.sleep(1)

except KeyboardInterrupt:
    print("End")
