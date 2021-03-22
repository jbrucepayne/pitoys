#!/usr/bin/python
import sys
import os
import subprocess
from subprocess import PIPE, Popen
import RPi.GPIO as GPIO
import time
import datetime
import requests
from gpiozero import LED

# Local files that are simple wrappers to make it easier to ingest information
import horoscope
import joke
import weather

# hardware pin IDs in use on pi board
hookPin = 15
dialSwitchPin = 24
numberSwitchPin = 23

# count is the number of clicks we have counted, while dialed number will contain the full sequence
count = 0
dialed_number = 0
previous_number_state = GPIO.LOW
is_counting = False

# Don't mess with any hook ups and downs less than 10 seconds - poor man's debounce
callInterval = datetime.timedelta(seconds=10)

def handle_number(number):
    if int(number) == 1:
        x=1
    elif int(number) == 2:
        speak_it_to_me ("One Six Eight Nine Seven West 73rd place, arvada colorado 80007")
    elif int(number) == 3:
        speak_it_to_me ("three")
    elif int(number) == 4:
        speak_it_to_me (horoscope.get_horoscope('sagittarius'))
    elif int(number) == 5:
        speak_it_to_me (joke.get_joke())
    elif int(number) == 6:
        speak_it_to_me ("six")
    elif int(number) == 7:
        speak_it_to_me ("seven")
    elif int(number) == 8:
        x=8
    elif int(number) == 9:
        speak_it_to_me (weather.get_weather())
    elif int(number) == 10:
        speak_it_to_me (get_help_message())
    else: 
       speak_it_to_me (number)

def get_help_message():
  return ("Dial 2 for current address. " + 
    "Dial 3 for the word 3. " +
    "Dial 4 for a horoscope. " +
    "Dial 5 for a joke. " +
    "Dial 6 for the word 6. " +
    "Dial 7 for the word 7. " +
    "Dial 8 for the sound of silence. " +
    "Dial 9 for weather. " +
    "Dial 0 to repeat this message. " ) 

#Requires package installation
#sudo apt-get install festival

#Requires installation of packages
def speak_it_to_me(words):
  with open("words.txt", "w") as text_file:
    text_file.write(words)
  os.system('festival --tts words.txt')

def dial_changed(channel):
  global count, previous_number_state, is_counting
  dial_state = GPIO.input(dialSwitchPin)
  if dial_state == GPIO.HIGH:
    #print ("Dial Begin")
    count = 0
    is_counting = True
  else:
    # print ("Dial End")
    handle_number(str(count))
    count = 0
    is_counting = False

def number_changed(channel):
  global count, previous_dial_state, is_counting
  number_state = GPIO.input(numberSwitchPin) 
  if number_state == GPIO.HIGH:
    #print ("Number Of")
    count = count + 1
  #else:
    #print ("Number On")
  

def hook_changed(channel):
  global lastButtonPress
  hookState = GPIO.input(hookPin)
  #if hookState == GPIO.HIGH:
    #print ("Hook has been lifted")
    #if ((datetime.datetime.now() - lastButtonPress) > callInterval):
      #w = weather.get_weather()
      #speak_it_to_me(w) 
  #else:
    # print ("Hook has been replaced")
  
  if ((datetime.datetime.now() - lastButtonPress) > callInterval):
    lastButtonPress = datetime.datetime.now()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(hookPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dialSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(numberSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(hookPin,GPIO.BOTH,callback=hook_changed) 
GPIO.add_event_detect(numberSwitchPin,GPIO.BOTH,callback=number_changed)
GPIO.add_event_detect(dialSwitchPin,GPIO.BOTH,callback=dial_changed)

lastButtonPress = datetime.datetime.now() - callInterval

while True:
  # Getting state and brief sleep help in reducing noise for the hardware in the rotary counter.
  # Leave these in unless you know what you are doing and can handle the rotary noise.
  hook_state = GPIO.input(hookPin)
  time.sleep(0.1)
  pass
