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
VIOLET = PURPLE
OFF = (0, 0, 0)

# Main variables needed for the color.  Can adjust each loop as needed
numPixels = 30
scrollMode = 7
maxScrollMode = 8
colorCycleList = (RED, GREEN, WHITE, PURPLE, YELLOW, BLUE, ORANGE)
rainbow_colors = (RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET)

# Each scroll mode should run for about a minute.  That way we can balamce them out.
# Scroll modes are
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

onboardpixels = local.SetupOnboardNeopixels()
strandpixels = local.SetupNeopixelsStrand(neoPixelPin, numPixels)

def neopixelstrip_color_chase(color, wait):
    for i in range(numPixels):
        strandpixels[i] = color
        if (i < len(onboardpixels)):
            onboardpixels[i] = color
        strandpixels.show()
        onboardpixels.show()
        time.sleep(wait)

def neopixelstrip_rainbow_cycle(wait):
    for j in range(255):
        for i in range(numPixels):
            rc_index = (i * 255 // numPixels) + j * 5
            strandpixels[i] = local.color_wheel(rc_index & 255)
            if (i < len(onboardpixels)):
                onboardpixels[i] = local.color_wheel(rc_index & 255)
        strandpixels.show()
        onboardpixels.show()
        time.sleep(wait)

def neopixelstrip_rainbow(wait):
    for j in range(255):
        for i in range(numPixels):
            idx = int(i + j)
            strandpixels[i] = local.color_wheel(idx & 255)
            if (i < len(onboardpixels)):
                onboardpixels[i] = local.color_wheel(idx & 255)
        strandpixels.show()
        onboardpixels.show()
        time.sleep(wait)

def neopixelstrip_slowlight(color, wait):
    for j in range(100):
        for i in range(numPixels):
            strandpixels[i] = (color[0] *j // 100, color[1] *j // 100, color[2] * j // 100)
            if (i < len(onboardpixels)):
                onboardpixels[i] = (color[0] *j // 100, color[1] *j // 100, color[2] * j // 100)
            strandpixels.show()
            onboardpixels.show()
        time.sleep(wait)

def neopixelstrip_gentleclassytwinkling(color, wait):
    # First set up the pixels in a random phase
    phase = []
    speed = []
    for i in range(numPixels):
        phase.append(random.randrange(628) / 100)
        speed.append(random.randrange(40) / 100) # radians per clock cycle

    # Loop over the brightening 1000 times.
    for j in range(200):
        for i in range(numPixels):
            phase[i] = phase[i] + speed[i]
            phaseValue = abs(math.sin(phase[i]))
            strandpixels[i] = local.gammaCorrectPixel((int(color[0] * phaseValue), int(color[1] * phaseValue), int(color[2] * phaseValue)))
            if (i < len(onboardpixels)):
                onboardpixels[i] = local.gammaCorrectPixel((int(color[0] * phaseValue), int(color[1] * phaseValue), int(color[2] * phaseValue)))
            onboardpixels.show();
            strandpixels.show()
        time.sleep(wait)

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
            strandpixels[i] = local.gammaCorrectPixel((int(color[0] * phaseValue), int(color[1] * phaseValue), int(color[2] * phaseValue)))
            if (i < len(onboardpixels)):
                onboardpixels[i] = local.gammaCorrectPixel((int(color[0] * phaseValue), int(color[1] * phaseValue), int(color[2] * phaseValue)))
            onboardpixels.show();
            strandpixels.show()
        time.sleep(wait)

def neopixelstrip_rainbowwalks(totalTimeSeconds, wait):
    rainbowpos = 0
    for j in range(totalTimeSeconds // wait):
        for i in range(numPixels):
            strandpixels[i] = rainbow_colors[(i+rainbowpos)%len(rainbow_colors)]
            if (i < len(onboardpixels)):
                onboardpixels[i] = rainbow_colors[(i+rainbowpos)%len(rainbow_colors)]
        strandpixels.show()
        onboardpixels.show()
        rainbowpos = rainbowpos + 1
        time.sleep(wait)

def neopixelstrip_random(totalTimeSeconds, wait):
    for j in range(totalTimeSeconds // wait):
        for i in range(numPixels):
            strandpixels[i] = local.color_random()
            if (i < len(onboardpixels)):
                onboardpixels[i] = local.color_random()
        strandpixels.show()
        onboardpixels.show()
        time.sleep(wait)

startTime = time.monotonic()
while True:
    print("Beginning scroll mode: ", scrollMode, " at time:" + str(time.monotonic() - startTime))
    if scrollMode == 0:
        for color in colorCycleList:
            neopixelstrip_slowlight(color, 0.06)

    if scrollMode == 1:
        for color in colorCycleList:
            neopixelstrip_color_chase(color, 0.06)

    # Some odd problems with this one.  Might need to resolve them before restoring to position 2
    if scrollMode == 2:
        for color in colorCycleList:
            strandpixels.fill(color)
            strandpixels.show()
            onboardpixels.fill(color)
            onboardpixels.show()
            time.sleep(5)

    if scrollMode == 3:
        neopixelstrip_rainbow_cycle(0.1)  # Increase the number to slow down the rainbow.

    if scrollMode == 4:
        neopixelstrip_rainbow(0.2)  # Increase the number to slow down the rainbow.

    # 5: Gentle classy twinkling - each light has a different brightness timer
    if scrollMode == 5:
        for color in colorCycleList:
            neopixelstrip_gentleclassytwinkling(color, 0.04)

    # 6: Rainbow walks down the wire
    if scrollMode == 6:
        neopixelstrip_rainbowwalks(60, 0.1)

    # 5: Gentle classy twinkling - each light has a different brightness timer
    if scrollMode == 7:
        neopixelstrip_gentleclassyrainbowtwinkling(0.05)

    #99: Fully random
    if scrollMode == 99:
        neopixelstrip_random(60, .25)

    scrollMode = (scrollMode+1) % maxScrollMode;