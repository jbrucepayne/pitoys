import board       # basic definitions
import digitalio
import time
import neopixel    # for neopixels
import analogio
import simpleio
import adafruit_thermistor   # onboard thermistor
import audiobusio            # use the microphone for input

# my routines that are set up for ease of use and consistency
import local

# What are the pins available on this board?
x=dir(board)
print(x)

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

relay = digitalio.DigitalInOut(board.TX)
relay.switch_to_output()

light = analogio.AnalogIn(board.LIGHT)

thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)

onboardpixels = local.SetupOnboardNeopixels()
strandpixels = local.SetupNeopixelsStrand(board.A2, 30)

# Use pin A1 for input on the thermocouple (ad8495 circuit)
ad8495 = analogio.AnalogIn(board.A1)

while True:
    ##### Pulse relay and LED in sync
    # led.value = not led.value
    # relay.value = led.value

    ##### Display light sensor result on the onboard Neopixel LEDs
    # This maps to range of 0-9 inclusive
    peak = simpleio.map_range(light.value, 2000, 62000, 0, 9)
    #print(light.value)
    #print(int(peak))
    for i in range(0, 10, 1):
        if i <= peak:
            onboardpixels[i] = local.color_random()
        else:
            onboardpixels[i] = (0, 0, 0)
    onboardpixels.show()

    ##### Temperature from thermistor example.  Doesn't seem super accurate though.
    temp_c = thermistor.temperature
    temp_f = temp_c * 9 / 5 + 32
    print("Thermistor Temperature is:   %f F and %f C" % (temp_f, temp_c))

    ###### Temperature from thermocouple example
    temperature = (local.get_voltage(ad8495) - 1.25) / 0.005
    print ("Thermocouple Temperature is: %f F" % (temperature * 9 / 5 + 32))
    time.sleep(.5)