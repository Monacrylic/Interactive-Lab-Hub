import time
import subprocess
import digitalio
import board
import random
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php

bigFontSize = 36
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
bigFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", bigFontSize)
# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


#temp
hour = 0
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0,0,0))
    # draw.text((x, top), strftime("%m/%d/%Y %H:%M:%S"), font=font, fill="#FFFFFF")
    # draw.text((x, top+20), "Hello World", font=font, fill="#FFFFFF")

    # Separate out the hour, minute, and second
    # hour = int(strftime("%H"))
    hour = hour + 1
    if(hour ==25):
        hour = 0
    
    minute = int(strftime("%M"))
    hour12Format = hour % 12
    isNight = hour >= 22 or hour <= 6
    #print hour and minute on different lines
    # draw.text((x, top+40), "Hour: "+str(hour), font=font, fill="#FFFFFF")
    # draw.text((x, top+60), "Minute: "+str(minute), font=font, fill="#FFFFFF")
    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 

    # Display 'Now' in the center of the screen in big white text.
    


    #if its night draw as many white outline concentric circles as 8 - hour12format
    if isNight:
        hoursAtNight = 0
        hoursAtNight = hour12Format + 2
        print(hoursAtNight)
        for i in range(8 - hoursAtNight):
            draw.ellipse((width/2 - i*2*10, bottom/2 - i*2*10, width/2 + i*2*10, bottom/2 + i*2*10), outline="#FFFFFF")
        draw.text((width/2-75, bottom/2 - 36), "Not Now.", font=bigFont, fill="#FFFFFF")
    else:

        for i in range(22 - hour):
            draw.ellipse((width/2 - i*2*10, bottom/2 - i*2*10, width/2 + i*2*10, bottom/2 + i*2*10), outline="#FFFFFF")
        draw.text((width/2-36, bottom/2 - 36), "Now.", font=bigFont, fill="#FFFFFF")
    # for i in range(12):
    #     if isNight:
    #         draw.ellipse((width/2 - i*10, bottom/2 - i*10, width/2 + i*10, bottom/2 + i*10), outline=0, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    #     else:
    #         draw.ellipse((width/2 - i*10, bottom/2 - i*10, width/2 + i*10, bottom/2 + i*10), outline=0, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    
    
    # Display image.
    disp.image(image, rotation)
    time.sleep(1)
