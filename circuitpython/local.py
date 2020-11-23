import time
import board
import neopixel
import random
import local
import digitalio

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
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.3, auto_write=False)
    pixels.fill((0, 0, 0))
    pixels.show()
    return pixels

# example SetupNeopixelsStrand(board.A2, 30)
def SetupNeopixelsStrand(pin, numPixels):
    pixels = neopixel.NeoPixel(pin, numPixels, brightness=.3, auto_write=False)
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