import machine

class Moisture:
    def __init__(self, pin):
        self.sensor = machine.ADC(pin)
        self.read = 0
    
    def work(self):
        sensor_data = self.sensor.read_u16()
        self.read = round((1 - (sensor_data / 65535)) * 100, 2)
        print(f"Soil Moisture: {self.read:.2f}%")

    def get_read(self):
        self.work()
        return self.read
