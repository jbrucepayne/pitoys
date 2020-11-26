import time
import board
import neopixel
import random
import local
import digitalio

gammaTable = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2,
2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5,
5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10,
10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255)

def gammaCorrectValue(brightnessIntended):
    return gammaTable[brightnessIntended];

def gammaCorrectPixel(pixelValue):
    return (gammaCorrectValue(pixelValue[0]), gammaCorrectValue(pixelValue[1]), gammaCorrectValue(pixelValue[2]))

# Setup input capacative touch - true when touched
#touch_A0 = touchio.TouchIn(board.A0)
def setupAllTouchInputs():
    touch_A1 = touchio.TouchIn(board.A1)
    touch_A2 = touchio.TouchIn(board.A2)
    touch_A3 = touchio.TouchIn(board.A3)
    touch_A4 = touchio.TouchIn(board.A4)
    touch_A5 = touchio.TouchIn(board.A5)
    touch_A6 = touchio.TouchIn(board.A6)
    touch_A7_TX = touchio.TouchIn(board.TX)

def color_volume(volume, numPixels):
    return 200, volume * (255 // numPixels), 0

def color_random():
    return (random.randrange(255),random.randrange(255),random.randrange(255))

def color_wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def SetupOnboardNeopixels():
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)
    pixels.fill((0, 0, 0))
    pixels.show()
    return pixels

# example SetupNeopixelsStrand(board.A2, 30)
def SetupNeopixelsStrand(pin, numPixels):
    pixels = neopixel.NeoPixel(pin, numPixels, auto_write=False)
    pixels.fill((0, 0, 0))
    pixels.show()
    return pixels

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def color_for_temperature (temperature):
    if temperature >= 60:
        return (0,255,0)
    if temperature >= 50:
        return (0,0,255)
    if temperature >= 40:
        return (255,255,0)
    if temperature < 40:
        return (255,0,0)

    # White is default if we don't know what else to do!
    return (255,255,255)