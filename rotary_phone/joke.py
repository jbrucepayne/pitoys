import requests
import json

# requires import python -m pip install requests
url = "http://api.icndb.com/jokes/random"

def get_joke():
  response = requests.request("POST", url)
  parsed = json.loads(response.text)
  return (parsed["value"]["joke"])
