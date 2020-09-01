import board
import digitalio
import time
import neopixel
import touchio

# Setup neopixels action
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

# Setup output LED light (by the USB plug) 
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Setup input A button - true when pressed
onboardButtonA = digitalio.DigitalInOut(board.BUTTON_A)
onboardButtonA.switch_to_input(pull=digitalio.Pull.DOWN)

# Setup input B button - true when pressed
onboardButtonB = digitalio.DigitalInOut(board.BUTTON_B)
onboardButtonB.switch_to_input(pull=digitalio.Pull.DOWN)

# Setup input onboard switch - true when switch is slid to the left.
switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.switch_to_input(pull=digitalio.Pull.UP)

# Setup input capacative touch - true when touched
#touch_A0 = touchio.TouchIn(board.A0)
touch_A1 = touchio.TouchIn(board.A1)
touch_A2 = touchio.TouchIn(board.A2)
touch_A3 = touchio.TouchIn(board.A3)
touch_A4 = touchio.TouchIn(board.A4)
touch_A5 = touchio.TouchIn(board.A5)
touch_A6 = touchio.TouchIn(board.A6)
touch_A7_TX = touchio.TouchIn(board.TX)

def lightbuttonviaxor():
    if onboardButtonA.value == onboardButtonB.value:   
        led.value = True
    else:
        led.value = False

def lightbuttonswitchleft():
    led.value = switch.value

def setneopixelstate():
    for pixel in pixels:
        pixel = (0,0,0)
    
    if(onboardButtonA.value == True): 
        pixels[0]=(0,255,0)
    else:
        pixels[0]=(0,0,0)
        
    pixels[4]=(255,255,0)
    pixels[7]=(0,255,255)
    pixels[5]=(255,255,255)

#    pixels[5] = (0,255,0) if touch_A0.value else (0,0,0)
    pixels[6] = (0,0,255) if touch_A1.value else (0,0,0)
    pixels[8] = (255,255,255) if touch_A2.value else (0,0,0)
    pixels[9] = (255,0,0) if touch_A3.value else (0,0,0)
    pixels[3] = (255,0,0) if touch_A7_TX.value else (0,0,0)
    pixels[2] = (255,0,0) if touch_A6.value else (0,0,0)
    pixels[1] = (255,0,255) if touch_A5.value else (0,0,0)
    pixels[0] = (255,0,255) if touch_A4.value else (0,0,0)
    pixels.show()

while True:
    lightbuttonviaxor()
    setneopixelstate()
    #lightbuttonswitchleft()
    time.sleep(0.01)

