import machine
import time, utime
from machine import I2C, Pin
from lcd1602 import LCD1602
from dht20 import DHT20

# set up the LCD screen
i2c = I2C(1,scl=Pin(7), sda=Pin(6), freq=400000)
d = LCD1602(i2c, 2, 16)
d.display()
# sensors
moisture_sensor = machine.ADC(26)
i2c0 = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
temp_sensor = DHT20(0x38, i2c0)
light_sensor = machine.ADC(27)

try:
    while True:
        # initialize the screen
        d.clear()
        
        # measure the moisture
        sensor_data = moisture_sensor.read_u16()
        humidity_percent = round((1 - (sensor_data / 65535)) * 100, 2)
        print(f"Soil Moisture: {humidity_percent:.2f}%")
        # measure the temp
        temp = temp_sensor.measurements['t']
        print(f'Temperature: {temp} °C')
        # measure the light
        light_value = light_sensor.read_u16()
        print("Light Sensor Value:", light_value)
        
        # output the sensor reads to the screen 
        d.print(f'Moisture: {humidity_percent:.2f}%')
        d.setCursor(0, 1)
        d.print(f'Temp: {temp:.2f} *C')
        utime.sleep(3)
        d.clear()
        d.setCursor(0, 0)
        d.print(f'Light:{light_value}')
        
        # wait for some time
        utime.sleep(5)

except KeyboardInterrupt:
    print("End")
