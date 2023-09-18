#sudo systemctl stop mini-screen.service

import time
import subprocess
import digitalio
import board
import random
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
import smbus
bus = smbus.SMBus(1)
addr = 0x20

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

bigFontSize = 38
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
bigFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", bigFontSize)
# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

colorOn = False #0 is black and white, 1 is color
colorR = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
colorG = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
colorB = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def qwiicjoystick():
    global bus_data, X, Y, joy_button
    global x_scaled, y_scaled
    global colorOn, colorR, colorG, colorB
    

    try:
        bus_data = bus.read_i2c_block_data(addr, 0x03, 5)
        #X_MSB = bus.read_byte_data(addr, 0x03) # Reads MSB for horizontal joystick position
        #X_LSB = bus.read_byte_data(addr, 0x04) # Reads LSB for horizontal joystick position
    
        #Y_MSB = bus.read_byte_data(addr, 0x05) # Reads MSB for vertical joystick position
        #Y_LSB = bus.read_byte_data(addr, 0x06) # Reads LSB for vertical joystick position

        #Select_Button = bus.read_byte_data(addr, 0x07) # Reads button position
    except Exception as e:
        print(e)

    X = (bus_data[0]<<8 | bus_data[1])>>6
    Y = (bus_data[2]<<8 | bus_data[3])>>6
    x_scaled = (X - 512)//4
    y_scaled = (Y - 512)//4
    joy_button = bus_data[4]
    # print(X, Y, " Button = ", bus_data[4])
    
    if(joy_button == 0):
        #set all RGB arrays to random values
        if colorOn:
            colorOn = False
        else:
            colorOn = True
            for i in range(15):
                colorR[i] = random.randint(0, 255)
                colorG[i] = random.randint(0, 255)
                colorB[i] = random.randint(0, 255)
        time.sleep(.5)

    time.sleep(.05)
    #if X < 450:
        #direction = RIGHT
    #elif 575 < X:
        #direction = LEFT

    
    #if Y< 450:
        #direction = DOWN
    #elif 575 < Y:
        #direction = UP

    #if Select_Button == 1:
        #terminate()


while True:
    # Draw a black filled box to clear the image.
    qwiicjoystick()
    draw.rectangle((0, 0, width, height), outline=0, fill=(0,0,0))
    # draw.text((x, top), strftime("%m/%d/%Y %H:%M:%S"), font=font, fill="#FFFFFF")
    # draw.text((x, top+20), "Hello World", font=font, fill="#FFFFFF")

    # Separate out the hour, minute, and second
    hour = int(strftime("%H"))
    # hour = hour + 1
    if(hour ==25):
        hour = 0
    
    minute = int(strftime("%M"))
    hour12Format = hour % 12
    isNight = hour >= 22 or hour <= 6
    #print hour and minute on different lines
    # draw.text((x, top+40), "Hour: "+str(hour), font=font, fill="#FFFFFF")
    # draw.text((x, top+60), "Minute: "+str(minute), font=font, fill="#FFFFFF")
    

    # ellipse multipliers
    if x_scaled > 0:
        x_left = x_scaled
        x_right = 0
    else:
        x_left = 0
        x_right = -x_scaled
    
    if y_scaled > 0:
        y_top = y_scaled
        y_bottom = 0
    else:
        y_top = 0
        y_bottom = -y_scaled

    if isNight:
        #if its night draw as many white outline concentric circles as 8 - hour12format
        hoursAtNight = 0
        hoursAtNight = hour12Format + 2
        print(hoursAtNight)
        for i in range(8 - hoursAtNight):
            if(colorOn):
                draw.ellipse((width/2 - i*2*7, bottom/2 - i*2*7, width/2 + i*2*7, bottom/2 + i*2*7), outline=(colorR[i], colorG[i], colorB[i]), width=6)
            else:
                draw.ellipse((width/2 - i*2*7, bottom/2 - i*2*7, width/2 + i*2*7, bottom/2 + i*2*7), outline="#FFFFFF", width=1)
        draw.text((width/2-75, bottom/2 - 30), "Not Now.", font=bigFont, fill="#FFFFFF")
    else:
       
        for i in range(22 - hour):
            if(colorOn):
                draw.ellipse((width/2 - i*2*9 - x_left, bottom/2 - i*2*9 -y_bottom, width/2 + i*2*9 + x_right, bottom/2 + i*2*9 + y_top), outline=(colorR[i], colorG[i], colorB[i]), width=6)
            else:
                draw.ellipse((width/2 - i*2*9 - x_left, bottom/2 - i*2*9 -y_bottom, width/2 + i*2*9 + x_right, bottom/2 + i*2*9 + y_top), outline="#FFFFFF", width=1)
        draw.text((width/2-36, bottom/2 - 30), "Now.", font=bigFont, fill="#FFFFFF")
    # for i in range(12):
    #     if isNight:
    #         draw.ellipse((width/2 - i*10, bottom/2 - i*10, width/2 + i*10, bottom/2 + i*10), outline=0, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    #     else:
    #         draw.ellipse((width/2 - i*10, bottom/2 - i*10, width/2 + i*10, bottom/2 + i*10), outline=0, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    
    
    # Display image.
    disp.image(image, rotation)
    time.sleep(0.02)
