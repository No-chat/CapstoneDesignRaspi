# import installed_module
from pymongo import MongoClient
from threading import Thread
from queue import Queue
import RPi.GPIO as GPIO
import sys

# import user_defined_module
from controlLed import startSignalLed
from imageProcessing import mainVideo
from num_extract import extract_thread
from config import config
# mongodb+srv://<username>:<password>@capstoneserver.ujte3.mongodb.net/?retryWrites=true&w=majority

# use gpio pin number
GPIO.setmode(GPIO.BCM)

# ignore warning
GPIO.setwarnings(False)

# set ledpin
MAIN_LED = [16,21,20]
TIME_LED = [19,23,6,5,25,24,23,22,27,17,4]

def main_func():
  
  for PIN in TIME_LED:
    GPIO.setup(PIN, GPIO.OUT)
  for PIN in MAIN_LED:
    GPIO.setup(PIN, GPIO.OUT)
  try:
    client = MongoClient(config.mongoURI)
  except:
    print('Database connect error')
    sys.exit()

  pipeline = Queue(maxsize=10)
  
  
  t1 = Thread(target=startSignalLed, args = (MAIN_LED, TIME_LED,))
  t2 = Thread(target=mainVideo, args=(pipeline, ))
  t3 = Thread(target=extract_thread, args=(pipeline, client, ))
  t1.start()
  t2.start()
  t3.start()

  t1.join()
  t2.join()
  t3.join()
  
  GPIO.cleanup()
  client.close()

if __name__ == '__main__':
  main_func()