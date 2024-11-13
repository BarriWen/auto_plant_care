import machine, utime

class Moisture:
    def __init__(self, pin, sleep_time):
        self.sensor = machine.ADC(pin)
        self.wait = sleep_time
        self.read = 0
    
    def work(self):
        try:
            while True:
                sensor_data = self.sensor.read_u16()
                self.read = round((1 - (sensor_data / 65535)) * 100, 2)
                print(f"Soil Moisture: {self.read:.2f}%")
                
                utime.sleep(self.wait)

        except KeyboardInterrupt:
            print("Moisture End")

    def get_read(self):
        return self.read
