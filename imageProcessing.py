import cv2
import datetime
import sys

from utils import controlDB

# main video에서 차량의 속도 추출해야함
def mainVideo(client, TIME_COUNTER):
  capture = cv2.VideoCapture(0)
  capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
  capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

  fps = capture.get(cv2.CAP_PROP_FPS) #frame per second
  delay = round(1000/fps)

  if not capture.isOpened():
    print("video stream failed")
    sys.exit()

  ret,__ = capture.read()
  if not ret:
      print('get frame failed')
      sys.exit()

  NOW = datetime.datetime.now()
  data = {
    'carNumber' : '',
    'carSpeed' : 0,
    'date' : NOW
  }
    
  while True:
    ret, frame = capture.read()
    cv2.imshow('video', frame)

    print(f"time: {TIME_COUNTER}")

    key = cv2.waitKey(delay)
    if key == ord('q'):
      break

    # 정해진 조건에 해당할 때 
    # carNum = findCarNumber(frame) -> 차량번호 추출
    # controlDB.saveDataToDB(data)
    
    # data 삽입 test
    elif key == ord('i'):
      controlDB.saveDataToDB(client,)
  capture.release()
  cv2.destroyAllWindows()


# findNumberCar를 멀티 쓰레딩 하기 위한 def imageMain 함수
# 또는 asyncio사용해서 바꿀 생각도 하고 있어야 함
def imageMain():
  if __name__ == "__main__":
    print('hello')