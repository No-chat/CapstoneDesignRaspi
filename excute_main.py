# import installed_module
from pymongo import MongoClient
from multiprocessing import Process, Lock, Value
import RPi.GPIO as GPIO
import sys

# import user_defined_module
from controlLed import startSignalLed
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
  

  sharedCount = Value('i', 0)
  lock = Lock()

  p1 = Process(target=mainVideo, args = (client, sharedCount, lock))
  p2 = Process(target=startSignalLed, args = (MAIN_LED, TIME_LED, sharedCount, lock))
  p1.start()
  p2.start()
  p1.join()
  p2.join()

  GPIO.cleanup()
  client.close()