import machine
import time, utime
from machine import I2C, Pin
from dht20 import DHT20

moisture_sensor = machine.ADC(26)
i2c0 = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
temp_sensor = DHT20(0x38, i2c0)

try:
    while True:
        # measure moisture
        sensor_data = moisture_sensor.read_u16()
        humidity_percent = round((1 - (sensor_data / 65535)) * 100, 2)
        print(f"Soil Moisture: {humidity_percent:.2f}%")
        # measure temp
        temp = temp_sensor.measurements['t']
        print(f'Temperature: {temp} °C')
        
        utime.sleep(1)

except KeyboardInterrupt:
    print("End")
