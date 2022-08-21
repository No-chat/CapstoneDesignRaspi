# import installed_module
from pymongo import MongoClient
from threading import Thread
import RPi.GPIO as GPIO
import sys

# import user_defined_module
import controlLed
from imageProcessing import mainVideo
from config import config
# mongodb+srv://<username>:<password>@capstoneserver.ujte3.mongodb.net/?retryWrites=true&w=majority

# use gpio pin number
GPIO.setmode(GPIO.BCM)

# ignore warning
GPIO.setwarnings(False)

# set ledpin
MAIN_LED = [16,21,20]
TIME_LED = [19,23,6,5,25,24,23,22,27,17,4]



if __name__ == '__main__':
  for PIN in TIME_LED:
    GPIO.setup(PIN, GPIO.OUT)
  for PIN in MAIN_LED:
    GPIO.setup(PIN, GPIO.OUT)
  try:
    client = MongoClient(config.mongoURI)
  except:
    print('Database connect error')
    sys.exit()
  
  
  t1 = Thread(target=controlLed.startSignalLed, args = (MAIN_LED, TIME_LED, ))
  t1.start()
  mainVideo(client, controlLed.TIME_COUNTER)
  t1.join()

  GPIO.cleanup()
  client.close()