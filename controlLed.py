import RPi.GPIO as GPIO
import time

def startSignalLed(main_channel, time_channel):
  while True:
    controlMainLed('RED', 10, main_channel[0])
    controlMainLed('GREEN', 11, main_channel[1], time_channel)
    controlMainLed('YELLOW', 1, main_channel[2])



def controlMainLed(color, delay, main_channel, time_channel = None):  
  GPIO.output(main_channel, GPIO.HIGH)

  if color == 'GREEN':
    controlTimeLed(time_channel)
  else:
    time.sleep(delay)

  GPIO.output(main_channel, GPIO.LOW)


def controlTimeLed(channels):
  time_arr = [11,10,9,8,7,6,5,4,3,2,1]
  
  for channel in channels:
    GPIO.output(channel, GPIO.HIGH)
  
  for channel in channels:
    #t = time_arr[channels.index(channel)]
    time.sleep(0.04)
    #t = 0
    time.sleep(0.96)
    
    GPIO.output(channel, GPIO.LOW)
