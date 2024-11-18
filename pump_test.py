from machine import Pin
import utime

def pump_on():
    relay_pin = Pin(18, Pin.OUT)

# Function to turn off the pump
def pump_off():
    relay_pin = Pin(18, Pin.IN)

# Schedule times (example: 10 seconds on, 5 seconds off)
def run_schedule():
    pump_on()
    utime.sleep(5)  # Pump on for 5 seconds
    pump_off()
    utime.sleep(5)   # Pump off for 5 seconds
    
# Run the schedule continuously
while True:
    run_schedule()


