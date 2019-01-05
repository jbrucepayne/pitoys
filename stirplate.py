# Import the GPIO capabilities needed for the Pi
import RPi.GPIO as GPIO

#Import sleep function for main loop
from time import sleep
from time import time

#use select for keyboard I/O handling
import select

# Setup Pinout definitions
GPIO.setmode(GPIO.BCM)

# Input and output pins for fan setup
GPIO.setup(14, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pwm = GPIO.PWM(14,25000)
width = 0
responseCount = 0
startTime = time()

def UpdatePulseWidth(newPw):
	print ("New pulse width set:") + "{:d}".format(newPw)
	pwm.ChangeDutyCycle(newPw)


def ReceiveCallback(channel):
	global responseCount
	global startTime
	responseCount = responseCount + 1
	if responseCount == 200 :
		endTime = time()
		delta = endTime-startTime
		#deltaFloat = delta.seconds + delta.microseconds/1E6
		#defined as 2 pulses per revolution
		print "time for 100 rotations: " + "{:f}".format(delta)
		print "inferred RPM: " + "{:f}".format(6000./delta)
		responseCount = 0
		startTime = time()
	#s = select.poll()
	#if s:
	#	print s
	#print "Callback" 


try:
	print "setup"
	#GPIO.add_event_detect(15, GPIO.RISING, callback=ReceiveCallback)
	GPIO.add_event_detect(15, GPIO.FALLING, callback=ReceiveCallback)
	pwm.start(0)
	while True:  # ifinite loop
		#width = (width + 1) % 99
		width = 0
		UpdatePulseWidth(width)
		sleep(61.0)
		#width = 100
		#UpdatePulseWidth(width)
		#sleep(61.0)

finally:
	pwm.ChangeDutyCycle(0)
	GPIO.remove_event_detect(15)
#	GPIO.cleanup()
