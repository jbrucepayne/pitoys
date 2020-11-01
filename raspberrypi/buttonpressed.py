#!/usr/bin/python
import RPi.GPIO as GPIO
import datetime
import time

def button_callback(channel):
  buttonState = GPIO.input(buttonPin)
  GPIO.output(lightPin, buttonState == GPIO.HIGH)
 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

lightPin = 12
buttonPin = 26
GPIO.setup(lightPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#GPIO.add_event_detect(buttonPin,GPIO.RISING,callback=button_callback) 
#GPIO.add_event_detect(buttonPin,GPIO.FALLING,callback=button_callback) 
GPIO.add_event_detect(buttonPin,GPIO.BOTH,callback=button_callback) 

print "Starting to blink GPIO 12 - lightPin"  + datetime.datetime.now().isoformat()
while True:
  #print "GPIO On : " + datetime.datetime.now().isoformat()
  #GPIO.output(lightPin, True)
  #time.sleep(2)
  #print "GPIO Off: " + datetime.datetime.now().isoformat()
  #GPIO.output(lightPin, False)

  #button_state = GPIO.input(buttonPin)
  #if button_state == GPIO.HIGH:
  #  print ("HIGH")
  #else:
  #  print ("LOW")

  time.sleep(0.1)
