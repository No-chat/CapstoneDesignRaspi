import cv2
import datetime
import sys
import controlLed

# main video에서 차량의 속도 추출해야함
def mainVideo(pipeline):
  capture = cv2.VideoCapture(0)
  capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
  capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

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
    # print(f"time: {TIME_COUNTER}")

    key = cv2.waitKey(delay)
    if key == ord('q'):
      break
    elif key == ord('c'):
      data = {
        'carNumber' : 'testdata',
        'carSpeed' : 0,
        'date' : NOW,
        'condition' : '촬영 시 해당하는 조건',
        'img' : frame
      }
      pipeline.put(data)
    #print(controlLed.counter)

    """
    정해진 조건에 해당할 때 data정의 후 인자로 받은 queue에 넣어준다
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
