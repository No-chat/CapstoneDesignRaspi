import cv2
import datetime
import sys
import controlLed
from tracker import *
import numpy as np


class Car():
  def __init__(self):
    self.carNumber = ''
    self.carSpeed = 0
    self.date = ''
    self.condition = ''
    self.img = []

  def setData(self, carSpeed, date, condition, img):
    self.carSpeed = carSpeed
    self.date = date
    self.condition = condition
    self.img = img


# main video에서 차량의 속도 추출해야함
def mainVideo(pipeline):
  tracker = EuclideanDistTracker()

  #Object Detection
  object_detector = cv2.createBackgroundSubtractorMOG2(history=None,varThreshold=None)
  #100,5

  #KERNALS
  kernalOp = np.ones((3,3),np.uint8)
  kernalOp2 = np.ones((5,5),np.uint8)
  kernalCl = np.ones((11,11),np.uint8)
  fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=True)
  kernal_e = np.ones((5,5),np.uint8)

  capture = cv2.VideoCapture(0)
  capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

  fps = capture.get(cv2.CAP_PROP_FPS) 
  delay = round(1000/fps)

  if not capture.isOpened():
    print("video stream failed")
    sys.exit()

  ret,__ = capture.read()
  if not ret:
      print('get frame failed')
      sys.exit()

    
  while True:
    ret, frame = capture.read()
    cv2.imshow('video', frame)
    NOW = datetime.datetime.now()
    # print(f"time: {controlLed.counter}")
    roi = frame[0:480,0:640]

    fgmask = fgbg.apply(roi)
    ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    mask1 = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernalOp)
    mask2 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernalCl)
    e_img = cv2.erode(mask2, kernal_e)

    contours,_ = cv2.findContours(e_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    detections = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        #THRESHOLD
        if 3000 < area < 30000:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(roi,(x,y),(x+w,y+h),(0,255,0),3)
            detections.append([x,y,w,h])

    #Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x,y,w,h,id = box_id


        if(tracker.getsp(id)<tracker.limit()):
            cv2.putText(roi,str(id)+" "+str(tracker.getsp(id)),(x,y-15), cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
        else:
            cv2.putText(roi,str(id)+ " "+str(tracker.getsp(id)),(x, y-15),cv2.FONT_HERSHEY_PLAIN, 1,(0, 0, 255),2)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 165, 255), 3)

        s = tracker.getsp(id)
        if 0 < controlLed.counter < 3:
          if s > 0.7:
            data = {
              'carNumber' : '',
              'carSpeed' : 0,
              'date' : NOW,
              'condition': '조건',
              'img' : frame
            }
            pipeline.put(data)
        

    # DRAW LINES
    cv2.line(roi, (0, 250), (640, 250), (0, 0, 255), 2)
    cv2.line(roi, (0, 270), (640, 270), (0, 0, 255), 2)

    cv2.line(roi, (0, 430), (640, 430), (0, 0, 255), 2)
    cv2.line(roi, (0, 450), (640, 450), (0, 0, 255), 2)

    key = cv2.waitKey(delay)
    if key == ord('q'):
      break
    elif key == ord('c'):
      data = {
        'carNumber' : '',
        'carSpeed' : 0,
        'date' : NOW,
        'condition': '조건',
        'img' : frame
      }
      pipeline.put(data)

    """
    정해진 조건에 해당할 때 data정의 후 인자로 받은 queue에 넣어준다
    차량이 무조건 멈추는 곳에 속도 측정 라인을 정해야함
    data = {
    'carNumber' : 'testdata',
    'carSpeed' : 0,
    'date' : NOW,
    'condition' : '촬영 시 해당하는 조건',
    'img' : frame
    }
    pipeline.put(data)
    """
    
  capture.release()
  cv2.destroyAllWindows()
