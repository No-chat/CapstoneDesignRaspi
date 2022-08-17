# import installed_module
from pymongo import MongoClient
from threading import Thread
import RPi.GPIO as GPIO
import sys

# import user_defined_module
from controlLed import *
from imageProcessing import mainVideo
from config import config
# mongodb+srv://<username>:<password>@capstoneserver.ujte3.mongodb.net/?retryWrites=true&w=majority

# use gpio pin number
GPIO.setmode(GPIO.BCM)

# ignore warning
GPIO.setwarnings(False)

# set ledpin
MAIN_LED = []
TIME_LED = []

if __name__ == '__main__':
  try:
    client = MongoClient(config.mongoURI)
  except:
    print('Database connect error')
    sys.exit()
  
  
  t1 = Thread(target=startSignalLed, args = (MAIN_LED, TIME_LED, ))
  t1.start()
  mainVideo(client, TIME_COUNTER)
  t1.join()

  GPIO.cleanup()
  client.close()