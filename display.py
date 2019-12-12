import time
import subprocess
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

i2c = busio.I2C(SCL, SDA)

disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

disp.fill(0)
disp.show()
 
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
 
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
 
 
# Load default font.
font = ImageFont.load_default()

def display(stop_info):
# Draw a black filled box to clear the image.
	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	# Write four lines of text.
	offset = 0
	for stop in stop_info.keys():
		draw.text((x, top + offset), f'{stop}', font=font, fill=255)
		offset += 8
		draw.text((x, top + offset), f'{stop_info[stop][1]}', font=font, fill=255)
		offset += 8
	# Display image.
	disp.image(image)
	disp.show()