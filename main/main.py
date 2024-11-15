from Class.screen.minihat import Minihat
from Class.sensors.light import Light
from Class.sensors.moisture import Moisture
from Class.sensors.temp import Temp
import time

sleep_time = 10

screen = Minihat()
light_sensor = Light(27)
moisture_sensor = Moisture(26)
temp_sensor = Temp(5, 4)

while True:
    
    temperature = temp_sensor.get_read()
    humidity = moisture_sensor.get_read()
    light_level = light_sensor.get_read()

    # Button controls (implement functionality as needed)
    if screen.displayhatmini.read_button(screen.displayhatmini.BUTTON_A):
        screen.display_BUTTON_A(temperature, humidity, light_level, moisture_level)
    elif screen.displayhatmini.read_button(screen.displayhatmini.BUTTON_B):
        pass
    elif screen.displayhatmini.read_button(screen.displayhatmini.BUTTON_X):
        pass
    elif screen.displayhatmini.read_button(screen.displayhatmini.BUTTON_Y):
        pass
    else:
        screen.display_BUTTON_A(temperature, humidity, light_level, moisture_level)

    time.sleep(sleep_time)