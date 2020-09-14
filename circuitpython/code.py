import board       # basic definitions
import digitalio
import time
import neopixel    # for neopixels
import analogio
import simpleio
import adafruit_thermistor   # onboard thermistor
import audiobusio            # use the microphone for input
import math                  # for microphone example
import array                 # for microphone example

# my routines that are set up for ease of use and consistency
import local

# What are the pins available on this board?
x=dir(board)
print(x)

# Current pins in use
ledOutputPin = board.D13
relayPin = board.TX
lightSensorPin=board.LIGHT
thermistorPin=board.TEMPERATURE
strandPixelPin=board.A2
thermocoupleInputPin=board.A1

led = digitalio.DigitalInOut(ledOutputPin)
led.direction = digitalio.Direction.OUTPUT

relay = digitalio.DigitalInOut(relayPin)
relay.switch_to_output()

light = analogio.AnalogIn(lightSensorPin)

thermistor = adafruit_thermistor.Thermistor(thermistorPin, 10000, 10000, 25, 3950)

onboardpixels = local.SetupOnboardNeopixels()

numPixels = 30
strandpixels = local.SetupNeopixelsStrand(strandPixelPin, 30)

peakColor = (100, 0, 255)  # Color of the peak pixel for audio display
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,sample_rate=16000, bit_depth=16)
input_floor = 50  # Example adapts from the first read
input_ceiling = input_floor + 500
peak = 0

# Use pin A1 for input on the thermocouple (ad8495 circuit)
ad8495 = analogio.AnalogIn(thermocoupleInputPin)

##################### FROM AUDIO MICROPHONE EXAMPLE
# Exponential scaling factor.
# Should probably be in range -10 .. 10 to be reasonable.
CURVE = 2
SCALE_EXPONENT = math.pow(10, CURVE * -0.1)

# Number of samples to read at once.
NUM_SAMPLES = 160
samples = array.array('H', [0] * NUM_SAMPLES)

# Restrict value to be between floor and ceiling.
def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))


# Scale input_value between output_min and output_max, exponentially.
def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / \
                             (input_max - input_min)
    return output_min + \
        math.pow(normalized_input_value, SCALE_EXPONENT) \
        * (output_max - output_min)


# Remove DC bias before computing RMS.
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))


def mean(values):
    return sum(values) / len(values)

###### Display sound level max to offboard neopixel strand
def setPixelColorsFromVolume():
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    # print("Audio Magnitude is: %f F" % (magnitude)))
    # Compute scaled logarithmic reading in the range 0 to numPixels
    c = log_scale(constrain(magnitude, input_floor, input_ceiling), input_floor, input_ceiling, 0, numPixels)
    strandpixels.fill(0)
    peak=0
    for i in range(numPixels):
        if i < c:
            strandpixels[i] = local.color_volume(i,numPixels)
        # Light up the peak pixel and animate it slowly dropping.
        if c >= peak:
            peak = min(c, numPixels - 1)
        elif peak > 0:
            peak = peak - 1
        if peak > 0:
            strandpixels[int(peak)] = peakColor
    strandpixels.show()
##################### END FROM AUDIO MICROPHONE EXAMPLE

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

def setPixelColorsByTemperature(temperature):
    strandpixels.fill(color_for_temperature(temperature))
    strandpixels.show()

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
    #print("Thermistor Temperature is:   %f F and %f C" % (temp_f, temp_c))

    ###### Temperature from thermocouple
    thermistor_c = (local.get_voltage(ad8495) - 1.25) / 0.005
    thermistor_f = thermistor_c * 9 / 5 + 32
    print ("Thermocouple Temperature is: %f F" % (thermistor_f))
    setPixelColorsByTemperature(thermistor_f)


    #### Audio example, make lights light VU meter
    #setPixelColorsFromVolume()

    time.sleep(60.0)