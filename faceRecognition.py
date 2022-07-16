import cv2
from PIL import Image
import time
import os

face_cascade = cv2.CascadeClassifier('./Cascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./Cascades/haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

while True:
  ret, img = cap.read()
  img = cv2.flip(img, 1)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)

  for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    # print (int(x+w/2), int(y+h/2))
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex, ey, ew, eh) in eyes:
      os.makedirs('./recognize/', exist_ok=True) # 输出目录
      now = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
      pic = cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)
      cv2.imshow('识别', pic)
      if cv2.waitKey(1) & 0xFF == ord('s'):
        # cv2.imwrite('./recognize/' + now + '.jpg', cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0, 0, 255), 2))
        cv2.imwrite('./recognize/' + now + '.jpg', pic)
        break
    # cv2.imshow('img', img)
    # cv2.imwrite('1.jpg', img)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
  
print('Done')

cap.release()
cv2.destroyAllWindows()