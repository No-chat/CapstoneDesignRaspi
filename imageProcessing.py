import cv2
import keyboard
import datetime
import asyncio

from utils import controlDB

# main video에서 차량의 속도 추출해야함
def mainVideo(client, sharedCount, lock):
  capture = cv2.VideoCapture(0)
  capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

  
  while True:
    ret, frame = capture.read()
    cv2.imshow('video', frame)

    # 정해진 조건에 해당할 때 
    # carNum = findCarNumber(frame) -> 차량번호 추출
    # controlDB.saveDataToDB(data)
    
    # data 삽입 test
    if keyboard.is_pressed('q'):
      data = {
        'carNumber' : '12가3456',
        'carSpeed' : 70,
        'date' : datetime.datetime.now()
      }
      controlDB.saveDataToDB(client, data)
      break
    elif sharedCount.value == 5:
      break

  capture.release()
  cv2.destroyAllWindows()

