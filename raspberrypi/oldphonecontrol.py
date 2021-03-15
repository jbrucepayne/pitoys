#!/usr/bin/python
import sys
import subprocess
import pygame
import sys
import RPi.GPIO as GPIO
import datetime
import requests
import time
import os
from subprocess import PIPE, Popen
from gpiozero import LED

# implement pip as a subprocess - runcmd is required for the weather reader
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'runcmd'])

hookPin = 15
dialSwitchPin = 24
numberSwitchPin = 23

# Don't mess with any hook ups and downs less than 10 seconds - poor man's debounce
callInterval = datetime.timedelta(seconds=10)

#Requires package installation
#sudo apt-get install festival

#Requires installation of packages
def speak_it_to_me(words):
  with open("words.txt", "w") as text_file:
    text_file.write(words)
  os.system('festival --tts words.txt')

def speak_it_to_me_festival_nogood(words):
  process = Popen(['festival', '--tts'], stdin=PIPE)
  #text = 'We love Raspberry.'
  process.stdin.write(words + '\n')
  process.stdin.close()
  process.wait()

# Requires installation of the following package
# sudo apt-get install weather-util
# pip install runcmd
import runcmd
def get_weather():
  w = runcmd.run(["weather","80007"]) 
  if (w.code == 0):
    return w.out
  return "Unable to connect to weather report"

def dial_turned(channel):
  dial_state = GPIO.input(dialSwitchPin)
  while dial_state == GPIO.HIGH:
    num_state = GPIO.input(numberSwitchPin)
    print('Num State in alternate thread: ' + str(num_state))
    dial_state = GPIO.input(dialSwitchPin)

def hook_changed(channel):
  global lastButtonPress
  hookState = GPIO.input(hookPin)
  if hookState == GPIO.HIGH:
    print ("Hook has been lifted")
    if ((datetime.datetime.now() - lastButtonPress) > callInterval):
      w = get_weather()
      speak_it_to_me(w) 
  else:
    print ("Hook has been replaced")

  if ((datetime.datetime.now() - lastButtonPress) > callInterval):
    lastButtonPress = datetime.datetime.now()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(hookPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dialSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(numberSwitchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(hookPin,GPIO.BOTH,callback=hook_changed) 
GPIO.add_event_detect(dialSwitchPin,GPIO.RISING,callback=dial_turned)

lastButtonPress = datetime.datetime.now() - callInterval

while True:
  #print "GPIO On : " + datetime.datetime.now().isoformat()
  #GPIO.output(lightPin, True)
  #time.sleep(2)
  #print "GPIO Off: " + datetime.datetime.now().isoformat()
  #GPIO.output(lightPin, False)

  hook_state = GPIO.input(hookPin)
  #if hook_state == GPIO.HIGH:
  #  print ("Hook Of")
  #else:
  #  print ("Hook On")
  #w = get_weather()
  #speak_it_to_me(w) 

  time.sleep(1)
