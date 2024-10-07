# import libraries
import time
import RPi.GPIO as GPIO

# GPIO setup -- pin 29 as moisture sensor input
# Sensor: GPIO 29, Relay 1: GPIO 37, Relay 2: GPIO 38
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.IN)
GPIO.setup(37, GPIO.OUT)

try:
    while True:
        if (GPIO.input(29)) == 0:
            print('Wet')
            GPIO.output(37, True)
        elif (GPIO.input(29)) == 1:
            print('Dry')
            GPIO.output(37, False)
        time.sleep(.25)

finally:
    # cleanup the GPIO pins before ending
    GPIO.cleanup()
