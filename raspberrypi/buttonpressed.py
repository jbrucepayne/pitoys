#!/usr/bin/python
import RPi.GPIO as GPIO
import datetime
import requests
import time

callInterval = datetime.timedelta(seconds=120)

iftttUrl = "https://maker.ifttt.com/trigger/WifiButtonPressed/with/key/cDzHzY8eqRhX2hv0O0As-v"

def button_callback(channel):
  global lastButtonPress
  buttonState = GPIO.input(buttonPin)
  GPIO.output(lightPin, buttonState == GPIO.LOW)
  print datetime.datetime.now() - lastButtonPress 
  if ((datetime.datetime.now() - lastButtonPress) > callInterval):
    print "here"
    #requests.post(iftttUrl)
    lastButtonPress = datetime.datetime.now()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

lightPin = 12
buttonPin = 26
GPIO.setup(lightPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#GPIO.add_event_detect(buttonPin,GPIO.RISING,callback=button_callback) 
#GPIO.add_event_detect(buttonPin,GPIO.FALLING,callback=button_callback) 
GPIO.add_event_detect(buttonPin,GPIO.BOTH,callback=button_callback) 

lastButtonPress = datetime.datetime.now() - callInterval

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
