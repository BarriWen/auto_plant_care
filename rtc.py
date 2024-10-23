from machine import RTC
import utime

# Initialize the RTC
rtc = RTC()

# Set the RTC to the current time if needed (year, month, day, weekday, hours, minutes, seconds, subseconds)
# rtc.datetime((2024, 10, 23, 2, 15, 30, 0, 0))

# Get the current time from the RTC
def get_current_time():
    current_time = rtc.datetime()
    # Format the datetime tuple into a readable string (year, month, day, hour, minute, second)
    formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
        current_time[0], current_time[1], current_time[2], 
        current_time[4], current_time[5], current_time[6]
    )
    return formatted_time

while True:
    print("Current time:", get_current_time())
    utime.sleep(1)  # Update every second
