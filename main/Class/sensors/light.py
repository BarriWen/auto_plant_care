import machine

class Light:
    def __init__(self, pin):
        self.sensor = machine.ADC(pin)
        self.read = 0
    
    def work(self):
        self.read = self.sensor.read_u16()
        print("Light Sensor Value:", self.read)

    def get_read(self):
        self.work()
        return self.read
    
