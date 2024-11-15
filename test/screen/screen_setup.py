import time
from displayhatmini import DisplayHATMini
from PIL import Image, ImageDraw, ImageFont
import math
from datetime import datetime

# Initialize the display
width = DisplayHATMini.WIDTH
height = DisplayHATMini.HEIGHT
buffer = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(buffer)

displayhatmini = DisplayHATMini(buffer)
displayhatmini.set_led(0.05, 0.05, 0.05)

# Default values for sensor data
DEFAULT_TEMP = 25.0
DEFAULT_HUMIDITY = 50.0
DEFAULT_LIGHT_LEVEL = 5
DEFAULT_MOISTURE_LEVEL = 5

# Display the label and value in the center
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
except IOError:
    font = ImageFont.load_default()


# Helper function to draw a circular gauge
def draw_gauge(center, radius, percentage, color, label, value):
    # Draw background circle
    draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline=(50, 50, 50), width=3)

    # Calculate the angle for the arc based on percentage
    angle = int(percentage * 360)

    # Draw the colored arc
    draw.arc([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], start=-90, end=-90 + angle, fill=color, width=8)

    # Display label
    draw.text((center[0] - radius + 5, center[1] + radius - 20), label, fill=(255, 255, 255), font=font)

    # Display value
    draw.text((center[0] - 10, center[1] - 10), f"{value}", fill=(255, 255, 255), font=font)


def display_BUTTON_A(temperature, humidity, light_level, moisture_level):
    # Clear the screen with a dark background
    draw.rectangle([0, 0, width, height], fill=(10, 10, 10))

    padding = 10
    line_height = 30
    current_datetime = datetime.now()

    draw.text((width // 2 - 90, padding), "COSI-142A: Auto Plant Care", fill=(255, 255, 255), font=font)
    draw.text((10, padding + line_height), f"{current_datetime}", fill=(255, 255, 255), font=font)
    draw.text((10, padding + 2 * line_height), f"Last Time Watering:", fill=(255, 255, 255), font=font)
    draw.text((10, padding + 3 * line_height), f"Plant Type:", fill=(255, 255, 255), font=font)

    draw_gauge(center=(40, 180), radius=40, percentage=(temperature / 100.0), color=(255, 69, 0), label="Temp", value=f"{temperature:.1f}°C")
    draw_gauge(center=(120, 180), radius=40, percentage=(humidity / 100.0), color=(30, 144, 255), label="Humidity", value=f"{humidity:.1f}%")
    draw_gauge(center=(200, 180), radius=40, percentage=(light_level / 10.0), color=(255, 215, 0), label="Light", value=light_level)
    draw_gauge(center=(280, 180), radius=40, percentage=(moisture_level / 10.0), color=(34, 139, 34), label="Moisture", value=moisture_level)

    displayhatmini.display()





while True:
    # Simulated sensor readings (replace with actual sensor data retrieval)
    temperature = DEFAULT_TEMP
    humidity = DEFAULT_HUMIDITY
    light_level = DEFAULT_LIGHT_LEVEL
    moisture_level = DEFAULT_MOISTURE_LEVEL

    # Display the readings on the screen
    display_BUTTON_A(temperature, humidity, light_level, moisture_level)

    # Button controls (implement functionality as needed)
    if displayhatmini.read_button(displayhatmini.BUTTON_A):
        pass
    if displayhatmini.read_button(displayhatmini.BUTTON_B):
        pass
    if displayhatmini.read_button(displayhatmini.BUTTON_X):
        pass
    if displayhatmini.read_button(displayhatmini.BUTTON_Y):
        pass
      

    time.sleep(1)