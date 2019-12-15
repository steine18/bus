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

def display(rsb, arrival, departure):
	time = datetime.now()
	ctime = datetime.strftime(time, '%H:%M')
	tformat = '%Y-%m-%d %H:%M:%S'
	arrive = (datetime.strptime(arrival, tformat) - time).seconds//60
	depart = (datetime.strptime(departure, tformat) - time).seconds//60
	# Draw a black filled box to clear the image.
	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	# Write four lines of text.
	offset = 8
	w,h = draw.textsize(ctime)
	draw.text(((width-w)/2, top+ offset), datetime.strftime(time, '%H:%M'), font=font, fill=255)
	offset +=8
	draw.text((x, top + offset), f'{rsb}', font=font, fill=255)
	offset += 8
	draw.text((x, top + offset), f'Arives in {arrive} minutes', font=font, fill=255)
	offset += 8
	draw.text((x, top + offset), f'Departs in {depart} minutes', font=font, fill=255)
	offset += 8
	# Display image.
	disp.image(image)
	disp.show()