import board       # basic definitions
import digitalio
import time
import neopixel    # for neopixels
import random
import math

# my routines that are set up for ease of use and consistency
import local

# Color definitions
RED = local.gammaCorrectPixel((255, 0, 0))
YELLOW = local.gammaCorrectPixel((255, 255, 0))
GREEN = local.gammaCorrectPixel((0, 255, 0))
CYAN = local.gammaCorrectPixel((0, 255, 255))
BLUE = local.gammaCorrectPixel((0, 0, 255))
PURPLE = local.gammaCorrectPixel((180, 0, 255))
WHITE = local.gammaCorrectPixel((255, 255, 255))
ORANGE = local.gammaCorrectPixel((255, 165, 0))
INDIGO = local.gammaCorrectPixel((75, 0, 130))
BRONCOS_ORANGE = local.gammaCorrectPixel((251, 79, 20))
BRONCOS_BLUE = local.gammaCorrectPixel((0, 20, 137))

VIOLET = PURPLE
BLACK = (0, 0, 0)
OFF = (0, 0, 0)

# Main variables needed for the color.  Can adjust each loop as needed
numPixels = 30
scrollMode = 6
maxScrollMode = 8
colorCycleList = (RED, GREEN, BLUE, WHITE, PURPLE, YELLOW, ORANGE)
rainbow_colors = (RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET)
broncos_colors = (BRONCOS_ORANGE, BRONCOS_BLUE, WHITE, BLACK)

# Scroll modes
# 0: Slowly brighten color and then stop
# 1: Color chase
# 2: Rotate primary colors
# 3: Rainbow Cycle
# 4: Rainbow
# 5: Gentle classy twinkling - each light has a different brightness timer
# 6: Rainbow walks down the wire
# 7: Gentle classy rainbow twinkling - each light has a different brightness timer
#99: Fully random

# What are the pins available on this board?
x=dir(board)
print(x)

# Current pins in use
neoPixelPin=board.A2

# set up NeoPixels arrays.
onboardpixels = local.SetupOnboardNeopixels()
strandpixels = local.SetupNeopixelsStrand(neoPixelPin, numPixels)

# Fill up the pixel colors array, then call into the display_pixel_array routine to show
# It is assumed here that the strand has more pixels that the onboard display.
# Otherwise this probably won't work
pixelColors = []
for i in range(numPixels):
    pixelColors.append(strandpixels[i])

# Takes the colors present in pixelColors and displays them to strand and onboard.
# TODO: Add ability to toggle onboard display on and off.
def display_pixel_array():
    pixelRatio = len(strandpixels) // len (onboardpixels)
    for i in range(numPixels):
        strandpixels[i] = pixelColors[i]
        if (i < len(onboardpixels)):
            # if strip and neopixel in opposite direction
            onboardpixels[i] = pixelColors[len(strandpixels) - i * pixelRatio - 1]
            # if strip and onboard in same direction
            #onboardpixels[i] = pixelColors[i * pixelRatio]
    strandpixels.show()
    onboardpixels.show()

# Mode 0
def neopixelstrip_slowlight(color, wait):
    for j in range(100):
        for i in range(numPixels):
            pixelColors[i] = (color[0] * j // 100, color[1] *j // 100, color[2] * j // 100)
        display_pixel_array()
        time.sleep(wait)
    for j in range(100):
        for i in range(numPixels):
            pixelColors[i] = (color[0] * (100-j) // 100, color[1] * (100-j) // 100, color[2] * (100-j) // 100)
        display_pixel_array()
        time.sleep(wait)

# Mode 1
def neopixelstrip_color_chase(color, wait):
    for i in range(numPixels):
        pixelColors[i] = color
        display_pixel_array()
        time.sleep(wait)

# Mode 2
def neopixelstrip_solid_color(color, wait):
    for i in range(numPixels):
        pixelColors[i] = color
    display_pixel_array()
    time.sleep(wait)

# Mode 3
def neopixelstrip_rainbow_cycle(wait):
    for j in range(255):
        for i in range(numPixels):
            rc_index = (i * 255 // numPixels) + j * 5
            pixelColors[i] = local.color_wheel(rc_index & 255)
        display_pixel_array()
        time.sleep(wait)

# Mode 4
def neopixelstrip_rainbow(wait):
    for j in range(255):
        for i in range(numPixels):
            idx = int(i + j)
            pixelColors[i] = local.color_wheel(idx & 255)
        display_pixel_array()
        time.sleep(wait)

# Mode 5
def neopixelstrip_gentleclassytwinkling(color, wait):
    # First set up the pixels in a random phase
    phase = []
    speed = []
    for i in range(numPixels):
        phase.append(random.randrange(628) / 100) # 0-6.28 radians, an entire circle
        speed.append(random.randrange(40) / 100) # radians per clock cycle

    # Loop over the brightening 1000 times.
    for j in range(200):
        for i in range(numPixels):
            phase[i] = phase[i] + speed[i]
            phaseValue = abs(math.sin(phase[i]))
            pixelColors[i] = local.gammaCorrectPixel((int(color[0] * phaseValue), int(color[1] * phaseValue), int(color[2] * phaseValue)))
            display_pixel_array()
        time.sleep(wait)


# Mode 6
def neopixelstrip_walkpattern(colorArray, totalTimeSeconds, wait):
    arrayPos = 0
    for j in range(totalTimeSeconds // wait):
        for i in range(numPixels):
            pixelColors[i] = colorArray[(i+arrayPos)%len(colorArray)]
        arrayPos = arrayPos + 1
        display_pixel_array()
        time.sleep(wait)

# Mode 7
def neopixelstrip_gentleclassyrainbowtwinkling(wait):
    # First set up the pixels in a random phase
    phase = []
    speed = []
    colors = []
    for i in range(numPixels):
        phase.append(random.randrange(628) / 100)
        speed.append(random.randrange(40) / 100) # radians per clock cycle
        colors.append(rainbow_colors[i%len(rainbow_colors)])

    # Loop over the brightening 1000 times.
    for j in range(200):
        for i in range(numPixels):
            phase[i] = phase[i] + speed[i]
            phaseValue = abs(math.sin(phase[i]))
            color = colors[i]
            pixelColors[i] = local.gammaCorrectPixel((int(color[0] * phaseValue), int(color[1] * phaseValue), int(color[2] * phaseValue)))
            display_pixel_array()
        time.sleep(wait)

# Mode 99: Not in the regular usage
def neopixelstrip_random(totalTimeSeconds, wait):
    for j in range(totalTimeSeconds // wait):
        for i in range(numPixels):
            pixelColors[i] = local.gammaCorrectPixel(local.color_random())
        display_pixel_array()
        time.sleep(wait)

startTime = time.monotonic()
while True:
    print("Beginning scroll mode: ", scrollMode, " at time:" + str(time.monotonic() - startTime))

    # 0: slowly light and unlight each color
    if scrollMode == 0:
        for color in colorCycleList:
            neopixelstrip_slowlight(color, 0.06)

    # 1: Color chase where the colors blend down the strip
    if scrollMode == 1:
        for color in colorCycleList:
            neopixelstrip_color_chase(color, 0.06)

    # 2: Fill with solid color
    if scrollMode == 2:
        for color in colorCycleList:
            neopixelstrip_solid_color(color, 5)

    # 3:
    if scrollMode == 3:
        neopixelstrip_rainbow_cycle(0.1)  # Increase the number to slow down the rainbow.

    # 4:
    if scrollMode == 4:
        neopixelstrip_rainbow(0.2)  # Increase the number to slow down the rainbow.

    # 5: Gentle classy twinkling - each light has a different brightness timer
    if scrollMode == 5:
        for color in colorCycleList:
            neopixelstrip_gentleclassytwinkling(color, 0.04)

    # 6: Rainbow walks down the wire
    if scrollMode == 6:
        neopixelstrip_walkpattern(rainbow_colors, 60, 0.1)

    # 5: Gentle classy twinkling - each light has a different brightness timer
    if scrollMode == 7:
        neopixelstrip_gentleclassyrainbowtwinkling(0.05)

    #99: Fully random
    if scrollMode == 99:
        neopixelstrip_random(60, .25)

    scrollMode = (scrollMode+1) % maxScrollMode;