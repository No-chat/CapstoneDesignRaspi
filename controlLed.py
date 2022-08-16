import RPi.GPIO as GPIO
import time
import keyboard


def startSignalLed(main_channel, time_channel, sharedCount, lock):
  while True:
    controlMainLed('RED', 10, main_channel[0])
    controlMainLed('GREEN', 10, main_channel[1], time_channel, sharedCount, lock)
    controlMainLed('YELLOW', 1, main_channel[2])
    if keyboard.is_pressed('q'):
      GPIO.cleanup()
      break

# 
def controlMainLed(color, delay, main_channel, time_channel = None, sharedCount = 0, lock = None):  
  GPIO.output(main_channel, GPIO.HIGH)
  if color == 'GREEN':
    controlTimeLed(time_channel, sharedCount, lock)
  else:
    time.sleep(delay)
  GPIO.output(main_channel, GPIO.LOW)

  


def controlTimeLed(channels, sharedCount, lock):
  with lock:
    sharedCount.value = 10
  for channel in channels:
    GPIO.output(channel, GPIO.HIGH)
  
  for channel in channels:
    time.sleep(1)
    with lock:
      sharedCount.value -= 1
    GPIO.output(channel, GPIO.LOW)
