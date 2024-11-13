import machine, utime

class Light:
    def __init__(self, pin, sleep_time):
        self.sensor = machine.ADC(pin)
        self.wait = sleep_time
        self.read = 0
    
    def work(self):
        try:
            while True:
                self.read = self.sensor.read_u16()
                print("Light Sensor Value:", self.read)
                
                utime.sleep(self.wait)

        except KeyboardInterrupt:
            print("Light End")

    def get_read(self):
        return self.read
    
