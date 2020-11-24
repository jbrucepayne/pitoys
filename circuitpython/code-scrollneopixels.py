import board       # basic definitions
import digitalio
import time
import neopixel    # for neopixels

# my routines that are set up for ease of use and consistency
import local

# Color definitions
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

# Main variables needed for the color.  Can adjust each loop as needed
numPixels = 30
scrollMode = 1
scrollColor1 = RED

# Scroll modes are
# 0: Just light up the color and hold
# 1: Color chase
# 2: Rotate primary colors
# 3: Rainbow Cycle
# 4: Rainbow
# 5: Fade brightness of color in and out
# 6: Gentle classy twinkling - each light has a different brightness timer


# What are the pins available on this board?
x=dir(board)
print(x)

# Current pins in use
neoPixelPin=board.A2

lightSensor = analogio.AnalogIn(lightSensorPin)
onboardpixels = local.SetupOnboardNeopixels()
strandpixels = local.SetupNeopixelsStrand(neoPixelPin, numPixels)
 
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)
 
 
def color_chase(color, wait):
    for i in range(numPixels):
        strandpixels[i] = color
        time.sleep(wait)
        strandpixels.show()
    time.sleep(0.5)
 
 
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(numPixels):
            rc_index = (i * 256 // numPixels) + j * 5
            strandpixels[i] = wheel(rc_index & 255)
        strandpixels.show()
        time.sleep(wait)
 
 
def rainbow(wait):
    for j in range(255):
        for i in range(numPixels):
            idx = int(i + j)
            strandpixels[i] = wheel(idx & 255)
        strandpixels.show()
        time.sleep(wait)

def slowlight(wait):
    for j in range(100):
	    strandpixels = local.SetupNeopixelsStrand(neoPixelPin, numPixels, j / 100.0)
		for i in range(numPixels):
			strandpixels[i] = scrollColor1  # Use global color here.
		time.sleep(wait)
 
while True:
    if scrollMode == 0:
		scrollColor1 = RED
		slowlight(0.1)
		scrollColor1 = GREEN
		slowlight(0.1)

    if scrollMode == 1:
        color_chase(RED, 0.1)  # Increase the number to slow down the color chase
        color_chase(YELLOW, 0.1)
        color_chase(GREEN, 0.1)
        color_chase(CYAN, 0.1)
        color_chase(BLUE, 0.1)
        color_chase(PURPLE, 0.1)
        color_chase(OFF, 0.1)
 
    if scrollMode == 2:
        strandpixels.fill(RED)
        strandpixels.show()
        # Increase or decrease to change the speed of the solid color change.
        time.sleep(1)
        strandpixels.fill(GREEN)
        strandpixels.show()
        time.sleep(1)
        strandpixels.fill(BLUE)
        strandpixels.show()
        time.sleep(1)
        strandpixels.fill(WHITE)
        strandpixels.show()
        time.sleep(1)
 
    if scrollMode == 3:
        rainbow_cycle(0.05)  # Increase the number to slow down the rainbow.
 
    if scrollMode == 4:
        rainbow(0.05)  # Increase the number to slow down the rainbow.
		
	scrollMode++;
	