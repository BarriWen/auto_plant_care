import machine, utime
from machine import I2C, Pin
from lcd1602 import LCD1602
from dht20 import DHT20

class Temp:
    def __init__(self, scl, sda, sleep_time):
        i2c0 = I2C(0, scl=Pin(scl), sda=Pin(sda), freq=100000)
        temp_sensor = DHT20(0x38, i2c0)
        self.read = 0
        self.wait = sleep_time
    
    def work(self):
        try:
            while True:
                self.read = self.sensor.measurements['t']
                print(f'Temperature: {temp} °C')
                
                utime.sleep(self.wait)

        except KeyboardInterrupt:
            print("Temp End")

    def get_read(self):
        return self.read
