#!/usr/bin/python
import RPi.GPIO as GPIO
import datetime
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
print "Starting to blink GPIO 24" + datetime.datetime.now().isoformat()
while True:
  print "GPIO On : " + datetime.datetime.now().isoformat()
  GPIO.output(24, True)
  time.sleep(2)
  print "GPIO Off: " + datetime.datetime.now().isoformat()
  GPIO.output(24, False)
  time.sleep(2)
