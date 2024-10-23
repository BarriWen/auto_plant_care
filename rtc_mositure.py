import time
from machine import ADC, Pin, RTC
import utime

# Set up ADC for the moisture sensor (e.g., connected to ADC pin 28)
moisture_sensor = ADC(Pin(26))

# Initialize the RTC
rtc = RTC()

# Optionally set the RTC to the current time if needed
# rtc.datetime((2024, 10, 23, 2, 12, 0, 0, 0))  # (year, month, day, weekday, hour, minute, second, subseconds)

# Function to get formatted current time
def get_current_time():
    current_time = rtc.datetime()
    return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
        current_time[0], current_time[1], current_time[2],
        current_time[4], current_time[5], current_time[6]
    )

# Function to log moisture data
def log_moisture_data():
    sensor_data = moisture_sensor.read_u16()
    humidity_percent = round((1 - (sensor_data / 65535)) * 100, 2)
    current_time = get_current_time()
    print("Time: {}, Humidity: {}%".format(current_time, humidity_percent))

# Main loop
last_logged_time = utime.time()

try:
    while True:
        # Get the current time in seconds
        current_time_sec = utime.time()

        # Log data every hour (3600 seconds), 10 seconds for test
        if current_time_sec - last_logged_time >= 10:
            log_moisture_data()
            last_logged_time = current_time_sec  # Update the last logged time

        time.sleep(0.25)

except KeyboardInterrupt:
    print("Program stopped")
