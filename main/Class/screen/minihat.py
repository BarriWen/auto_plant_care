import time
from displayhatmini import DisplayHATMini
from PIL import Image, ImageDraw, ImageFont
import math
from datetime import datetime


class Minihat:
    def __init__(self):
        self.width = DisplayHATMini.WIDTH
        self.height = DisplayHATMini.HEIGHT
        self.buffer = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.buffer)
        self.displayhatmini = DisplayHATMini(self.buffer)
        self.displayhatmini.set_led(0.05, 0.05, 0.05)
        
        try:
            self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
        except IOError:
            self.font = ImageFont.load_default()

    def display_BUTTON_A(self, temperature, humidity, light_level, moisture_level):
        # Clear the screen with a dark background
        self.draw.rectangle([0, 0, self.width, self.height], fill=(10, 10, 10))

        padding = 10
        line_height = 30
        current_datetime = datetime.now()

        self.draw.text((self.width // 2 - 90, padding), "COSI-142A: Auto Plant Care", fill=(255, 255, 255), font=self.font)
        self.draw.text((10, padding + line_height), f"{current_datetime}", fill=(255, 255, 255), font=self.font)
        self.draw.text((10, padding + 2 * line_height), f"Last Time Watering:", fill=(255, 255, 255), font=self.font)
        self.draw.text((10, padding + 3 * line_height), f"Plant Type:", fill=(255, 255, 255), font=self.font)

        self.draw_gauge(center=(40, 180), radius=40, percentage=(temperature / 100.0), color=(255, 69, 0), label="Temp", value=f"{temperature:.1f}°C")
        self.draw_gauge(center=(120, 180), radius=40, percentage=(humidity / 100.0), color=(30, 144, 255), label="Humidity", value=f"{humidity:.1f}%")
        self.draw_gauge(center=(200, 180), radius=40, percentage=(light_level / 10.0), color=(255, 215, 0), label="Light", value=light_level)
        self.draw_gauge(center=(280, 180), radius=40, percentage=(moisture_level / 10.0), color=(34, 139, 34), label="Moisture", value=moisture_level)

        self.displayhatmini.display()

    def display_BUTTON_B(self):
        pass

    def display_BUTTON_X(self):
        pass

    def display_BUTTON_Y(self):
        pass

    def draw_gauge(self, center, radius, percentage, color, label, value):
        # Draw background circle
        self.draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], outline=(50, 50, 50), width=3)

        # Calculate the angle for the arc based on percentage
        angle = int(percentage * 360)

        # Draw the colored arc
        self.draw.arc([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius], start=-90, end=-90 + angle, fill=color, width=8)

        # Display label
        self.draw.text((center[0] - radius + 5, center[1] + radius - 20), label, fill=(255, 255, 255), font=self.font)

        # Display value
        self.draw.text((center[0] - 10, center[1] - 10), f"{value}", fill=(255, 255, 255), font=self.font)