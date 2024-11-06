import time
from displayhatmini import DisplayHATMini
from PIL import Image, ImageDraw, ImageFont
from collections import namedtuple

# Initialize the display
width = DisplayHATMini.WIDTH
height = DisplayHATMini.HEIGHT
buffer = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(buffer)

displayhatmini = DisplayHATMini(buffer)
displayhatmini.set_led(0.05, 0.05, 0.05)

Position = namedtuple('Position', 'x y')
Size = namedtuple('Size', 'w h')


DEFAULT_TEMP = 1.0
DEFAULT_HUMIDITY = 1.0
DEFAULT_LIGHT_LEVEL = 1
DEFAULT_MOISTURE_LEVEL = 1


def display_sensor_values(temperature, humidity, light_level, moisture_level):
    # Clear the screen with a background color (dark gray)
    draw.rectangle([0, 0, width, height], fill=(20, 20, 20))

    # Font settings
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)  # Larger bold font
    except IOError:
        font = ImageFont.load_default()

    # Add padding between each line of text
    padding = 10
    line_height = 30  # Adjust the space between lines
   
    draw.text((width // 2 - 70, padding), "Sensor Readings", fill=(255, 255, 255), font=font)
    draw.text((10, padding + line_height), f"Temp: {temperature:.1f}°C", fill=(255, 255, 255), font=font)
    draw.text((10, padding + 2 * line_height), f"Humidity: {humidity:.1f}%", fill=(255, 255, 255), font=font)
    draw.text((10, padding + 3 * line_height), f"Light: {light_level}", fill=(255, 255, 255), font=font)
    draw.text((10, padding + 4 * line_height), f"Soil Moisture: {moisture_level}", fill=(255, 255, 255), font=font)
    draw.line([(0, height - 1), (width, height - 1)], fill=(255, 255, 255), width=2)

    displayhatmini.display()


while True:
    temperature = DEFAULT_TEMP
    humidity = DEFAULT_HUMIDITY
    light_level = DEFAULT_LIGHT_LEVEL
    moisture_level = DEFAULT_MOISTURE_LEVEL

    # Display the readings on the screen by default
    display_sensor_values(temperature, humidity, light_level, moisture_level)

    if displayhatmini.read_button(displayhatmini.BUTTON_A):
        pass
    if displayhatmini.read_button(displayhatmini.BUTTON_B):
        pass
    if displayhatmini.read_button(displayhatmini.BUTTON_X):
        pass
    if displayhatmini.read_button(displayhatmini.BUTTON_Y):
        pass


    time.sleep(1)
