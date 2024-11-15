import sys
import subprocess

# implement pip as a subprocess - runcmd is required for the weather reader
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'runcmd'])

# Requires installation of the following package
# sudo apt-get install weather-util
# pip install runcmd
import runcmd

def get_weather():
  w = runcmd.run(["weather","80007"])
  if (w.code == 0):
    return w.out
  return "Unable to connect to weather report"


